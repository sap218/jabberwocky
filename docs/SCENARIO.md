# scenario

### >> go back to [main page](https://sap218.github.io/jabberwocky/)


### >> go to [`jabberwocky/test_files`](https://github.com/sap218/jabberwocky/tree/master/test_files) for data of the following examples

## Aim

You have extracted textual data: blog posts from a social media platform. These social media posts include varios individuals discussing a topic, which you are researching. In this scenario the users are talking about [*pokemon*](https://simple.wikipedia.org/wiki/Pok%C3%A9mon).

Some example posts from the text data:

> I think only gen 6 pokemon are on this path, try route 2 - wanderer wendy

> No thanks, I'm, trying to catch a flying type in the mountains with the clear air - trainer penelope

Your aim is to extract particular posts which individuals use specific terms, e.g. "dragon".

This is where **ontologies are useful**. Ontologies are a controlled set of vocabulary with terms logically related to the other, e.g. in anatomy our hand is a part of the arm. The purpose of Jabberwocky is looking at these terms and their synonyms, as in the example above that the arm has a synonym "upper limb". Current tools which exist for NLP don't include an ontology manipulation aspect, which Jabberwocky overcomes.

## Bandersnatch

[test_files](https://github.com/sap218/jabberwocky/tree/master/test_files/bandersnatch) for `bandersnatch`

You have access to `pocketmonsters.owl` an ontology with some concepts of pokemon, e.g. pokemon types. Below is a snippet of the ontology, looking at the class (label) "generation one", which has the synonym "gen one".
```
<owl:Class rdf:about="pocketmonsters#PM_00008">
	<rdfs:subClassOf rdf:resource="pocketmonsters#PM_00001"/>
        <oboInOWL:hasExactSynonym>generation 1</oboInOWL:hasExactSynonym>
        <oboInOWL:hasRelatedSynonym>gen 1</oboInOWL:hasRelatedSynonym>
        <oboInOWL:hasRelatedSynonym>gen one</oboInOWL:hasRelatedSynonym>
        <rdfs:label xml:lang="en">generation one</rdfs:label>
</owl:Class>
```
Notice the relevant synonym tags, to use `bandersnatch` you need to provide a newline-separated list of tags, `ontology_synonym_tags.txt`.
```
oboInOWL:hasExactSynonym
oboInOWL:hasRelatedSynonym
```
Finally, you have some terms of interest, `words_of_interest_for_ontology.txt`. Notice these terms are exactly the same labels from the ontology.
```
generation one
dragon
route
water
small
large
generation six
```
Using the command `bandersnatch`:
```
$ jab-bandersnatch -o pocketmonsters.owl -s ontology_synonym_tags.txt -k words_of_interest_for_ontology.txt
```
The output `output_ontology_label_synonyms.json` includes your terms of interest and their synonyms based on the synonym tags, some synonym tags are in different formats so it is important to investigate. If you don't have an ontology of interest, FOLLOWING THE SAME STYLE YOU SHOULD MAKE YOUR OWN `.json`. Below is an example of the output (the empty lists mean no synonyms for this term).
```
{
    "small": [],
    "large": [],
    "route": [],
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
    "dragon": []
}
```

## Catch

[test_files](https://github.com/sap218/jabberwocky/tree/master/test_files/catch) for `catch`

Next, using the `catch` command, you provide the previous `bandersnatch` output: `output_ontology_label_synonyms.json` **OR** your own created `.json`, in the example you can see `own_created_word_w_synonyms.json` which includes different synonyms not in the ontology, e.g. "small" has the synonym "tiny". **NOTE**: for the remaining scenario, we will be using `output_ontology_label_synonyms.json`.

You have the social media posts, in the `test_files/catch` directory I provide two formats, `social_media_posts.txt` and `social_media_posts.json` - below is an example of the newline-separated unformatted `.txt`:
```
Any small pokemon nearby? I need to catch a Metapod!
I think only gen 6 pokemon are on this path - try route 2.
```
The `.json` example is below - when using this formatted version, you will need to provide the parameter for user comment / text and possible inner-comments / replies. Notice below `post` is used for a user's comment.
```
{
"thread_one":[
	{"name": "bug catcher joe", "post": "Any small pokemon nearby? I need to catch a Metapod!"},
	{"name": "wanderer wendy", "post": "I think only gen 6 pokemon are on this path - try route 2."}
...
```
Below is an example of running `catch`:
```
$ jab-catch -k output_ontology_label_synonyms.json -t social_media_posts.json -p post -i reply
```
The outputs include `output_terms_match_raw.txt` which include a `.txt` file of newline-separated posts which included one of the terms of interest - this output has **9 posts** (remember this number)
```
what route is best for small normal pokemon my skitty needs a friend
any small pokemon nearby i need to catch a metapod
```
Additionally, the posts formatted as with their terms of interest, `output_terms_match.json`: 
```
{
    "small": [
        "any small pokemon nearby i need to catch a metapod",
...
```

## Bite

[test_files](https://github.com/sap218/jabberwocky/tree/master/test_files/bite) for `bite`

But what if there are synonyms which weren't present in the ontology? Or synonyms which you didn't previously consider? The statistical tf-idf method scores each word in a corpus based on the frequency in the document - essentially picking out the "important terms".

Following the same social media input files as `catch`, you provide a `social_media_posts.txt` or `social_media_posts.json` (with parameters) - in addition to `output_ontology_label_synonyms.json` which removes from the posts in order to increase the scores of the tf-idf statistical analysis, however you don't need to include this file and rather you could investigate how these terms present in the results.

Below is an example of running `bite`:
```
$ jab-bite -k output_ontology_label_synonyms.json -t social_media_posts.txt -g True
```
The output includes `tfidf_results.tsv`, which is a tab-separated file of terms and their tf-idf score, as seen below:
```
words	count
route	2.27975328153784
path	1.8866845905817748
pokemon	1.8215522309449206
...
```
You can also request a plot of term scores as a bar plot and set the term limit (`-l`) - the plot is saved as: `tfidf_plot.pdf`.

## Arise

[test_files](https://github.com/sap218/jabberwocky/tree/master/test_files/arise) for `arise`

Looking at the results from the `tfidf_results.tsv`, you curate synonyms of interest and create: `tfidf_new_synonyms.tsv`. This `.tsv` includes the synonym you wish to inject / update in the ontology, with the corresponding class label, and the type of synonym.
```
synonym	class	type
path	route	oboInOWL:hasRelatedSynonym
evolve	generation	oboInOWL:hasBroadSynonym
```
Below is an example of running `arise` whilst providing the original `pocketmonsters.owl`:
```
$ jab-arise -o pocketmonsters.owl -f tfidf_new_synonyms.tsv
```
The output is an updated ontology `updated-ontology.owl`. See below the broad synonym "evolve" addition to "generation".
```
<owl:Class rdf:about="pocketmonsters#PM_00001">
	<oboInOWL:hasBroadSynonym>evolve</oboInOWL:hasBroadSynonym>
	<rdfs:label xml:lang="en">generation</rdfs:label>
</owl:Class>
```

## **Lets go back to the beginning**

## Bandersnatch ROUND 2

Using `bandersnatch` with `updated-ontology.owl`, the `output_ontology_label_synonyms.json` output will include the new synonyms, for example "route" now has the synonym "path". For this example, I renamed it to `roundtwo_output_ontology_label_synonyms.json`.
```
$ jab-bandersnatch -o updated-ontology.owl -s ontology_synonym_tags.txt -k words_of_interest_for_ontology.txt
```

## Catch ROUND 2

Finally, using `catch`, with the updated `roundtwo_output_ontology_label_synonyms.json` - the output posts should be increased due to more synonyms, from **9 posts to 13**.
```
$ jab-catch -k roundtwo_output_ontology_label_synonyms.json -t social_media_posts.txt
```
