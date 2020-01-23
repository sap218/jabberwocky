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

Unstructured textual data is underused. Gaining the key textual elements can be complicated due to limited terms being used. There are clinical terms one can use, however synonyms expand a search horizon: exact synonyms could be other clinical terms and related synonyms would include patient-preferred terms (natural language). To extract important text from a corpus, a user will need to use a combination of terms and synonyms for a larger output.

In order to use a collection of texts, firstly one would have to mine and parse into an appropriate format. Many users may not have these abilities/skills: using methods to extract and organise textual data in order to be used appropriately. 

Once in an appropriate format, a user can then try to extract the important parts - a user may use only one known term. On many occasions one does not consider that term’s synonyms. 
There is also a gap in this area: there is a lack of controlled vocabulary for various areas of interest and a lack of synonyms to expand those terms.

Ontologies can help us as they formalise a domain of knowledge in a condensed manner [@Hoehndorf2015-qr]. They have terms, which are classes, that can be annotated with synonyms: related, exact, narrow, and broad. There are various ontologies which exist and all have their own domains of interest, many are biomedical, such as the Human Phenotype Ontology [@Robinson2008-jh] and the Disease Ontology [@Schriml2012-qp]. Ontologies also include relationships (plus logical axioms) and additional annotations, such as cross-referencing to other biomedical ontologies [@Hoehndorf2015-qr].

Biomedical ontologies will be a collection of clinical terms with synonyms. This collection can be used to annotate textual data. But there are a lack of tools which make ontologies useful, furthermore there are tools for text annotation but none use an ontology directly. Users are left playing with the XML of the ontology to extract labels as an exercise before they can conduct their annotation - many users may not have these abilities for this extraction task. 

There are some examples of tools for annotating text, such as “spaCy” [@Honnibal2017-dn], “tagtog” [@Cejuela2014-lv], and “Stanford CoreNLP” [@Manning2014-rt]. These tools cannot be implemented with ontologies - these tools usually return all text with each word tagged, such as “noun” or “verb” - rather than looking for particular terms, some other tools will allow a user to provide tags via playing with the ontology XML - still providing an output of all text rather than displaying the important texts.

There needed to be a better and easier method to annotate textual data and for the extraction of important texts. Especially for those not so familiar with this area of research or will the desired skill set for textual manipulation.

A toolkit created, jabberwocky, is aimed for the direct use of ontologies, helping a user to manipulate textual data, see https://github.com/sap218/jabberwocky. Thus far, it only includes a single command, ``catch`` however in future the plan would include additional commands for a wide range of tasks useful for users who need to use textual data and controlled vocabulary via ontologies.

With jabberwocky’s ``catch`` command, one can provide some keywords and a chosen ontology. The script will search the ontology for the keyword and class match to pair them with their synonyms. The ``catch`` command then reads and cleans the users’ textual data, filtering the output on whether it finds a class or one of its synonyms in a value.

In the repository, https://github.com/sap218/jabberwocky-tests, I use an example for ``catch``. Out of 26 blog posts, jabberwockys’ ``catch`` returned 13 posts: the correct number. 
When using Stanford CoreNLP, first I had to play with an ontology in order to gain each class, synonyms, and their ID codes. Stanford CoreNLP actually returned 35 posts (more than the original 26), this is because it separated each post by their full-stop (``catch`` returns the full post) and so output was larger, essentially acting as if each sentence was a separate blog post. One would have to again play with some data in order to see the output properly since they structure it in a particular way, again showing the limitations in this area. Compared to jabberwocky’s ``catch``, the command simply returns the texts which contains the label/phrase for individuals to then conduct their own further research on the text itself. 

This is straightforward but powerful, now one can effectively search their text data for some basic classes, but automatically search for all the implied meanings of those keywords too - returning a bigger collection of text to conduct research. This larger output of text can provide further insight of a user’s investigation: potentially revealing subgroups.

The aim of the toolkit, jabberwocky, is to utilise the strengths of ontologies and text. Thus far with one command ``catch`` we have made this process far less complicated.

# References

