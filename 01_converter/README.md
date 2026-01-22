# `converter` - `gimble`

### `is_this_a_test`
+ set to `True` to run the test, see `test/` for results

***

### `dir_output`
+ any outputs will be stored here (including logs)
+ suggested to use `output/` but users are welcome to create their own dir

***

### `excel_file`
+ the `.xlsx` file, users should include the filepath too

**Additional Excel information**

+ each worksheet in the excel should be labelled with the superclass
+ each sheet should have at least one column: class
+ it is **strongly** recommended to have another column for annotating, e.g. a definition
+ see [`space.xlsx`](https://github.com/sap218/CelestialObject/tree/main/excel) for a working example

***

### `the_name`
+ the name of the ontology, users don't need to include `.owl` here

### `git_uid_repo`
+ username & repository where ontology stored - e.g. `sap218/CelestialObject` - completes:

```
namespace = f"https://github.com/{git_uid_repo}/blob/master/{the_name}.owl"
```

+ it is important that users do not edit the `namespace`!

## Ontology metadata

+ `iri_prefix` - IRI of ontology, often an abbreviation/acronym (e.g. for the space ontology we used `iri_prefix="UFO"`)
+ `ontology_description` - describe your ontology
+ `developers` - list of individuals involved in the development of the ontology
+ `contributors` - list of individuals who helped
+ `version` - version of ontology, e.g. `version="v0.1"`
+ `licensed` - license information, a commonly used one is: https://creativecommons.org/licenses/by-nc/4.0/

### `defined_annotations`
+ this is a dictionary that that'll link the excel and ontology metadata together
+ keys are the column names for annotating and the value is an url, see the example below:

```
defined_annotations = {
    "definition": "http://www.w3.org/2000/01/rdf-schema#comment",
    "dbXref": "http://www.geneontology.org/formats/oboInOwl#DbXref",
    "externalResource": "http://www.w3.org/2000/01/rdf-schema#seeAlso",
    "synonym": f"{namespace}#hasSynonym"
    }
```

+ users can define their own (see the above last example for `synonym`)
+ or users can use from the The RDF Schema vocabulary ([RDFS](https://www.w3.org/2000/01/rdf-schema))

***

End of page
