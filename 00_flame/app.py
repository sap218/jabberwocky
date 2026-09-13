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

from pathlib import Path
import re
import xml.etree.ElementTree as ET

import streamlit as st

APP_DIR = Path(__file__).resolve().parent
WORKSPACE_ROOT = APP_DIR.parent
DEFAULT_TEXT_PATH = WORKSPACE_ROOT / "test" / "CelestialObject" / "corpus" / "social_media_posts.txt"
DEFAULT_CLASSES_PATH = WORKSPACE_ROOT / "test" / "CelestialObject" / "corpus" / "classes_of_interest.txt"
#DEFAULT_CLASSES_PATH = WORKSPACE_ROOT / "02_snatch_metadata" / "test" / "20260122-203746_requested.txt"
DEFAULT_ONTOLOGY_TAGS_PATH = WORKSPACE_ROOT / "test" / "CelestialObject" / "corpus" / "ontology_tags.txt"
DEFAULT_ONTOLOGY_PATH = WORKSPACE_ROOT / "01_converter" / "test" / "20260122-203441_space.owl"

def load_file_text(file_path: Path) -> str:
    if file_path.exists():
        return file_path.read_text(encoding="utf-8")
    return ""


def extract_annotation_tags_from_ontology(ontology_text: str, fallback_tags_text: str = ""):
    if ontology_text:
        try:
            root = ET.fromstring(ontology_text)
        except ET.ParseError:
            root = None

        if root is not None:
            namespace_map = {}
            for match in re.finditer(r'xmlns(?::([A-Za-z0-9_\-]+))?="([^"]+)"', ontology_text):
                prefix, uri = match.groups()
                if prefix and uri:
                    namespace_map[uri] = prefix

            tags = []
            seen = set()
            for concept in root.iter():
                if concept.tag.split("}")[-1] != "Class":
                    continue

                for child in concept:
                    local_name = child.tag.split("}")[-1]
                    if local_name in {"label", "subClassOf", "type", "Class"}:
                        continue
                    if not child.text or not child.text.strip():
                        continue

                    uri = child.tag[1:].split("}", 1)[0] if child.tag.startswith("{") else ""
                    if uri in namespace_map:
                        tag_name = f"{namespace_map[uri]}:{local_name}"
                    else:
                        tag_name = local_name

                    if tag_name not in seen:
                        tags.append(tag_name)
                        seen.add(tag_name)

            if tags:
                return tags

    fallback_tags = [line.strip() for line in fallback_tags_text.splitlines() if line.strip()]
    return fallback_tags


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
            help=(
                "If you do not upload a file, the app will use the bundled sample corpus as a placeholder. "
                f"Sample file: {DEFAULT_TEXT_PATH}"
            ),
        )

        uploaded_classes_file = st.file_uploader(
            "Upload your own words of interest file",
            type=["txt"],
            help=(
                "If you do not upload a file, the app will use the bundled words-of-interest sample as a placeholder. "
                f"Sample file: {DEFAULT_CLASSES_PATH}"
            ),
        )

        uploaded_ontology_file = st.file_uploader(
            "Upload your own ontology file",
            type=["owl"],
            help=(
                "If you do not upload a file, the app will use the bundled ontology placeholder. "
                f"Sample file: {DEFAULT_ONTOLOGY_PATH}"
            ),
        )

        uploaded_ontology_tags_file = st.file_uploader(
            "Upload your own ontology tags file",
            type=["txt"],
            help=(
                "If you do not upload a file, the app will use the bundled ontology tags sample. "
                f"Sample file: {DEFAULT_ONTOLOGY_TAGS_PATH}"
            ),
        )

        update_outputs_clicked = st.form_submit_button("Update outputs")

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
    summary_text = "No ontology classes were found for the selected ontology and annotation tags."

#########################

st.write("---")

#########################

st.code(corpus_status)
st.text_area(
    "Corpus text",
    value=corpus_text,
    height=320,
    key="corpus_text",
)

st.write("---")

st.code(classes_status)
st.text_area(
    "Words of interest",
    value=classes_of_interest,
    height=140,
    key="classes_of_interest",
    help=(
        "This is pre-populated from the bundled words-of-interest sample. "
        f"Sample file: {DEFAULT_CLASSES_PATH}"
    ),
)

st.write("---")

st.code(ontology_source)
st.code(ontology_tags_status)
st.text_area(
    "Ontology tags",
    value=ontology_tags_text,
    height=140,
    key="ontology_tags_text",
    help=(
        "This is the list of ontology annotation tags used to build the class/synonym summary. "
        f"Sample file: {DEFAULT_ONTOLOGY_TAGS_PATH}"
    ),
)

st.write("---")

st.text_area(
    "Classes and synonyms",
    value=summary_text,
    height=220,
    key="ontology_summary",
)

#########################

st.write("---")

#########################





#########################

# End
