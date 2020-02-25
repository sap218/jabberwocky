---
title: 'jabberwocky: a toolkit for ontologies and text'
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

A toolkit created, jabberwocky, is aimed for the direct use of ontologies, helping a user to manipulate textual data, see https://github.com/sap218/jabberwocky. 

Unstructured textual data is underused. Gaining the key textual elements or values can be complicated as terms can be limited. There are clinical terms, however synonyms expand a search horizon. To extract important text from a corpus, a user will need to use a combination of terms and synonyms for a larger output. Moreover the type of syonyons needed depends on the text, e.g. social media posts may need layman’s terms. Text processing involves practical ability: there are methods available however when a multitude of terms are being used, including synonyms, the task becomes more complicated and time-consuming.

Ontologies are constantly being developed as they formalise a domain of knowledge in a condensed manner [@Hoehndorf2015-qr], they contain a collection of controlled terms. Ontologies have classes (clinical terms), that can be annotated with synonyms: related, exact, narrow, and broad. There are various existing ontologies, all having their own areas of interest, such as the Human Phenotype Ontology [@Robinson2008-jh] and the Disease Ontology [@Schriml2012-qp]. Ontologies also include relationships (plus logic) and additional annotations, such as cross-referencing to other ontologies [@Hoehndorf2015-qr].
Biomedical ontologies’ classes are a collection of clinical terms, with additional clinical terms as synonyms: some ontologies have layman’s terms as included, however not as synonyms. Ontologies and their classes/synonyms can be used to annotate textual data, but there are a lack of tools which make ontologies useful, furthermore there are tools for text annotation but none use an ontology directly. 

There are some examples of tools for annotating text, such as “spaCy” [@Honnibal2017-dn], “tagtog” [@Cejuela2014-lv], and “Stanford CoreNLP” [@Manning2014-rt]. These tools cannot be implemented with ontologies and rather require other formats (looking into the XML of an ontology to extract labels and tags can be a time consuming exercise). They return all text with each word tagged, such as “noun” or “verb”, or customised tags - rather than only returning key elements in a useful format. There needed to be a better and an easier method to retrieve key textual data from a corpus, especially for those who don’t require tags. 

With jabberwocky’s ``catch`` command, a user can provide textual data and a chosen ontology. The script will take in a JSON formatted (or TXT) file and clean them. Using the cleaned textual data, ``catch`` returns the key elements (e.g. lines from a corpus) which contain a class term or synonym from the ontology. Adding a set of keywords, ``catch`` will output only those key elements, providing a more precise search.

The ``bite`` command allows a user to provide textual data and observe the important terms: via the tf-idf method, which measures the information in a document and balancing it based on the size - providing a CSV output for users to observe the terms and rankings from their data. 

The third command, ``arise``, lets you add synonyms into an ontology. A user’s CSV of synonyms may be influenced by the ``bite`` tf-idf output.
A user could then re-do the ``bite`` step, this time using the ontology to remove classes/synonyms in order for terms to be re-weighed. 

Finally, a final ``catch`` can be performed and a user will see a bigger output. 

In the repository, https://github.com/sap218/jabberwocky-tests, I show examples of each command separately, however in the ‘process’ directory, I combine all three commands as a workflow. With 24 blog posts, the first use of ``catch`` returned 11 posts with the provided keywords. With ``bite`` I saw a collection of ranked terms and extracted those to put in a CSV file, which I then used ``arise`` to put into the ontology. With the second round of ``catch`` the output increased to 16,  (with keywords). 

This is a basic and straightforward example, but powerful. Now individuals can effectively gain a larger output of text, which can provide further insight of a user’s investigation: potentially revealing subgroups.

The aim of the toolkit, jabberwocky, is to utilise the strengths of ontologies and text for a wide range of tasks useful for users who need to use textual data and controlled vocabulary via ontologies.

# Acknowledgements

Project was funded by the Medical Research Council (MRC) (MR/S502431/1) & supported by Health Data Research (HDR) UK (HDRUK/CFC/01).

# References

