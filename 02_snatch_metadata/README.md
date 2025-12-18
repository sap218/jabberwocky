# `snatch metadata`

### `is_this_a_test`
+ set to `True` to run the test, see `test/` for results

### `dir_output`
+ any outputs will be stored here (including logs)
+ suggested to use `output/` but users are welcome to create their own dir

### `files_location`
+ location of your input files, e.g. `input/`

***

### `ontology_name`
+ the name of the ontology
+ users don't need to include `xlsx / owl`

### `ontology_tags`
+ newline delimited (`.txt`) file of ontology tags to determine the metadata to `snatch`, e.g. `ufo:hasSynonym`:

```
  <owl:Class rdf:about="https://github.com/sap218/CelestialObject/blob/master/space.owl#UFO_0013">
    <rdfs:label xml:lang="en">mars</rdfs:label>
    <rdfs:subClassOf rdf:resource="https://github.com/sap218/CelestialObject/blob/master/space.owl#UFO_0009"/>
    <ufo:hasSynonym>red planet</ufo:hasSynonym>
  </owl:Class>
```

### `classes_of_interest`
+ newline delimited (`.txt`) file with ontology classes of interest
+ if users don't provide a file, script will extract metadata from **all** classes
+ ensure classes are extact matches to the literal ontology classes

***

End of page
