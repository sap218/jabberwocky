An ontology is a knowledge representation framework that is machine readable.
It facilitates logical relationships between classes and allows us to standardise the formalised vocabulary within this domain.
The metadata contained within an ontology is valuable for research having shown to address the challenge presented by unstructured text.

Unstructured text can be processed, mined, and empowered by NLP tools, yet majority of tools are not designed to consider ontologies.

Jabberwocky allows users to easily manipulate ontologies with extraction and enhancements for conducting NLP tasks.
Here provides an explanation - with a working example - for the Jabberwocky toolkit. 

See the [Jabberwocky](https://github.com/sap218/jabberwocky) repository for code.

---

## Functionality


### bandersnatch
Extract metadata from ontology classes based on a list of tags.

Users should use ontologies that are in the `OWL` RDF/XML syntax.
(if not in this format, users can open ontology in [Protégé](https://protege.stanford.edu/) and export in correct format)

Metadata in ontologies are in various formats, below shows a list of tags as an example:
```
oboInOWL:hasExactSynonym
oboInOWL:hasRelatedSynonym
```

Words of interest (recommended to match ontology)
```
dragon
water
large
```

##### Output
`snatch_output.txt` will include the ontology classes and corresponding metadata based on chosen classes & tags.

If users have no words of interest, then the output will include **all ontology classes** but users will still need to include a list of tags.

---

### catch
Annotation of a corpus (unstructured text).

Words of interest - the `bandersnatch` output can be used here:
```
dragon
water
ocean
large
big
```
It is **important to note**: phrases work in Jabberwocky.

The corpus should be a `txt` with sentences/posts separated in new lines:
```
This is post 1 in a corpus
This is post 2

This is post 3 - as you can see there is a gap between post 2 and 3
This is post 4 - don't worry about extra whitespace as the code will drop "empty lines"
```

##### Output
`catch_output.txt` will include the posts that were annotated.
Users can choose output type: `grep` format or w/ corresponding tags.

Moreover, users can choose to export the posts that **weren't** annotated.

##### Plotting
Users can generate a wordcloud figure from the corpus.

---

### bite
Rank all words in a corpus in terms of importance (via the TF-IDF statistical technique).

Users can provide a list of words to remove from the corpus to avoid being weighted/measured - the `bandersnatch` output can be used here.

##### Output
`bite_output.tsv` is a dataframe with Word and Score.
Scores are the average TF-IDF values across posts, normalised for readability.
Moreover, normalised scores that are 0 are dropped.

Word | Raw score | Normalised score
------- | -----------
mega | 0.078 | 1.0
path | 0.06 | 0.719

##### Plotting
Users can export a bar plot of the top N ranked terms (default 30).

---

### arise
Updating ontology classes with new metadata. 

Users will provide a dataframe with three columns: the annotation, class (exact ontology match), and tag:
```
annotation	class	tag
sea	water	oboInOWL:hasExactSynonym
mega	large	oboInOWL:hasRelatedSynonym
https://pokemon.fandom.com/wiki/Types	type	oboInOWL:DbXref
```
This can be derived from the `bite` output (e.g. synonyms).

##### Output
`[ontology]_updated.owl` is the updated ontology.

---

### eyes
Plot an ontology in web or tree style.

By default, superclasses will have overlay text but users can choose whether to include for subclasses.

##### Output
`[ontology]_[plottype].png` is the updated ontology.

---

## Scenario

You have curated unstructured text: blog posts from a social media platform (with permission of course, in this example I invented these fake conversations).

Your aim is to text mine the corpus and only have posts covering a particular topic (or set of topics).
But you realise, although you know some words in this topic of yours, you may be missing related/broad synonyms.

This is where **ontologies are useful**. Ontologies are a controlled set of vocabulary with annotations.

With your words of interest (ontology classes) you can run `bandersnatch` to extract all synonyms.

With these classes and corresponding synonyms, you can annotate the corpus using `catch` - the `PhraseMatcher()` function[^spacy] tags each post in the corpus.

You've chosen to have two outputs: one with the annotated posts for downstream analysis.
The other you decided to investigate if there is anything valuable in the posts that weren't annotated.

You can proceed to use `bite` - investigating if there are any "important" terms.
The statistical TF-IDF method[^tfidf] is applied and all words are ranked in terms of importance.

With this `bite` output, you may have noticed new synonyms...
You can use `arise` to update your ontology classes with these new synonyms.

Finally, you may want to rerun `bandersnatch` to extract an updated list of key terms and then rerun `catch`.
This concludes the NLP workflow: you noticed the 2nd round of `catch` provides more data and so a more fruitful downstream analysis.

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
[^tfidf]: Term frequency inverse document frequency (TF-IDF)

***

End of page
