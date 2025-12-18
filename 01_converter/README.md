# `converter` - `gimble`

### `is_this_a_test`
+ set to `True` to run the test, see `test/` for results

### `dir_output`
+ any outputs will be stored here (including logs)
+ suggested to use `output/` but users are welcome to create their own dir

### `excel_file_location`
+ where the excel file is located

**Additional information:**

+ each worksheet in the excel should be labelled with the superclass
+ each sheet should have at least one column: class
+ it is **strongly** recommended to have another column for annotating, e.g. a definition
+ see [`space.xlsx`](https://github.com/sap218/CelestialObject/tree/main/excel) for a working example

### `the_name`
+ the name of the excel file/your ontology
+ users don't need to include `xlsx / owl`

### `git_uid` / `git_repo`
+ username & repository where ontology stored, completes:

```
namespace = f"https://github.com/{git_uid}/{git_repo}/blob/master/{the_name}.owl"
```

## Ontology metadata

+ `iri_prefix` - IRI of ontology, often an abbreviation/acronym (e.g. space IRI=UFO)
+ `ontology_description` - describe your ontology
+ `developers` - list of individuals involved in the development of the ontology
+ `contributors` - list of individuals who helped
+ `version` - version of ontology, e.g. v1.0
+ `licensed` - license information, a commonly used one is: https://creativecommons.org/licenses/by-nc/4.0/

### `defined_annotations`
+ this is a dictionary that essentially links the ontology and excel together
+ keys are the column names for annotating and the value is an url, see the example below:

```
defined_annotations = {
    "synonym": f"{namespace}#hasSynonym",
    "definition": "http://www.w3.org/2000/01/rdf-schema#comment"
    "externalResource": "http://www.w3.org/2000/01/rdf-schema#seeAlso"
    }
```

- users can define their own (see the above example for `synonym`)
- or users can use from the The RDF Schema vocabulary [RDFS](https://www.w3.org/2000/01/rdf-schema)

***

End of page
