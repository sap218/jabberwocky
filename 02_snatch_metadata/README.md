# `snatch metadata`

### `is_this_a_test`
+ set to `True` to run the test, see `test/` for results

***

### `dir_output`
+ any outputs will be stored here (including logs)
+ suggested to use `output/` but users are welcome to create their own dir

***

### `ontology_file`
+ the name of the `.owl` ontology, users should include filepath

### `metadata_tags_file`
+ newline delimited (`.txt`) file of the ontology tags to determine which metadata to `snatch`
+ users should open their ontology in a text editor to see how the tags are defined if they are unsure, e.g. `UFO:hasSynonym`:

```
  <owl:Class rdf:about="https://raw.githubusercontent.com/sap218/CelestialObject/main/space.owl#UFO_0006">
    <rdfs:label xml:lang="en">mars</rdfs:label>
    <rdfs:subClassOf rdf:resource="https://raw.githubusercontent.com/sap218/CelestialObject/main/space.owl#UFO_0002"/>
    <UFO:hasSynonym>red planet</UFO:hasSynonym>
  </owl:Class>
```

### `classes_of_interest`
+ newline delimited (`.txt`) file with ontology classes of interest
+ ensure classes are extact matches to the literal ontology classes
+ if users don't provide a file, script will extract metadata from **all** classes using the provided metadata tags file

***

End of page
