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
from io import StringIO
from pathlib import Path
import csv
import html
import re
import sys
import xml.etree.ElementTree as ET

import streamlit as st

APP_DIR = Path(__file__).resolve().parent
WORKSPACE_ROOT = APP_DIR.parent

if str(WORKSPACE_ROOT) not in sys.path:
    sys.path.insert(0, str(WORKSPACE_ROOT))

from highlevel import clean_lower_lemma, stopWords
DEFAULT_TEXT_PATH = WORKSPACE_ROOT / "test" / "CelestialObject" / "corpus" / "social_media_posts.txt"
DEFAULT_CLASSES_PATH = WORKSPACE_ROOT / "test" / "CelestialObject" / "corpus" / "classes_of_interest.txt"
#DEFAULT_CLASSES_PATH = WORKSPACE_ROOT / "02_snatch_metadata" / "test" / "20260122-203746_requested.txt"
DEFAULT_ONTOLOGY_TAGS_PATH = WORKSPACE_ROOT / "test" / "CelestialObject" / "corpus" / "ontology_tags.txt"
DEFAULT_ONTOLOGY_PATH = WORKSPACE_ROOT / "01_converter" / "test" / "20260122-203441_space.owl"

def load_file_text(file_path: Path) -> str:
    if file_path.exists():
        return file_path.read_text(encoding="utf-8")
    return ""


def get_timestamped_filename(prefix: str, suffix: str) -> str:
    timestamp = datetime.today().strftime("%Y%m%d-%H%M%S")
    return f"{timestamp}_{prefix}{suffix}"


def get_stopwords_list():
    stopword_level = stopWords[2]
    stopwords_lemma = []
    stopwords_list = []

    for word in stopword_level:
        stopwords_lemma.append(clean_lower_lemma(word, "stopwords", stopwords_list))

    stopwords_lemma_flat = [word for phrase in stopwords_lemma for word in phrase.split()]
    return sorted(set(filter(None, stopwords_lemma_flat)))


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


def build_class_synonym_match_rows(corpus_text: str, ontology_classes):
    if not corpus_text:
        return []

    stopwords_list = get_stopwords_list()
    rows = []

    for class_name, annotations in ontology_classes.items():
        class_match_sentence = None
        normalized_class = normalize_for_matching(class_name, stopwords_list, "wordsInterest")

        for line in corpus_text.splitlines():
            if not line.strip():
                continue
            normalized_line = normalize_for_matching(line, stopwords_list, "corpus")
            if contains_term_as_subsequence(normalized_line, normalized_class):
                class_match_sentence = line
                break

        rows.append(
            {
                "class": class_name,
                "synonym": None,
                "sentence": class_match_sentence,
            }
        )

        seen_synonyms = set()
        for annotation_tag in annotations:
            for synonym in annotations[annotation_tag]:
                if synonym in seen_synonyms:
                    continue
                seen_synonyms.add(synonym)

                normalized_synonym = normalize_for_matching(synonym, stopwords_list, "wordsInterest")
                match_sentence = None
                if normalized_synonym:
                    for line in corpus_text.splitlines():
                        if not line.strip():
                            continue
                        normalized_line = normalize_for_matching(line, stopwords_list, "corpus")
                        if contains_term_as_subsequence(normalized_line, normalized_synonym):
                            match_sentence = line
                            break

                rows.append(
                    {
                        "class": class_name,
                        "synonym": synonym,
                        "sentence": match_sentence,
                    }
                )

    return rows


def build_class_synonym_csv(rows):
    buffer = StringIO()
    writer = csv.writer(buffer)
    writer.writerow(["class", "synonym", "sentence"])

    for row in rows:
        writer.writerow([
            row["class"],
            row["synonym"] or "",
            row["sentence"] or "",
        ])

    return buffer.getvalue()


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
st.write("@ sap218")

#########################

sample_text = load_file_text(DEFAULT_TEXT_PATH)
classes_of_interest = load_file_text(DEFAULT_CLASSES_PATH)
ontology_tags_text = load_file_text(DEFAULT_ONTOLOGY_TAGS_PATH)
ontology_text = load_file_text(DEFAULT_ONTOLOGY_PATH)

#########################

with st.container(border=True):
    with st.form("input_form"):
        uploaded_file = st.file_uploader(
            "Upload your own corpus text file",
            type=["txt"],
            key="uploaded_file",
            help=(
                "If you do not upload a file, the app will use the bundled sample corpus as a placeholder. "
                f"Sample file: {DEFAULT_TEXT_PATH}"
            ),
        )

        uploaded_classes_file = st.file_uploader(
            "Upload your own words of interest file",
            type=["txt"],
            key="uploaded_classes_file",
            help=(
                "If you do not upload a file, the app will use the bundled words-of-interest sample as a placeholder. "
                f"Sample file: {DEFAULT_CLASSES_PATH}"
            ),
        )

        uploaded_ontology_file = st.file_uploader(
            "Upload your own ontology file",
            type=["owl"],
            key="uploaded_ontology_file",
            help=(
                "If you do not upload a file, the app will use the bundled ontology placeholder. "
                f"Sample file: {DEFAULT_ONTOLOGY_PATH}"
            ),
        )

        uploaded_ontology_tags_file = st.file_uploader(
            "Upload your own ontology tags file",
            type=["txt"],
            key="uploaded_ontology_tags_file",
            help=(
                "If you do not upload a file, the app will use the bundled ontology tags sample. "
                f"Sample file: {DEFAULT_ONTOLOGY_TAGS_PATH}"
            ),
        )

        button_col_1, button_col_2 = st.columns(2)
        with button_col_1:
            update_outputs_clicked = st.form_submit_button("Update outputs")
        with button_col_2:
            reset_inputs_clicked = st.form_submit_button("Reset page")

if reset_inputs_clicked:
    for key in [
        "uploaded_file",
        "uploaded_classes_file",
        "uploaded_ontology_file",
        "uploaded_ontology_tags_file",
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

if uploaded_ontology_file is not None:
    ontology_text = uploaded_ontology_file.read().decode("utf-8", errors="replace")
    ontology_source = f"Loaded uploaded ontology file: {uploaded_ontology_file.name}"
else:
    ontology_source = f"Using the bundled ontology placeholder: {DEFAULT_ONTOLOGY_PATH.name}"

if uploaded_ontology_tags_file is not None:
    ontology_tags_text = uploaded_ontology_tags_file.read().decode("utf-8", errors="replace")
    ontology_tags_source = f"Loaded uploaded ontology tags file: {uploaded_ontology_tags_file.name}"
else:
    ontology_tags_text = load_file_text(DEFAULT_ONTOLOGY_TAGS_PATH)
    ontology_tags_source = "Using the bundled ontology tags sample as a placeholder."

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

classes_lines = [line.strip() for line in classes_of_interest.splitlines() if line.strip()]
classes_line_count = len(classes_lines)

classes_status = (
    f"{classes_source}\n"
    f"Words line count:\t{classes_line_count}"
)

ontology_tag_options = [line.strip() for line in ontology_tags_text.splitlines() if line.strip()]
ontology_tags_status = (
    f"{ontology_tags_source}\n"
    f"Ontology tags line count:\t{len(ontology_tag_options)}"
)

summary_text = "No ontology classes were found for the selected ontology and annotation tags."

ontology_classes = extract_classes_with_annotations(
    ontology_text,
    classes_of_interest,
    ontology_tag_options,
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

    summary_text = "\n".join(unique_requested_lines).strip()
else:
    unique_requested_lines = []
    summary_text = "No ontology classes were found for the selected ontology and annotation tags."

highlighted_corpus_data = build_highlighted_corpus_data(corpus_text, unique_requested_lines)
highlighted_corpus_html = highlighted_corpus_data["html"]
class_synonym_match_rows = build_class_synonym_match_rows(corpus_text, ontology_classes)
class_synonym_csv = build_class_synonym_csv(class_synonym_match_rows)

#########################

if st.session_state.get("show_results", False):
    st.write("---")

    st.markdown("### Corpus matches from classes and synonyms")
    if highlighted_corpus_html:
        st.markdown(highlighted_corpus_html, unsafe_allow_html=True)
    else:
        st.info("No matching classes or synonyms were found in the corpus.")

    st.markdown("### Download outputs")
    download_cols = st.columns(4)

    with download_cols[0]:
        st.download_button(
            label="Download highlighted lines",
            data="\n".join(highlighted_corpus_data["highlighted_lines"]),
            file_name=get_timestamped_filename("highlighted_lines", ".txt"),
            mime="text/plain",
            disabled=not highlighted_corpus_data["highlighted_lines"],
        )

    with download_cols[1]:
        st.download_button(
            label="Download non-highlighted lines",
            data="\n".join(highlighted_corpus_data["non_highlighted_lines"]),
            file_name=get_timestamped_filename("non_highlighted_lines", ".txt"),
            mime="text/plain",
            disabled=not highlighted_corpus_data["non_highlighted_lines"],
        )

    with download_cols[2]:
        st.download_button(
            label="Download highlighted HTML",
            data=highlighted_corpus_html,
            file_name=get_timestamped_filename("cyannotator", ".html"),
            mime="text/html",
            disabled=not highlighted_corpus_html,
        )

    with download_cols[3]:
        st.download_button(
            label="Download class/synonym CSV",
            data=class_synonym_csv,
            file_name=get_timestamped_filename("class_synonym_matches", ".csv"),
            mime="text/csv",
            disabled=not class_synonym_match_rows,
        )

    
    st.code(corpus_status)
    '''
    st.text_area("Corpus text", value=corpus_text, height=320, key="corpus_text",)
    '''

    st.code(classes_status)
    '''
    st.text_area("Words of interest", value=classes_of_interest, height=140, key="classes_of_interest",
        help=("This is pre-populated from the bundled words-of-interest sample. "
        f"Sample file: {DEFAULT_CLASSES_PATH}"),
    )
    '''

    st.code(ontology_source)
    st.code(ontology_tags_status)
    st.write("Ontology tags")
    st.code(ontology_tags_text)

    '''
    st.text_area("Classes and synonyms", value=summary_text, height=220, key="ontology_summary",)
    '''
    
    #########################

    st.write("---")

    #########################





#########################

# End
