# Jabberwocky

[![DOI](https://joss.theoj.org/papers/10.21105/joss.02168/status.svg)](https://doi.org/10.21105/joss.02168) 

Jabberwocky is a toolkit for NLP and **ontologies**. Since we all know ontologies are *nonsense*.

## Functionality

script | description
------- | -----------
`bandersnatch` | extract annotations from an ontology (`OWL` RDF/XML syntax)
`catch` | text mining (grep) a corpus using key words/phrases
`bite`  | TF-IDF for ranking important terms from corpus
`arise` | adding / updating ontology concepts with new annotations

When combining these functions, users can create an NLP workflow.

![workflow](/docs/workflow.png)

#### Prerequisites

Check [`requirements.py`](https://github.com/sap218/jabberwocky/blob/master/requirements.py) for a list of packages and versions.

#### AOB

- Check the [**Changelog**](https://github.com/sap218/jabberwocky/blob/master/changelog.md) for version information
- [License](https://github.com/sap218/jabberwocky/blob/master/LICENSE) is **MIT**
- The poem, Jabberwocky, written by Lewis Carrol, is described as a "nonsense" poem :dragon:

## Contributing

Please read the [**Contributing Guidelines**](https://github.com/sap218/jabberwocky/blob/master/contributing.md).

- [@majensen](https://github.com/majensen) set up automated testing w/ `pytest` in v1.0 - see [pull request #13](https://github.com/sap218/jabberwocky/pull/13) for more details

## Citing

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

***

End of page
