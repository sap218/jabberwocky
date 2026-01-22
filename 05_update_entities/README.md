# `update entities` - `arise`

### `is_this_a_test`
+ set to `True` to run the test, see `test/` for results

***

### `dir_output`
+ any outputs will be stored here (including logs)
+ suggested to use `output/` but users are welcome to create their own dir

***

### `ontology_file`
+ the name of the `.owl` ontology, users should include filepath

### `update_entities`
+ file of entities to update ontology, the order is important: new classes should be defined before metadata
+ can be either `.tsv` or `.csv`
+ users should open their ontology in a text editor to see how the tags are defined, e.g.

```
class	annotation	tag
eclipse	UFO_0045	rdfs:subClassOf
eclipse	darkening	UFO:hasSynonym
```

### `new_version`
+ update version of ontology, e.g. `new_version="v2.0"` (can leave empty if you don't wish to update')

***

End of page
