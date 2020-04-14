---
title: 'Jabberwocky: an ontology-aware toolkit for manipulating text'
tags:
  - Python
  - Ontologies
  - Text
authors:
  - name: Samantha C Pendleton
    orcid: 0000-0002-6169-0135
    affiliation: "1, 2" # (Multiple affiliations must be quoted)
  - name: Georgios V Gkoutos
    affiliation: "1, 2" # (Multiple affiliations must be quoted)
affiliations:
 - name: Institute of Cancer and Genomic Sciences, University of Birmingham, UK
   index: 1
 - name: University Hospitals Birmingham NHS Foundation Trust, UK
   index: 2
date: 25 February 2020
bibliography: paper.bib

---

# Summary

Unstructured textual data is underused, as gaining the key textual elements is complicated by a lack of structured terms. To extract valuable parts from a corpus, a user will need to use a combination of terms and their associated synonyms. For example, when analysing clinical documents, having knowledge of the synonyms for clinical terminology may increase the size of the corpus available for analysis. Additionally, the type of synonyms needed depends on the text, e.g. social media posts will need awareness of layman’s terms. One way to represent our knowledge of terms associated with a domain is to create an ontology. Ontologies allow us to formalise our knowledge of a domain in a condensed manner by using controlled terms, called classes [@Hoehndorf2015-qr]. Classes can be annotated with metadata, including synonyms. Ontologies can include relationships between terms, and annotations such as cross-references to other ontologies [@Hoehndorf2015-qr].

Clearly, ontologies are valuable for the analysis of textual data. Unfortunately, despite the existence of many well-established ontologies, such as the "Human Phenotype Ontology" [@Robinson2008-jh] and the "Disease Ontology" [@Schriml2012-qp], there remains a lack of tools that can take advantage of ontologies, especially for general text manipulation. Existing tools for annotating text, such as “spaCy” [@Honnibal2017-dn], “tagtog” [@Cejuela2014-lv], and “Stanford CoreNLP” [@Manning2014-rt] cannot interrogate text with an ontology directly, and require ontologies to be pre-processed into other formats (leaving the time-consuming task of extracting labels and tags from an ontology into a suitable intermediate format as an exercise for the end-user). These are specialist tools, returning all text in the document with every word tagged, as “noun”, “verb”, and other customised tags. There exists a niche for users who want to leverage an ontology to retrieve textual data from a corpus without having to perform any pre-processing, or parse away unwanted tags.

We introduce Jabberwocky, a Python-based [@Van_Rossum1995-ia], open-source toolkit (accessible via https://github.com/sap218/jabberwocky) that allows users to query text in an ontology-aware fashion, and to modify those ontologies based on their findings. For example, with Jabberwocky’s ``catch`` command, a user provides textual data, their chosen ontology and a set of classes from the ontology to use as search terms. Jabberwocky cleans the input text, collects the annotated synonyms for the user-specified target classes (using “Beautiful Soup” to read the ontology’s XML structure [@Richardson2007-ba]) and then returns the key elements (e.g. lines from a corpus) which match one of the target terms, or a synonym from the ontology. The ``catch`` command will help users retrieve more matches for their chosen terms from the corpus, without users having to explicitly define all the possible synonyms or alternative spellings beforehand.

Jabberwocky also helps ontology developers to iteratively improve their ontology. The ``bite`` command allows a user to provide textual data and rank the important terms: using the term frequency–inverse document frequency (tf-idf) method from “scikit-learn” [@Pedregosa2011-st], which calculates an importance metric for a term based on the frequency of its occurrence and the document size. Providing an ontology will exclude terms already described in the ontology, meaning the result of ``bite`` will be a CSV of candidate terms to potentially be added to the ontology, exported by “pandas” [@McKinney2010-xf]. Once an expert has reviewed the terms and associated them to a class in the ontology, Jabberwocky’s third command ``arise`` will annotate the classes in the ontology, adding the newly identified synonyms. Iteratively performing multiple rounds of ``bite`` and ``arise`` can help the development and maintenance of ontologies. A user could use the ``catch`` command to confirm the modified ontology now captures more of the corpus.

In Jabberwocky’s test repository (see Jabberwocky repo for further instructions), I show examples of each command separately. In the ‘process’ directory, I combine all three commands to demonstrate an example workflow. With 24 blog posts, the first use of ``catch`` returned 11 posts with the provided keywords. With ``bite`` I reviewed the CSV of ranked terms and curated new synonyms, simply by adding the corresponding class label from the ontology. I then used ``arise`` to add the identified synonyms into the ontology. With the second round of ``catch`` the number of posts returned for the same keywords increased to 16. This is a basic and straightforward example, but powerful. With Jabberwocky, users can efficiently search their text and gain more instances, providing new insight.

Jabberwocky leverages the strength of ontologies and text for a wide range of tasks. It will be useful to users who want to manipulate textual data using controlled vocabulary from ontologies.

# Acknowledgements

Project was funded by the Medical Research Council (MRC) (MR/S502431/1) & supported by Health Data Research (HDR) UK (HDRUK/CFC/01).

# References

