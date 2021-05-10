# scenario

### go back to [main page](https://sap218.github.io/jabberwocky/)


### go to directory in repo for the following [relevant files](https://github.com/sap218/jabberwocky/tree/master/test_files)

## Aim

You have extracted textual data: blog posts from a social media platform. These social media posts include varios individuals discussing a topic, which you are researching. In this scenario the users are talking about [*pokemon*](https://simple.wikipedia.org/wiki/Pok%C3%A9mon).

Some example posts from the text data:

> I think only gen 6 pokemon are on this path, try route 2 - wanderer wendy

> No thanks, I'm, trying to catch a flying type in the mountains with the clear air - trainer penelope

Your aim is to extract particular posts which individuals use specific terms, e.g. "gen" or "flying".

This is where **ontologies are useful**. Ontologies are a controlled set of vocabulary with terms logically related to the other, e.g. in anatomy our hand is a part of the arm. The purpose of Jabberwocky is looking at these terms and their synonyms, as in the example above that the arm has a synonym "upper limb". 

## Bandersnatch

[Bandersnatch test files](https://github.com/sap218/jabberwocky/tree/master/test_files/bandersnatch)

You have access to `pocketmonsters.owl` - an ontology with some concepts of pokemon, e.g. pokemon types. Below is a snippet of the ontology, looking at the class (label) "generation one", which has the synonym "gen one".
```
<owl:Class rdf:about="pocketmonsters#PM_00008">
	<rdfs:subClassOf rdf:resource="pocketmonsters#PM_00001"/>
        <oboInOWL:hasExactSynonym>generation 1</oboInOWL:hasExactSynonym>
        <oboInOWL:hasRelatedSynonym>gen 1</oboInOWL:hasRelatedSynonym>
        <oboInOWL:hasRelatedSynonym>gen one</oboInOWL:hasRelatedSynonym>
        <rdfs:label xml:lang="en">generation one</rdfs:label>
</owl:Class>
```
You have a list of the relevant synonym tags, `ontology_synonym_tags.txt`. As you can see, these tags are in the example class above.
```
oboInOWL:hasExactSynonym
oboInOWL:hasRelatedSynonym
```
Finally, you have some terms of interest, `words_of_interest_for_ontology.txt`:
```
generation one
dragon
...
```
Using the command `bandersnatch`:
```
$ jab-bandersnatch -o pocketmonsters.owl -s ontology_synonym_tags.txt -k words_of_interest_for_ontology.txt
```
The output is `output_ontology_label_synonyms.json` which includes your terms of interest and their synonyms based on the synonym tags. **Note**: if you don't have an ontology of interest, YOU SHOULD MAKE YOUR OWN `.json` FOLLOWING THE SAME STYLE. Below is an example of the output, as you can see, you curated the synonyms for the terms you wanted, the empty lists mean no synonyms for this term.
```
{
    "small": [],
    "large": [],
    "generation one": [
        "generation 1",
        "gen 1",
        "gen one"
    ],
    "generation six": [
        "generation 6",
        "gen 6",
        "gen six"
    ],
    "water": [],
    "dragon": [],
    "fairy": []
}
```

## Catch

[Catch test files](https://github.com/sap218/jabberwocky/tree/master/test_files/catch)

Next, using the `catch` command, you provide the previous `bandersnatch` output: `output_ontology_label_synonyms.json` of keyterms OR your own created `.json`.

You have the social media posts, in the tests directory I provide two formats, `social_media_posts.txt` and `social_media_posts.json`. Below is an example of the newline-separated unformatted `.txt`:
```
Any small pokemon nearby? I need to catch a Metapod!
I think only gen 6 pokemon are on this path - try route 2.
```
The `.json` example is below. If you use the formatted version, you will need to provide the parameter for user comment / text, e.g. "post". If your user posts have replies, or even inner replies, they should follow the same inner-parameter, e.g. "reply".
```
{
"thread_one":[
	{"name": "bug catcher joe", "post": "Any small pokemon nearby? I need to catch a Metapod!"},
	{"name": "wanderer wendy", "post": "I think only gen 6 pokemon are on this path - try route 2."}
...
```
Below is an example of running `catch`:
```
$ jab-catch -k output_ontology_label_synonyms.json -t example_textfile.json -p post -i reply
```
The outputs include `output_terms_match_raw.txt` which include a `.txt` file of newline-separated posts which included one of the terms of interest
```
what route is best for small normal pokemon my skitty needs a friend
any small pokemon nearby i need to catch a metapod
```
Additionally, the posts formatted as with their terms of interest:
```
{
    "small": [
        "any small pokemon nearby i need to catch a metapod",
...
```

## Bite

[Bite test files](https://github.com/sap218/jabberwocky/tree/master/test_files/bite)

But what if there are synonyms which weren't present in the ontology? Or synonyms which you didn't previously consider? You can use `bite` command!

Following the same social media input files as `catch` (using a `.txt`, or `.json` with parameters) in addition to `output_ontology_label_synonyms.json` which removes from the posts in order to increase the scores of the tf-idf statistical analysis, however you don't need to include these terms and synonyms `.json` file.

Below is an example of running `bite`:
```
$ jab-bite -k output_ontology_label_synonyms.json -t example_textfile.json -p post -i reply -g True -l 20
```
The output includes `tfidf_results.tsv`, which is a tab-separated file of terms and their tf-idf score, as seen below:
```
words	count
route	2.27975328153784
path	1.8866845905817748
pokemon	1.8215522309449206
...
```
You can also request a plot of term scores as a bar plot and set the term limit, `tfidf_plot.pdf`.

## Arise

[Arise test files](https://github.com/sap218/jabberwocky/tree/master/test_files/arise)

Looking at these results from the `tfidf_results.tsv`, you curate a new `tfidf_new_synonyms.tsv` of the sort of new synonyms you wish to inject / update in the ontology, like below:
```
synonym	class	type
path	route	oboInOWL:hasRelatedSynonym
evolve	generation	oboInOWL:hasBroadSynonym
```
Below is an example of running `arise` whilst providing the original `pocketmonsters.owl` and this `tfidf_new_synonyms.tsv`:
```
$ jab-arise -o pocketmonsters.owl -f tfidf_new_synonyms.tsv
```
The output is an updated ontology `updated-ontology.owl`.
```
<owl:Class rdf:about="pocketmonsters#PM_00001">
	<oboInOWL:hasBroadSynonym>evolve</oboInOWL:hasBroadSynonym>
	<rdfs:label xml:lang="en">generation</rdfs:label>
</owl:Class>
```

## **Lets go back to the beginning**

Using `bandersnatch` with `updated-ontology.owl`, the `output_ontology_label_synonyms.json` output will included the new synonyms!

Finally, using `catch`, you provide the updated `output_ontology_label_synonyms.json` - the output posts should be increased due to more synonyms!
