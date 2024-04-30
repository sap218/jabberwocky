# Jabberwocky

[![DOI](https://joss.theoj.org/papers/10.21105/joss.02168/status.svg)](https://doi.org/10.21105/joss.02168) [![DOI](https://zenodo.org/badge/227571502.svg)](https://zenodo.org/badge/latestdoi/227571502) 

Jabberwocky is a toolkit for **ontologies**. Since we all know ontologies are "*nonsense*". 

Don't hesitate to create an [`Issue`](https://github.com/sap218/jabberwocky/issues) - please read the [**guidelines**](https://github.com/sap218/jabberwocky/blob/master/CONTRIBUTING.md) first.

#### Version
See `setup.py` in your local copy for version number | or `Releases`:
* **v1.0.0.0** [29/06/2020] - version presented in **JOSS** paper
* **v2.0.0.0** [10/05/2021]
     - includes `spacy PhraseMatcher`
     - own synonym tags
     - plot output for tf-idf
* **v2.1.0.0** [2024]
     - Revamp

#### Install
```
$ git clone https://github.com/sap218/jabberwocky
$ cd jabberwocky
$ python setup.py install --user
```
**note**: if you are using a virtual environment you can avoid `--user`

##### Prerequisites
```
$ pip install click BeautifulSoup4 scikit-learn pandas lxml pytest spacy matplotlib
```
or **after installing**, use the `requirements.txt` file:
```
$ pip install -r requirements.txt
```

### Functions

command | description
------- | -----------
`bandersnatch` | extract synonyms from an RDF/XML syntax `OWL` ontology
`catch` | extract elements / sentences of text using key words
`bite`  | run statistical tf-idf for important words from text
`arise` | adding / updating new synonyms to an ontology

#### Ontology formats
`jabberwocky` works with the `OWL` ontology format: `RDF/XML`.

Well-known biomedical ontologies such as `doid.owl`, `hpo.owl`, and `uberon.owl` will all work, plus your own created.

### In practice
for examples of Jabberwocky's commands in use, please see the **[site](https://sap218.github.io/jabberwocky/SCENARIO.html)**.

You can combine these commands together to form a process of steps of ontology synonym development and text analysis - see the [SCENARIO](https://sap218.github.io/jabberwocky/SCENARIO.html) for a working example of this process.

![jabberwocky cycle](/images/cycle.jpg)

#### Testing
To run the automated tests (in the cloned directory):
```
$ git submodule init
$ git submodule update
$ tox
```

---

**Thanks!** :dragon:

the poem "Jabberwocky" written by Lewis Carrol is described as a "nonsense" poem.

**Contributors** - thank you!
- [@majensen](https://github.com/majensen) for setting up automated testing w/ `pytest` - [see pull request #13 for more details](https://github.com/sap218/jabberwocky/pull/13)

### Citing
Unstructured text is a rich, untapped resource for advancing research.
Ontologies are valuable in research having shown to address the challenges presented by unstructured text.

Natural Language Processing (NLP) tools exist for text mining and annotation tasks, not enough of these existing tools have ontology manipulation capabilities, despite ontologies being machine readable.
**Jabberwocky** combines ontologies and NLP.

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

End of page.
