# Jabberwocky

[![DOI](https://joss.theoj.org/papers/10.21105/joss.02168/status.svg)](https://doi.org/10.21105/joss.02168) [![DOI](https://zenodo.org/badge/227571502.svg)](https://zenodo.org/badge/latestdoi/227571502) 

**see [Jabberwocky site](https://sap218.github.io/jabberwocky/) for in-depth explanation and working scenarios (including test files)**

Jabberwocky is a toolkit for **ontologies**. Since we all know ontologies are "*nonsense*". Not enough tools existsing utilise the power of ontologies. Don't hesitate to create an [`issue`](https://github.com/sap218/jabberwocky/issues) or [`pull request`](https://github.com/sap218/jabberwocky/pulls) (see [**guidelines**](https://github.com/sap218/jabberwocky/blob/master/CONTRIBUTING.md) first).

#### Version

See `setup.py` in your local copy for version number | or `Releases`:
* **v1.0.0.0** [29/06/2020]
* **v2.0.0.0** [10/05/2021]

##### Install
```
$ git clone https://github.com/sap218/jabberwocky
$ cd jabberwocky
$ python3 setup.py install --user
```
**note**: if you are using a virtual environment you can avoid `--user`

##### Prerequisites
```
$ pip3 install click BeautifulSoup4 scikit-learn pandas lxml pytest spacy matplotlib
```
or **after installing**, use the `requirements.txt` file:
```
$ pip3 install -r requirements.txt
```

#### Elements

command | description
------- | -----------
`bandersnatch` | extract synonyms from an RDF/XML syntax `OWL` ontology
`catch` | extract elements / sentences of text using key words
`bite`  | run statistical tf-idf for important words from text
`arise` | adding / updating new synonyms to an ontology

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

## bandersnatch
`bandersnatch` curates synonyms for a list of key terms / or words of interest from an ontology of your choice, you provide a list of ontology synonym tags. **note**: it is recommended your list of keywords are exactly the classes from your chosen ontology (all in lowercase).
```
$ jab-bandersnatch -o hpo.owl -s ontology_synonym_tags.txt -k words_of_interest.txt
```

## catch
`catch` essentially "catches" key elements / sentences from textual data using a `.json` of key terms and their synonyms, you can use the outcome from `bandersnatch`. A user will also provide a `.txt` or `.json` of the text data. **note**: if a `.json` of text data is provided, you need specify the parameter for the field that contains the textual data to process.
```
$ jab-catch -k label_with_synonyms.json -t facebook_posts.json -p user-comment -i inner-user-comment-reply
```

## bite
`bite` runs a tf-idf statistical analysis: searching for important terms in a text corpus. a user can use a list of key terms to remove from the text in order to avoid being in the statistical model - meaning other terms may be ranked higher. **note**: again with `catch`, if you provide a `.json` of text data, you need specify the field that contains the textual data to process. Using `-g True` means you'll get a bar plot of the (default) 30-top terms.
```
$ jab-bite -k label_with_synonyms.json -t twitter_posts.txt -g True
```

## arise
`arise` inserts synonyms in an ontology: **you** define these synonyms (e.g. "exact", "broad", "related", or "narrow") - these new synonyms may be based on the tf-idf statistical analysis from `bite`.
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

You can combine these commands together to form a process of steps of ontology synonym development and text analysis - see the [SCENARIO](https://sap218.github.io/jabberwocky/SCENARIO.html) for a working example of this process.

![jabberwocky cycle](/images/cycle.jpg)
