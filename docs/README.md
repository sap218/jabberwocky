An ontology is a knowledge representation framework that is machine readable.
It facilitates logical relationships between classes and allows us to standardise the formalised vocabulary within this domain.
The metadata contained within an ontology is valuable for research having shown to address the challenge presented by unstructured text.

Unstructured text can be processed, mined, and empowered by NLP tools, yet majority of tools aren't designed to consider ontologies.

Jabberwocky allows users to easily manipulate ontologies with extraction and enhancements for conducting NLP tasks.
Here provides an explanation - with a working example - for the Jabberwocky toolkit. 

See the [Jabberwocky](https://github.com/sap218/jabberwocky) repository for code.

## Functionality

---

### bandersnatch
Extract annotations from ontology concepts based on a list of annotation tags.

Users should use ontologies in the `OWL` RDF/XML syntax.
(if not in this format, users can open ontology in [Protégé](https://protege.stanford.edu/) and export in correct format)

Annotations in ontologies are in various formats, below shows a list of tags as an example:
```
oboInOWL:hasExactSynonym
oboInOWL:hasRelatedSynonym
```

Words of interest (via ontology)
```
dragon
water
large
```

##### Output
`snatch_output.txt` will include all ontology classes (from words of interest) and their annotations.

If users have no words of interest then the output will include **annotations of all ontology classes**.

---

### catch
Annotation of a corpus.

Words/Phrases of interest - the `bandersnatch` output can be used here:
```
dragon
water
ocean
large
big
```

The corpus should be a `txt` with new lines to separate each post:
```
This is post 1 in a corpus
This is post 2

As you can see there is a gap between post 3 and 2 but the code drops "empty lines"
```

##### Output
`catch_output.txt` will include the posts that were annotated with a word/phrase of interest.

---

### bite
Rank all words in a corpus in terms of importance (via TF-IDF).

Users can provide a list words to remove from the text to avoid being weighted in the statistical algorithm - the `bandersnatch` output can be used here.

##### Output
`bite_output.tsv` is a dataframe with Word and Score. Scores are average TF-IDF rankings across posts then normalised for readability.

```
Word	Score
pokemon	1.0
catch	0.7241347494806625
path	0.6806667025792819
evolve	0.4746729555593563
```

---

### arise
Enhances ontology classes with new annotations - these new annotations can be derived from the `bite` output (synonyms).

A dataframe should be provided with three columns, the annotation (e.g. synonym), class (exact match in ontology), and tag:
```
annotation	class	tag
sea	water	oboInOWL:hasExactSynonym
mega	large	oboInOWL:hasRelatedSynonym
https://pokemon.fandom.com/wiki/Types	type	oboInOWL:DbXref
```

##### Output
`[ontology]_updated.owl` is the updated ontology.

---

## Scenario

You have curated unstructured text: blog posts from a social media platform (with permission of course, in this example I invented these fake conversations).

Your aim is to text mine the corpus and only have posts covering a particular topic (or set of topics).
But you realise, you know some words in this topic of yours but you may be missing related/broad synonyms.

This is where **ontologies are useful**. Ontologies are a controlled set of vocabulary with annotations.

With your words of interest (ontology classes) you can run `bandersnatch` to extract all synonyms.

With or without the additional synonyms, you can continue onto `catch` where a `PhraseMatcher()` [^spacy] tags each post in the corpus.
Now you can continue to conduct your analysis on the output.

Now you wonder what words are "important" in the corpus, here you can use `bite`.
The statistical TF-IDF [^tfidf] is applied and all words are ranked in terms of importance.

With this `bite` output, you may have noticed new synonyms...
You can use `arise` to update your ontology classes with these new synonyms.

Finally, you may want to rerun `bandersnatch` and `catch` to redo the curation of class/synonyms and text mine the corpus with this updated list of words of interest.
This concludes the NLP workflow and so your research with the `catch` (2nd round) is more fruitful.

---

## Conclusion

This work was published in [JOSS](https://doi.org/10.21105/joss.02168), you can cite here:

```
@article{Pendleton2020,
  doi = {10.21105/joss.02168},
  url = {https://doi.org/10.21105/joss.02168},
  year = {2020},
  publisher = {The Open Journal},
  volume = {5},
  number = {51},
  pages = {2168},
  author = {Samantha C. Pendleton and Georgios V. Gkoutos},
  title = {Jabberwocky: an ontology-aware toolkit for manipulating text},
  journal = {Journal of Open Source Software}
}
```

This repository was inspired by (and the inspiration of) the [OcIMIDo](https://doi.org/10.1016/j.compbiomed.2021.104542) project.

[^spacy]: using [spaCy](https://spacy.io/api/phrasematcher)
[^tfidf]: Term frequency inverse document frequency

***

End of page
