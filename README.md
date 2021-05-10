# jabberwocky

>> see [site](https://sap218.github.io/jabberwocky/) for in-depth explanation and working scenarios (including test files)

a toolkit for **ontologies**. Since we all know ontologies are "*nonsense*". 

[![DOI](https://joss.theoj.org/papers/10.21105/joss.02168/status.svg)](https://doi.org/10.21105/joss.02168) [![DOI](https://zenodo.org/badge/227571502.svg)](https://zenodo.org/badge/latestdoi/227571502) 

**note**: see `setup.py` in your local copy for version number | or `Releases`:
* **v1.0.0.0** [29/06/2020]
* **v2.0.0.0** [10/05/2021]

don't hesitate to create an [`issue`](https://github.com/sap218/jabberwocky/issues) or [`pull request`](https://github.com/sap218/jabberwocky/pulls) (see [**guidelines**](https://github.com/sap218/jabberwocky/blob/master/CONTRIBUTING.md) first).

#### Elements

command | description
------- | -----------
`bandersnatch` | to extract synonyms from an RDF/XML syntax `OWL` ontology
`catch` | to extract elements of text using key words
`bite`  | to look at important words from text
`arise` | adding new synonyms to an ontology


##### Prerequisites
```
$ pip3 install click BeautifulSoup4 scikit-learn pandas lxml pytest spacy matplotlib
```
**or after installing**, use the `requirements.txt` file:
```
$ pip3 install -r requirements.txt
```

##### Install
```
$ git clone https://github.com/sap218/jabberwocky
$ cd jabberwocky
$ python3 setup.py install --user
```
**note**: if you are using a virtual environment you can avoid `--user`

#### Ontology formats
`jabberwocky` works with the `OWL` ontology format: `RDF/XML` - for example, well-known biomedical ontologies such as `doid.owl`, `hpo.owl`, and `uberon.owl` will all work, plus your own created.

#### Examples
for examples of Jabberwocky's commands in use, please see the **[site](https://sap218.github.io/jabberwocky/SCENARIO.html)**.

**OR** to run the automated tests (in the cloned directory):
```
$ git submodule init
$ git submodule update
$ tox
```

---
---

## bandersnatch
`bandersnatch` curates synonyms for a list of key terms / or words of interest from an ontology of your choice, you provide a list of ontology synonym tags. **note**: it is recommended your list of keywords are exactly the classes from your chosen ontology (all in lowercase).

#### Usage
```
$ jab-bandersnatch -o pocketmonsters.owl -s ontology_synonym_tags.txt -k words_of_interest.txt
```

---

## catch
`catch` essentially "catches" key elements / sentences from textual data using a `.json` of key terms and their synonyms. **note**: if a `.json` is provided, you need specify the parameter for the field that contains the textual data to process.

#### Usage
```
$ jab-catch -k output_ontology_label_synonyms.json -t example_textfile.json -p user-comment -i inner-user-comment-reply
```

---

## bite
`bite` runs a tf-idf statistical analysis: searching for important terms in a text corpus. a user can use a list of key terms to remove from the text in order to avoid being in the statistical model - meaning other terms may be ranked higher. **note**: with the `.json` input you need specify the field inside the JSON that contains the textual data to process.

#### Usage
```
$ jab-bite -k output_ontology_label_synonyms.json -t example_textfile.json -p user-comment -i inner-user-comment-reply -g True -l 20
```

---

## arise
`arise` inserts synonyms in an ontology: **you** define these synonyms (e.g. "exact", "broad", "related", or "narrow") - these new synonyms may be based on the tf-idf statistical analysis from `bite`.

#### Usage
```
$ jab-arise -o pocketmonsters.owl -f tfidf_new_synonyms.tsv
```

---

## Thanks! :dragon:

the poem "Jabberwocky" written by Lewis Carrol is described as a "nonsense" poem.

**Contributors** - thank you!
- [@majensen](https://github.com/majensen) for setting up automated testing w/ `pytest` - [see pull request #13 for more details](https://github.com/sap218/jabberwocky/pull/13)

**Citing**
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

---

## ONE LAST THING...

You can combine these commands together to form a process of steps of ontology synonym development and text analysis.

![jabberwocky cycle](/images/cycle.jpg)
