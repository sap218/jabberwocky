---
title: 'Annotating texts using ontologies and jabberwocky’s catch'
tags:
  - Python
  - Annotation
  - Ontologies
authors:
  - name: Samantha C Pendleton
    orcid: 0000-0002-6169-0135
    affiliation: "1, 2" # (Multiple affiliations must be quoted)
  - name: Author Without ORCID
    affiliation: 2
affiliations:
 - name: Institute of Cancer and Genomic Sciences, University of Birmingham, UK
   index: 1
 - name: Institution 2
   index: 2
date: 22 January 2020
bibliography: paper.bib

---

# Summary

Textual data is underused due to the complications when mining and parsing. In unstructured text, a researcher may use clinical terms to extract important sentences. However, one does not consider that term’s synonyms. Also, there is a lack of controlled vocabulary for various areas of interest.

Ontologies can help us as they formalise a domain of knowledge in a condensed manner, which we can then use to annotate textual data: ontologies use a clinical term and they have various types of synonyms, such as related, broad, and exact. There are a lack of tools which make ontologies useful, furthermore there are tools for text annotation but none use an ontology directly. Researchers are left playing with the XML of the ontology to extract labels as an exercise before they can conduct their annotation. 

There are some examples of tools for annotating text, such as “spaCy” [@Honnibal2017-dn], “tagtog” [@Cejuela2014-lv], and “Stanford CoreNLP” [@Manning2014-rt]. These tools cannot implement with ontologies, a user must provide a tags - in Stanford CoreNLP a user must provide a TSV of class and synonyms with their unique codes, meaning a lot of work for an individual beforehand.

There needed to be a better and easier method to annotate textual data. Especially for those not so familiar with this area of research. A toolkit created, jabberwocky, is aimed for the direct use of ontologies, helping a researcher to manipulate textual data, see https://github.com/sap218/jabberwocky.

With jabberwocky’s ``catch`` command, one can provide some keywords and it will search the chosen ontology for the classes and pairs them with their synonyms. The ``catch`` command then reads and cleans the users’ textual data, and filters the output on whether it finds a class or one of its synonyms in a value.

In the repository, https://github.com/sap218/jabberwocky-tests, I use an example for ``catch``. Out of 26 blog posts, jabberwockys’ ``catch`` returned 13 posts: the correct number. When using Stanford CoreNLP, it returned all 26 posts, however separated each post by their full-stop (``catch`` returns the full post) and so output was larger: 35. One would have to again play with some data in order to see the output properly - another limitation in this area. Compared to jabberwocky’s ``catch``, the command simply returns the texts which contains the label/phrase for individuals to then conduct their own further research on the text itself. 

This is straightforward but powerful, now one can effectively search their text data for some basic classes, but automatically search for all the implied meanings of those keywords too - returning a bigger collection of text to conduct research. The aim of jabberwocky for future development is to utilise the strengths of ontologies and text.

# References

