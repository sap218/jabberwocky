# Jabberwocky

[![DOI](https://joss.theoj.org/papers/10.21105/joss.02168/status.svg)](https://doi.org/10.21105/joss.02168) 

Jabberwocky is a toolkit for NLP and **ontologies**. Since we all know ontologies are *nonsense*.

## Functionality

Read the [documentation](https://sap218.github.io/jabberwocky/) for more detail.

script | description
------- | -----------
`bandersnatch` | extract metadata from ontology classes
`catch` | annotate corpus with key terms & generate wordcloud
`bite`  | rank terms in order of importance & bar plot
`arise` | update ontology with new metadata
`eyes` | plot an ontology via web or tree format

When combining these Jabberwocky functions, users can create an NLP workflow.

![workflow](/docs/workflow.png)

## Running
Within each directory, there is a file `params_*.py` which users can edit.
This means users shouldn't need to edit the main/primary script.

Check the individual `READMEs` for parameter information.

#### Prerequisites
Check [`requirements.py`](https://github.com/sap218/jabberwocky/blob/master/requirements.py) for a list of packages and versions.

## Changelog
Information on versions, see the [**Changelog**](https://github.com/sap218/jabberwocky/blob/master/changelog.md) (ordered by newest first).

## Contributing
Please read the [**Contributing Guidelines**](https://github.com/sap218/jabberwocky/blob/master/contributing.md).

- [@majensen](https://github.com/majensen) set up automated testing w/ `pytest` in v1.0 - see [pull request #13](https://github.com/sap218/jabberwocky/pull/13) for more details

## License 
The [license](https://github.com/sap218/jabberwocky/blob/master/LICENSE) is **MIT** and so users only need to cite (below) if using.

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

The poem, Jabberwocky, written by Lewis Carrol, is described as a "nonsense" poem :dragon:

***

End of page
