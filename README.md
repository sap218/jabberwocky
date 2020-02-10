# jabberwocky

**Tool for ontologies. Since we all know ontologies are "nonsense".**

#### Install
`$ git clone https://github.com/sap218/jabberwocky`

`$ python3 setup.py install --user`

#### Prerequisites
```pip3 install click BeautifulSoup4```

#### Example
Please see the [`jabberwocky-tests`](https://github.com/sap218/jabberwocky-tests) repository for the user tests of jabberwocky's commands.

## catch
`catch` annotates textual data using an ontology's classes & synonyms, with a set of keywords one can limit their search. **Note**: it is recommended your list of keywords are exactly the classes from your chosen ontology (all in lowercase). **Note**: if a JSON is provided, you need to give a parameter.

#### Usage
```
$ catch --help
Usage: catch [OPTIONS]

Options:
  -o, --ontology TEXT   file of ontology. [required]
  -k, --keywords TEXT   list of classes/terms you want to use to search.
  -t, --textfile TEXT   JSON ot TXT file of text you want annotate. [required]
  -p, --parameter TEXT  parameter for the JSON file text.
  --help                Show this message and exit.
```
#### Running
`$ catch --ontology doid.owl --keywords term_list.txt --textfile blogs.json.json --parameter post_text`

`$ catch -o hpo.owl -k my_tags.txt -t user_notes.txt`

`$ catch -o pato.owl --textfile patient_symptoms.json -p text_entry

###### Output
* a JSON file of the classes and synonyms for your reference
* `catch` prints out the key texts, which included these classes/synonyms
* you can use `>` to put into a separate file
* see [`jabberwocky-tests`](https://github.com/sap218/jabberwocky-tests) for an example of `catch` with an example output file

## Thanks!
Don't hesitate to create an issue/request (see [contributing guidelines](https://github.com/sap218/jabberwocky/blob/master/CONTRIBUTING.md) first).

The poem "Jabberwocky" written by Lewis Carrol is described as a "nonsense" poem.
