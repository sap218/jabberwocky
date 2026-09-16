#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2026
@author: Samantha Pendleton
@description: Streamlit app for loading a corpus and classes of interest.
@GitHub: github.com/sap218/jabberwocky

@useful links:
    # https://docs.streamlit.io/
"""

from datetime import datetime
from io import BytesIO, StringIO
from pathlib import Path
import csv
import html
import re
import sys
import xml.etree.ElementTree as ET

from nltk import ngrams
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
from wordcloud import WordCloud

APP_DIR = Path(__file__).resolve().parent
WORKSPACE_ROOT = APP_DIR.parent

if str(WORKSPACE_ROOT) not in sys.path:
    sys.path.insert(0, str(WORKSPACE_ROOT))

from highlevel import clean_lower_lemma, stopWords
DEFAULT_TEXT_PATH = WORKSPACE_ROOT / "test" / "CelestialObject" / "corpus" / "social_media_posts.txt"
DEFAULT_CLASSES_PATH = WORKSPACE_ROOT / "test" / "CelestialObject" / "corpus" / "classes_of_interest.txt"
DEFAULT_ONTOLOGY_TAGS_PATH = WORKSPACE_ROOT / "test" / "CelestialObject" / "corpus" / "ontology_tags.txt"
DEFAULT_ONTOLOGY_PATH = WORKSPACE_ROOT / "01_converter" / "test" / "20260122-203441_space.owl"

@st.cache_data(show_spinner=False)
def load_file_text(file_path: Path) -> str:
    if file_path.exists():
        return file_path.read_text(encoding="utf-8")
    return ""


def get_timestamped_filename(prefix: str, suffix: str) -> str:
    timestamp = datetime.today().strftime("%Y%m%d-%H%M%S")
    return f"{timestamp}_{prefix}{suffix}"


@st.cache_data(show_spinner=False)
def get_stopwords_list():
    stopword_level = stopWords[2]
    stopwords_lemma = []
    stopwords_list = []

    for word in stopword_level:
        stopwords_lemma.append(clean_lower_lemma(word, "stopwords", stopwords_list))

    stopwords_lemma_flat = [word for phrase in stopwords_lemma for word in phrase.split()]
    return sorted(set(filter(None, stopwords_lemma_flat)))


@st.cache_data(show_spinner=False)
def normalize_for_matching(text: str, stopwords_list, mode: str):
    if not text:
        return []

    normalized = clean_lower_lemma(text, mode, stopwords_list)
    return [token for token in normalized if token]


def contains_term_as_subsequence(line_tokens, term_tokens):
    if not term_tokens or not line_tokens:
        return False

    matched = 0
    for token in line_tokens:
        if matched < len(term_tokens) and token == term_tokens[matched]:
            matched += 1

    return matched == len(term_tokens)


@st.cache_data(show_spinner=False)
def build_highlighted_corpus_data(corpus_text: str, match_terms):
    if not corpus_text:
        return {
            "html": "",
            "highlighted_lines": [],
            "non_highlighted_lines": [],
        }

    stopwords_list = get_stopwords_list()

    normalized_terms = []
    for term in match_terms:
        normalized_term = normalize_for_matching(term, stopwords_list, "wordsInterest")
        if normalized_term:
            normalized_terms.append(normalized_term)

    if not normalized_terms:
        return {
            "html": "",
            "highlighted_lines": [],
            "non_highlighted_lines": [line.strip("\n") for line in corpus_text.splitlines() if line.strip()],
        }

    highlighted_lines = []
    non_highlighted_lines = []
    html_lines = []

    for line in corpus_text.splitlines():
        if not line.strip():
            continue

        normalized_line = normalize_for_matching(line, stopwords_list, "corpus")
        is_match = any(contains_term_as_subsequence(normalized_line, term) for term in normalized_terms)

        if is_match:
            highlighted_lines.append(line)
            html_lines.append(
                f"<div><mark style='background-color: #9be7ff; color: #0f172a; border-radius: 4px; padding: 0 2px;'>{html.escape(line)}</mark></div>"
            )
        else:
            non_highlighted_lines.append(line)
            html_lines.append(f"<div>{html.escape(line)}</div>")

    html_output = (
        "<div style='max-height: 440px; overflow-y: auto; white-space: pre-wrap; "
        "line-height: 1.6; font-family: monospace; padding: 0.5rem;'>"
        + "".join(html_lines)
        + "</div>"
    )

    return {
        "html": html_output,
        "highlighted_lines": highlighted_lines,
        "non_highlighted_lines": non_highlighted_lines,
    }


@st.cache_data(show_spinner=False)
def build_class_synonym_match_rows(corpus_text: str, ontology_classes, include_unmatched):
    stopwords_list = get_stopwords_list()
    rows = []
    corpus_lines = []
    for line in corpus_text.splitlines():
        if not line.strip():
            continue
        corpus_lines.append((
            line,
            normalize_for_matching(line, stopwords_list, "corpus"),
        ))

    for class_name, annotations in ontology_classes.items():
        normalized_class = normalize_for_matching(class_name, stopwords_list, "wordsInterest")
        class_matches = [
            line
            for line, normalized_line in corpus_lines
            if contains_term_as_subsequence(normalized_line, normalized_class)
        ]
        if class_matches:
            rows.extend(
                {
                    "class": class_name,
                    "synonym": None,
                    "sentence": line,
                }
                for line in class_matches
            )
        elif include_unmatched:
            rows.append({"class": class_name, "synonym": None, "sentence": None})

        seen_synonyms = set()
        for annotation_tag in annotations:
            for synonym in annotations[annotation_tag]:
                if synonym in seen_synonyms:
                    continue
                seen_synonyms.add(synonym)

                normalized_synonym = normalize_for_matching(synonym, stopwords_list, "wordsInterest")
                synonym_matches = [
                    line
                    for line, normalized_line in corpus_lines
                    if normalized_synonym
                    and contains_term_as_subsequence(normalized_line, normalized_synonym)
                ]
                if synonym_matches:
                    rows.extend(
                        {
                            "class": class_name,
                            "synonym": synonym,
                            "sentence": line,
                        }
                        for line in synonym_matches
                    )
                elif include_unmatched:
                    rows.append({"class": class_name, "synonym": synonym, "sentence": None})

    return rows


@st.cache_data(show_spinner=False)
def build_class_synonym_csv(rows):
    buffer = StringIO()
    writer = csv.writer(buffer, delimiter="\t")
    writer.writerow(["class", "synonym", "sentence"])

    for row in rows:
        writer.writerow([
            row["class"],
            row["synonym"] or "",
            row["sentence"] or "",
        ])

    return buffer.getvalue()


@st.cache_data(show_spinner=False)
def parse_ngram_values(ngram_text: str):
    if not ngram_text or not ngram_text.strip():
        return [1]

    parsed_values = []
    for chunk in re.split(r"[,\s]+", ngram_text.strip()):
        if not chunk:
            continue
        try:
            value = int(chunk)
        except ValueError:
            continue
        if value >= 1:
            parsed_values.append(value)

    return sorted(set(parsed_values)) if parsed_values else [1]


@st.cache_data(show_spinner=False)
def build_tfidf_ranked_terms(corpus_text: str, ngram_values):
    if not corpus_text or not ngram_values:
        return pd.DataFrame()

    stopwords_list = get_stopwords_list()
    cleaned_posts = []

    for line in corpus_text.splitlines():
        if not line.strip():
            continue
        cleaned = clean_lower_lemma(line, "corpus", stopwords_list)
        if cleaned:
            cleaned_posts.append(" ".join(cleaned))

    if not cleaned_posts:
        return pd.DataFrame()

    ngram_strings = []
    for post in cleaned_posts:
        ngram_tokens = []
        for n in ngram_values:
            ngram_tokens.extend("_".join(gram) for gram in ngrams(post.split(), n))
        ngram_strings.append(" ".join(ngram_tokens))

    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(ngram_strings)

    tfidf_df = pd.DataFrame(
        data=tfidf_matrix.toarray(),
        columns=tfidf_vectorizer.get_feature_names_out(),
    )

    tfidf_df["Sentence"] = cleaned_posts
    summary_scores = tfidf_df.drop(columns=["Sentence"]).agg("mean", axis=0)

    ranked_df = pd.DataFrame({
        "Word": summary_scores.index,
        "Raw score": summary_scores.values,
    })

    scaler = MinMaxScaler()
    ranked_df["Normalised score"] = scaler.fit_transform(ranked_df[["Raw score"]])
    ranked_df = ranked_df.sort_values("Normalised score", ascending=False)
    ranked_df = ranked_df[ranked_df["Normalised score"] != 0].copy()

    ranked_df["Raw score"] = ranked_df["Raw score"].round(decimals=3)
    ranked_df["Normalised score"] = ranked_df["Normalised score"].round(decimals=3)

    return ranked_df.reset_index(drop=True)


@st.cache_data(show_spinner=False)
def remove_class_synonyms_from_corpus(corpus_text: str, requested_terms):
    if not corpus_text or not requested_terms:
        return corpus_text

    stopwords_list = get_stopwords_list()
    normalized_terms = [
        normalize_for_matching(term, stopwords_list, "wordsInterest")
        for term in requested_terms
    ]
    normalized_terms = sorted(
        (term for term in normalized_terms if term),
        key=len,
        reverse=True,
    )

    filtered_lines = []
    for line in corpus_text.splitlines():
        if not line.strip():
            continue

        remaining_tokens = normalize_for_matching(line, stopwords_list, "corpus")
        changed = True
        while changed:
            changed = False
            for term_tokens in normalized_terms:
                term_length = len(term_tokens)
                index = 0
                while index <= len(remaining_tokens) - term_length:
                    if remaining_tokens[index:index + term_length] == term_tokens:
                        del remaining_tokens[index:index + term_length]
                        changed = True
                    else:
                        index += 1

        if remaining_tokens:
            filtered_lines.append(" ".join(remaining_tokens))

    return "\n".join(filtered_lines)


@st.cache_data(show_spinner=False)
def build_normalized_corpus_lines(corpus_text: str):
    if not corpus_text:
        return []

    stopwords_list = get_stopwords_list()
    normalized_lines = []

    for line in corpus_text.splitlines():
        if not line.strip():
            continue
        normalized_line = clean_lower_lemma(line, "corpus", stopwords_list)
        if normalized_line:
            normalized_lines.append(normalized_line)

    return normalized_lines


@st.cache_data(show_spinner=False)
def build_wordcloud_image(corpus_text: str):
    if not corpus_text:
        return None

    lemmatised_tokens = [
        token
        for line_tokens in build_normalized_corpus_lines(corpus_text)
        for token in line_tokens
    ]

    if not lemmatised_tokens:
        return None

    wordcloud = WordCloud(
        width=2400,
        height=1350,
        background_color="white",
        colormap="plasma",
        max_words=40,
        min_font_size=10,
        collocations=True,
        normalize_plurals=False,
        prefer_horizontal=0.8,
        scale=2,
        random_state=123,
    )

    wordcloud.generate(" ".join(lemmatised_tokens))

    fig, ax = plt.subplots(figsize=(16, 9), dpi=300)
    ax.imshow(wordcloud, interpolation="bilinear")
    ax.axis("off")

    buffer = BytesIO()
    fig.savefig(buffer, format="png", bbox_inches="tight", pad_inches=0, dpi=300)
    plt.close(fig)

    return buffer.getvalue()


@st.cache_data(show_spinner=False)
def extract_classes_with_annotations(ontology_text: str, classes_of_interest_text: str, annotation_tags):
    if not ontology_text or not annotation_tags:
        return {}

    try:
        root = ET.fromstring(ontology_text)
    except ET.ParseError:
        return {}

    classes_and_annotations = {}

    for concept in root.iter():
        if concept.tag.split("}")[-1] != "Class":
            continue

        label = None
        for child in concept:
            child_name = child.tag.split("}")[-1]
            if child_name == "label" and child.text:
                label = child.text.strip()
                break

        if not label:
            continue

        annotations_by_tag = {}
        for tag_format in annotation_tags:
            local_name = tag_format.split(":", 1)[1] if ":" in tag_format else tag_format
            matching_values = []

            for child in concept:
                child_name = child.tag.split("}")[-1]
                if child_name == local_name and child.text and child.text.strip():
                    matching_values.append(child.text.strip())

            if matching_values:
                annotations_by_tag[tag_format] = sorted(set(matching_values))

        classes_and_annotations[label] = annotations_by_tag

    classes_of_interest_lines = [line.strip() for line in classes_of_interest_text.splitlines() if line.strip()]

    if classes_of_interest_lines:
        expanded_concepts = {}
        for word in classes_of_interest_lines:
            if word in classes_and_annotations:
                expanded_concepts[word] = classes_and_annotations[word]
            else:
                expanded_concepts[word] = {}
        return expanded_concepts

    return classes_and_annotations.copy()

#########################

st.title("Jabberwocky")

st.markdown("a toolkit for Natural Language Processing (NLP) and Ontologies &nbsp; <small>@ sap218</small>",unsafe_allow_html=True)

link_colsA, link_colsB, link_colsC, _ = st.columns([0.15, 0.15, 0.15, 0.6], gap="small")
with link_colsA:
    st.link_button("JOSS", "https://joss.theoj.org/papers/10.21105/joss.02168")
with link_colsB:
    st.link_button("Github", "https://github.com/sap218/jabberwocky")
with link_colsC:
    st.link_button("Post", "https://sap218.uk/projects/jabberwocky/")

#########################

sample_text = load_file_text(DEFAULT_TEXT_PATH)
classes_of_interest = load_file_text(DEFAULT_CLASSES_PATH)
ontology_tags_text = load_file_text(DEFAULT_ONTOLOGY_TAGS_PATH)
ontology_text = load_file_text(DEFAULT_ONTOLOGY_PATH)

#########################

with st.container():#border=True):
    with st.form("input_form"):
        #st.markdown("### Inputs")

        #st.markdown("##### Corpus")

        uploaded_file = st.file_uploader("Corpus:", type=["txt"], key="uploaded_file",
            help=("Upload a TXT file (new line delimited) of your corpus"),
        )

        #st.markdown("##### Words-of-Interest")

        uploaded_classes_file = st.file_uploader("Words-of-Interest file:", type=["txt"], key="uploaded_classes_file",
            help=("Upload a TXT file (new line delimited) of your words of interest"),
        )

        use_all_ontology_classes = st.checkbox("Use all classes from the ontology", key="use_all_ontology_classes",
            help="Bypass the Words-of-Interest file input and use all classes found in the ontology",
        )

        #st.markdown("##### Ontology")

        uploaded_ontology_file = st.file_uploader("Ontology file:", type=["owl"], key="uploaded_ontology_file",
            help=("Upload an OWL file (RDF/XML format)"),
        )

        uploaded_ontology_tags_file = st.file_uploader("Ontology tags:", type=["txt"], key="uploaded_ontology_tags_file",
            help=(
                "Upload a TXT file (new line delimited) of the ontology tags for metadata extraction of the words of interest\n\n"
                "If unsure, run as is and see bottom of page for an example"
                ),
        )

        #st.markdown("##### Wordcloud")

        #st.markdown("##### Important terms analysis")

        tfidf_corpus_mode = st.radio("TF-IDF performed on:", options=["Whole corpus", "Corpus with classes and synonyms removed"],
            key="tfidf_corpus_mode", help="Choose how to preprocess the corpus for TF-IDF",
        )

        ngram_input = st.text_input("N-grams to consider for TF-IDF:",value="1,2,3",
            help="Comma-separated values, for example: 1,2,3",
        )

        st.markdown("<small><i>running without uploading will use test files as a placeholder</i></small>", unsafe_allow_html=True)

        button_col_1, button_col_2 = st.columns([1, 1], gap="small")
        with button_col_1:
            update_outputs_clicked = st.form_submit_button("Run matcher")
        with button_col_2:
            reset_inputs_clicked = st.form_submit_button("Reset page")

if reset_inputs_clicked:
    for key in [
        "uploaded_file",
        "uploaded_classes_file",
        "use_all_ontology_classes",
        "uploaded_ontology_file",
        "uploaded_ontology_tags_file",
        "tfidf_corpus_mode",
    ]:
        st.session_state.pop(key, None)
    st.session_state["show_results"] = False
    st.rerun()

if update_outputs_clicked:
    st.session_state["show_results"] = True

if "show_results" not in st.session_state:
    st.session_state["show_results"] = False

if uploaded_file is not None:
    corpus_text = uploaded_file.read().decode("utf-8", errors="replace")
    corpus_source = f"Loaded uploaded corpus file: {uploaded_file.name}"
else:
    corpus_text = sample_text
    corpus_source = "Using the bundled sample corpus as a placeholder."

if uploaded_classes_file is not None:
    classes_of_interest = uploaded_classes_file.read().decode("utf-8", errors="replace")
    classes_source = f"Loaded uploaded words file: {uploaded_classes_file.name}"
else:
    classes_of_interest = load_file_text(DEFAULT_CLASSES_PATH)
    classes_source = "Using the bundled words-of-interest sample as a placeholder."

if use_all_ontology_classes:
    classes_of_interest = ""
    classes_source = "Using all classes from the ontology."

if uploaded_ontology_file is not None:
    ontology_text = uploaded_ontology_file.read().decode("utf-8", errors="replace")
    ontology_source = f"Loaded uploaded ontology file: {uploaded_ontology_file.name}"
else:
    #ontology_source = f"Using the bundled ontology placeholder: {DEFAULT_ONTOLOGY_PATH.name}"
    ontology_source = f"Using the bundled ontology as a placeholder."

if uploaded_ontology_tags_file is not None:
    ontology_tags_text = uploaded_ontology_tags_file.read().decode("utf-8", errors="replace")
    ontology_tags_source = f"Loaded uploaded ontology tags file: {uploaded_ontology_tags_file.name}"
else:
    ontology_tags_text = load_file_text(DEFAULT_ONTOLOGY_TAGS_PATH)
    ontology_tags_source = "Using the bundled ontology tags as a placeholder."

corpus_lines = [line.strip() for line in corpus_text.splitlines() if line.strip()]
corpus_line_count = len(corpus_lines)
corpus_average_word_count = 0.0
if corpus_lines:
    corpus_average_word_count = sum(len(line.split()) for line in corpus_lines) / len(corpus_lines)

corpus_status = (
    f"{corpus_source}\n"
    f"Corpus line count:\t{corpus_line_count}\n"
    f"Average word count in corpus:\t{corpus_average_word_count:.1f}"
)

classes_status = classes_source

ontology_tag_options = [line.strip() for line in ontology_tags_text.splitlines() if line.strip()]
ontology_tags_status = (
    f"{ontology_tags_source}\n"
    #f"Ontology tags line count:\t{len(ontology_tag_options)}"
)

show_results = st.session_state.get("show_results", False)

if show_results:
    progress_placeholder = st.empty()

    progress_placeholder.progress(0, text="Preparing inputs...")

    progress_placeholder.progress(15, text="Parsing ontology annotations...")
    ontology_classes = extract_classes_with_annotations(
        ontology_text,
        classes_of_interest,
        ontology_tag_options,
    )
    classes_status = (
        f"{classes_source}\n"
        f"Words of interest count:\t{len(ontology_classes)}"
    )

    requested_lines = []
    if ontology_classes:
        for word, annotations in ontology_classes.items():
            requested_lines.append(word)
            for annotation_tag in ontology_tag_options:
                if annotation_tag in annotations:
                    requested_lines.extend(annotations[annotation_tag])

        seen = set()
        unique_requested_lines = []
        for line in requested_lines:
            if line not in seen:
                seen.add(line)
                unique_requested_lines.append(line)
    else:
        unique_requested_lines = []

    progress_placeholder.progress(35, text="Building highlighted corpus output...")
    highlighted_corpus_data = build_highlighted_corpus_data(corpus_text, unique_requested_lines)
    highlighted_corpus_html = highlighted_corpus_data["html"]

    progress_placeholder.progress(55, text="Building class/synonym export...")
    class_synonym_match_rows = build_class_synonym_match_rows(
        corpus_text,
        ontology_classes,
        include_unmatched=not use_all_ontology_classes,
    )
    class_synonym_csv = build_class_synonym_csv(class_synonym_match_rows)
    matched_classes = {
        row["class"]
        for row in class_synonym_match_rows
        if row["synonym"] is None and row["sentence"]
    }
    matched_class_count = len(matched_classes)
    matched_expanded_terms = {
        row["class"] if row["synonym"] is None else row["synonym"]
        for row in class_synonym_match_rows
        if row["sentence"]
    }

    progress_placeholder.progress(70, text="Creating word clouds...")
    wordcloud_image = build_wordcloud_image(corpus_text)

    progress_placeholder.progress(85, text="Computing ranked TF-IDF terms...")
    ngram_values = parse_ngram_values(ngram_input)
    tfidf_corpus = corpus_text
    if tfidf_corpus_mode == "Corpus with classes and synonyms removed":
        tfidf_corpus = remove_class_synonyms_from_corpus(
            corpus_text,
            tuple(unique_requested_lines),
        )
    ranked_terms_df = build_tfidf_ranked_terms(tfidf_corpus, ngram_values)
    ranked_terms_tsv = ranked_terms_df.to_csv(index=False, sep="\t") if not ranked_terms_df.empty else ""

    progress_placeholder.progress(100, text="Finished — results are ready.")
else:
    ontology_classes = {}
    unique_requested_lines = []
    highlighted_corpus_data = {"html": "", "highlighted_lines": [], "non_highlighted_lines": []}
    highlighted_corpus_html = ""
    class_synonym_match_rows = []
    class_synonym_csv = ""
    matched_class_count = 0
    matched_expanded_terms = set()
    wordcloud_image = None
    ngram_values = []
    ranked_terms_df = pd.DataFrame()
    ranked_terms_tsv = ""

#########################

if st.session_state.get("show_results", False):

    with st.container(border=True):
        st.markdown("#### Match summary")
        summary_cols = st.columns(2)
        with summary_cols[0]:
            st.metric(
                "Words of interest matched",
                f"{matched_class_count}/{len(ontology_classes)}",
            )
        with summary_cols[1]:
            st.metric(
                "Expanded terms matched",
                f"{len(matched_expanded_terms)}/{len(unique_requested_lines)}",
            )
    
    st.markdown("### Phrase matching")
    if highlighted_corpus_html:
        with st.container():
            st.markdown(
                f"<div style='border: 1px solid #d0d7de; border-radius: 8px; padding: 0.75rem; background-color: #ffffff;'>{highlighted_corpus_html}</div>",
                unsafe_allow_html=True,
            )
    else:
        st.info("No matching classes or synonyms were found in the corpus.")

    st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)

    st.markdown("#### Download outputs")
    download_cols = st.columns(4)

    with download_cols[0]:
        st.download_button(label="Class & tags TSV", data=class_synonym_csv,
            file_name=get_timestamped_filename("class_synonym_matches", ".tsv"),
            mime="text/tab-separated-values", disabled=not class_synonym_match_rows,
        )

    with download_cols[1]:
        st.download_button(label="Matched lines only", data="\n".join(highlighted_corpus_data["highlighted_lines"]),
            file_name=get_timestamped_filename("highlighted_lines", ".txt"),
            mime="text/plain", disabled=not highlighted_corpus_data["highlighted_lines"],
        )

    with download_cols[2]:
        st.download_button(label="No matches", data="\n".join(highlighted_corpus_data["non_highlighted_lines"]),
            file_name=get_timestamped_filename("non_highlighted_lines", ".txt"),
            mime="text/plain", disabled=not highlighted_corpus_data["non_highlighted_lines"],
        )

    with download_cols[3]:
        st.download_button(label="Highlights as HTML", data=highlighted_corpus_html,
            file_name=get_timestamped_filename("cyannotator", ".html"),
            mime="text/html", disabled=not highlighted_corpus_html,
        )

    #########################
    st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)

    st.markdown("### Wordcloud")
    if wordcloud_image:
        #st.image(wordcloud_image, caption="Corpus word cloud (lemmatised, stopword-filtered)", use_container_width=True)
        st.image(wordcloud_image, use_container_width=True)
    else:
        st.info("No corpus content was available to generate a word cloud.")

    st.download_button(label="Download corpus word cloud", data=wordcloud_image,
        file_name=get_timestamped_filename("corpus_wordcloud", ".png"),
        mime="image/png", disabled=not wordcloud_image,
    )

    #########################
    st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)

    st.markdown("### Ranked terms (TF-IDF)")
    if ranked_terms_df.empty:
        st.info("No ranked terms were produced for the selected n-grams.")
    else:
        top_ranked_terms = ranked_terms_df.head(30).copy()
        max_ngram_value = max(ngram_values) if ngram_values else 1
        st.caption(f"Bar plot of normalised TF-IDF scores for n-grams up to {max_ngram_value}")
        st.bar_chart(top_ranked_terms.set_index("Word")["Normalised score"])
        #st.dataframe(top_ranked_terms, use_container_width=True)

        st.download_button(label="Download ranked TSV", data=ranked_terms_tsv,
            file_name=get_timestamped_filename("ranked_terms", ".tsv"),
            mime="text/tab-separated-values", disabled=ranked_terms_df.empty,
        )

    #########################
    st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)

    st.markdown("### Summaries")
    st.code(corpus_status)
    st.code(classes_status)
    st.code(f"Expanded phrases count:\t{len(unique_requested_lines)}")
    st.code(ontology_source)
    st.code(f"{ontology_tags_status}\nOntology tags:\t{', '.join([tag.strip() for tag in ontology_tags_text.splitlines() if tag.strip()])}")

    matched_ontology_tags = sorted({
        tag
        for annotations in ontology_classes.values()
        for tag in annotations.keys()
    })
    st.code(
        "Matched ontology tags:\t"
        + (", ".join(matched_ontology_tags) if matched_ontology_tags else "None")
    )

    #########################

#########################

# End
