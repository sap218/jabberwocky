# jabberwocky

A toolkit for **ontologies**. Since we all know ontologies are "*nonsense*". **Note**: to check version, see `setup.py` in your local copy.

Don't hesitate to create an [`issue`](https://github.com/sap218/jabberwocky/issues) or [`pull request`](https://github.com/sap218/jabberwocky/pulls) (see [**guidelines**](https://github.com/sap218/jabberwocky/blob/master/CONTRIBUTING.md) first).

#### Elements

command | description
------- | -----------
`catch` | to extract elements of text using key words
`bite`  | to look at important words from text
`arise` | adding new synonyms to an ontology


##### Prerequisites
```
$ pip3 install click BeautifulSoup4 scikit-learn pandas lxml
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
`jabberwocky` works with `OWL` ontology formats such as `OWL/XML` and also `RDF/XML`. For example biomedical ontologies such as `doid.owl`, `hpo.owl`, and `uberon.owl` will all work.

**note**: if you are using your own created ontology, make sure you define annotations with the `rdfs:` schema, e.g. `rdfs:hasExactSynonym`.

#### Examples
For examples of Jabberwocky's commands in use, please see the **[`jabberwocky-tests`](https://github.com/sap218/jabberwocky-tests)** repository.

**OR** see [**SCENARIO.md**](https://github.com/sap218/jabberwocky/blob/master/SCENARIO.md) for further explanation. 

---

---

## catch
`catch` essentially "catches" key elements from textual data using an ontology's classes & synonyms, with a set of keywords one can limit their search. **Note**: it is recommended your list of keywords are exactly the classes from your chosen ontology (all in lowercase). **Note**: if a `.json` is provided, you need specify the field inside the JSON that contains the textual data to process.

#### Usage
```
$ catch --help
Usage: catch [OPTIONS]

Options:
  -o, --ontology TEXT   file of ontology. [required]
  -k, --keywords TEXT   list of classes/terms you want to use to search.
  -t, --textfile TEXT   JSON or TXT file of text you want annotate. [required]
  -p, --parameter TEXT  parameter for the JSON file text.
  --help                Show this message and exit.
```
#### Running
```
$ catch -o ../ontology/pocketmonsters.owl -k listofwords.txt -t public_forum.json -p post
```

###### Output
* a `.json` file of the classes and synonyms for your reference
* `catch` prints out the key texts which included these classes/synonyms
* you can use `>` to put into a separate file
* see [`jabberwocky-tests`](https://github.com/sap218/jabberwocky-tests) for an example of `catch` with an example output file

---

## bite
`bite` runs a tf-idf statistical analysis: searching for important terms in a text corpus. A user can use an ontology to avoid key terms being in the statistical model. **Note**: with the `.json` input you need specify the field inside the JSON that contains the textual data to process.

#### Usage
```
$ bite --help
Usage: bite [OPTIONS]

Options:
  -o, --ontology TEXT   file of ontology.
  -t, --textfile TEXT   JSON file of text you want to observe.  [required]
  -p, --parameter TEXT  parameter for the JSON file text.  [required]
  --help                Show this message and exit.
```
#### Running
```
$ bite -t public_forum.json -p post
```

###### Output
* a `.txt` file of all classes and synonyms which were in the ontology - for your reference
* `bite` prints out the important terms from the textual data: sorted by value - which also makes a `.csv`
* see [`jabberwocky-tests`](https://github.com/sap218/jabberwocky-tests) for an example of `bite`

---

## arise
`arise` inserts synonyms in an ontology based on your chosing: **you** define if these synonyms are "exact", "broad", "related", or "narrow" - these new synonyms may be based on the tf-idf statistical analysis from `bite`.

#### Usage
```
$ arise --help
Usage: arise [OPTIONS]

Options:
  -o, --ontology TEXT  file of ontology.  [required]
  -f, --tfidf TEXT     tf-idf CSV file of the synonyms you want to add.  [required]
  --help               Show this message and exit.
```
#### Running
```
$ arise -o ../ontology/pocketmonsters.owl -f new_synonyms_tfidf.csv
```

###### Output
* file titled, `updated_ontology.owl` in the directory you run
* see [`jabberwocky-tests`](https://github.com/sap218/jabberwocky-tests) for an example of `arise`

---

## Thanks! :dragon:

The poem "Jabberwocky" written by Lewis Carrol is described as a "nonsense" poem.

You can combine these commands together to form a process of steps of ontology synonym development and text analysis. See `jabberwocky-tests` repo for the [`jabberwocky-tests/process`](https://github.com/sap218/jabberwocky-tests/tree/master/process) directory for a chain of commands (as described in the image below).

![jabberwocky cycle](/images/cycle.jpg)
