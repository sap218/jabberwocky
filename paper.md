---
title: 'Annotating text with ontologies using jabberwocky’s catch'
tags:
  - Python
  - Annotation
  - Ontologies
authors:
  - name: Samantha C Pendleton
    orcid: 0000-0002-6169-0135
    affiliation: 1 # (Multiple affiliations must be quoted)
affiliations:
 - name: Institute of Cancer and Genomic Sciences, University of Birmingham, UK
   index: 1
date: 22 January 2020
bibliography: paper.bib

---

# Summary

A toolkit created, jabberwocky, is aimed for the direct use of ontologies, helping a user to manipulate textual data, see https://github.com/sap218/jabberwocky. 

With jabberwocky’s ``catch`` command, a user can provide textual data, keywords, and a chosen ontology. The script will search the ontology using the keywords, with each keyword it will match it with a class: the class is then paired with their synonyms. The ``catch`` command will also read and clean the input textual data, then filtering the output on whether it finds a class or one of its synonyms in a value.

Unstructured textual data is underused. Gaining the key textual elements or values can be complicated due to limited terms being used. There are clinical terms a user can use, however synonyms expand a search horizon: exact synonyms could be other clinical terms and related synonyms would include patient-preferred terms (natural-language). To extract important text from a corpus, a user will need to use a combination of terms and synonyms for a larger output - the types of syonyons a user will need depends on their textual data, e.g. individual blogs may need natural-language synonyms. 

In order to use a collection of texts, firstly one would have to manually mine and parse into an appropriate format or use methods available, either option can take time and practical ability. Once extracted and organised in an appropriate format, a user can then try to extract the key elements. To extract the key elements a user may only know a single term and does not consider the synonyms: using a single term, a user could potentially use ``grep`` however when a multitude of terms are being used, including synonyms, the task becomes more complicated and time-consuming.

Ontologies are constantly being developed as they formalise a domain of knowledge in a condensed manner [@Hoehndorf2015-qr]. They have terms, which are classes, that can be annotated with synonyms: related, exact, narrow, and broad. There are various ontologies which exist and all have their own domains of interest, many are biomedical, such as the Human Phenotype Ontology [@Robinson2008-jh] and the Disease Ontology [@Schriml2012-qp]. Ontologies also include relationships (plus logical axioms) and additional annotations, such as cross-referencing to other biomedical ontologies [@Hoehndorf2015-qr].

Biomedical ontologies’ classes are a collection of clinical terms, with additional clinical terms as synonyms: some biomedical ontologies have natural-language terms as synonyms too. Ontologies and their classes/synonyms can be used to annotate textual data. But there are a lack of tools which make ontologies useful, furthermore there are tools for text annotation but none use an ontology directly. 

There are some examples of tools for annotating text, such as “spaCy” [@Honnibal2017-dn], “tagtog” [@Cejuela2014-lv], and “Stanford CoreNLP” [@Manning2014-rt]. These tools cannot be implemented with ontologies - they usually return all text with each word tagged, such as “noun” or “verb” - rather than looking and returning key elements, some other tools will allow a user to provide tags via playing with the ontology XML - still providing an output of all text rather than displaying the important texts. Looking into the XML on an ontology to extract labels and tags can be a time consuming exercise.

There needed to be a better and an easier method to retrieve key textual data from a corpus. Especially for those not so familiar with this area of research or will the desired skill set for textual manipulation.

In the repository, https://github.com/sap218/jabberwocky-tests, I use an example for ``catch``. Out of the 26 example blog posts, jabberwockys’ ``catch`` returned 13 posts using the keywords I provided: the correct number. Using ``grep`` and only a single word, such as “generation 1”, the output was 1, as expected. When using the ontology and the keyword, the output increases to 3. 

When using Stanford CoreNLP, first I had to play with an ontology in order to gain each class, synonyms, and their ID codes. Stanford CoreNLP actually returned 35 posts (more than the original 26), this is because it separated each post by their full-stop (``catch`` returns the full post) and so output was larger, essentially acting as if each sentence was a separate blog post. One would have to again play with data: in order to see the output properly since Stanford CoreNLP structures the output in a particular way: again revealing the limitations in this area. Compared to jabberwocky’s ``catch``, the command simply returns the texts which contains the label/phrase for individuals to then conduct their own further research on the text itself. The ``catch`` command returns the text in the terminal which a user could use ``>`` to redirect into a file. 

This is straightforward but powerful, now one can effectively search their text corpus using keywords/classes from an ontology, but the script automatically searches for all the implied meanings of those keywords too - returning a bigger collection of text to conduct research. This larger output of text can provide further insight of a user’s investigation: potentially revealing subgroups.

The aim of the toolkit, jabberwocky, is to utilise the strengths of ontologies and text. Thus far with one command ``catch`` we have made this process far less complicated. A future expansion would include additional commands for a wide range of tasks useful for users who need to use textual data and controlled vocabulary via ontologies.

# Acknowledgements

Project was funded by the Medical Research Council (MRC) (MR/S502431/1).

# References

