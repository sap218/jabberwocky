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
`catch` annotates textual data using keywords which searches an ontology for the classes & synonyms. **Note**: it is recommended your list of keywords are exactly the classes from your chosen ontology (all in lowercase).

#### Usage
```
$ catch --help
Usage: catch [OPTIONS]

Options:
  -ontology TEXT   file of ontology
  -keywords TEXT   list of classes/terms you want to use to search
  -textfile TEXT   JSON file of text you want annotate
  -parameter TEXT  parameter for the JSON file text
  --help           Show this message and exit.
```
#### Running
`$ catch -ontology doid.owl -keywords list_of_classes.txt -textfile textualdata.json -parameter post_comment`

`$ catch -ontology hpo.owl -keywords my_tags.txt -textfile blog_text.txt -parameter blog_text`

###### Output
* a JSON file of the classes and synonyms for your reference
* `catch` prints out the key texts, which include these classes/synonyms, in the command line
* you can use `>` to put into a separate file
* see [`jabberwocky-tests`](https://github.com/sap218/jabberwocky-tests) for an example of `catch` with an example output file

## Thanks!
Don't hesitate to create an issue/request (see [contributing guidelines](https://github.com/sap218/jabberwocky/blob/master/CONTRIBUTING.md) first).

The poem "Jabberwocky" written by Lewis Carrol is described as a "nonsense" poem.
