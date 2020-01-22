# jabberwocky

Samantha C Pendleton | v0.0.1

**Tool for ontologies. Since we all know ontologies are "nonsense".**

#### Install
`$ git clone https://github.com/sap218/jabberwocky`

`$ python3 setup.py install --user`

## catch
`catch` annotates textual data using keywords which searches an ontology for the classes & synonyms. 

#### Running
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

`$ catch -ontology doid.owl -keywords list_of_classes.txt -textfile textualdata.json -parameter post_comment`

The poem "Jabberwocky" written by Lewis Carrol is described as a "nonsense" poem.
