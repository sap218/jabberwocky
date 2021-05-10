# scenario

### go back to [main page](https://sap218.github.io/jabberwocky/)

You have extracted textual data: blog posts from a social media platform. These social media posts include varios individuals discussing a topic, which you are researching. In this scenario the users are talking about [*pokemon*](https://simple.wikipedia.org/wiki/Pok%C3%A9mon).

Some example posts from the text data:

> I think only gen 6 pokemon are on this path, try route 2 - wanderer wendy

> No thanks, I'm, trying to catch a flying type in the mountains with the clear air - trainer penelope

Your aim is to extract particular posts which individuals use specific terms, e.g. "gen" or "flying".

This is where **ontologies are useful**. Ontologies are a controlled set of vocabulary with terms logically related to the other, e.g. in anatomy our hand is a part of the arm. The purpose of Jabberwocky is looking at these terms and their synonyms, as in the example above that the arm has a synonym "upper limb". 

You have access to `pocketmonsters.owl` - an ontology with some concepts of pokemon, e.g. pokemon types.

You make a note of the synonym tags:
```
oboInOWL:hasExactSynonym
oboInOWL:hasRelatedSynonym
```
You have some terms of interest:
```
generation one
dragon
...
```
Using `bandersnatch` you get a `.json` output which includes your terms of interest and their synonyms based on the synonym tags. **Note**: if you don't have an ontology of interest, you can make your own `.json` file of terms and synonyms of interest.

What you have at this point: a `.json` of terms of interest and their synonyms, whether you used an ontology or not.

Next, using the `catch` command, you provide that `.json` of keyterms and your text file: this could be a `.txt` of newline-separated posts or a `.json`. **Note**: if you provide a `.json` you will need to provide the parameter for post text, e.g. "user-comment". If your `.json` posts have replies, or even inner replies, they should follow the same inner-parameter, e.g. "user-comment-reply".

What you have at this point: a `.json` of terms of interest and the posts which matches that term, and a `.txt` with all posts which included a term of interest.

But what if there are synonyms which weren't present in the ontology? Or synonyms which you didn't previously consider? You can use `bite`, which follows the same posts input file and structure as `catch` (using a `.txt`, or `.json` with parameters). You can provide the `.json` of keyterms which will be removed from the posts to increase the scores of the tf-idf statistical analysis. You can also request a plot of term scores as a bar plot and set the term limit.

What you have at this point: a `.tsv` of the tf-idf results and a `.pdf` of the plot.

Looking at these results from the `.tsv`, you curate a new `.tsv` of the sort of new synonyms you wish to inject / update in the ontology.
```
synonym	class	type
path	route	oboInOWL:hasRelatedSynonym
```
Using `arise`: providing the original `pocketmonsters.owl` and this `.tsv`, you will be given an updated ontology `.owl`.

**Lets go back to the beginning**

Using `bandersnatch` you get an updated `.json` output which includes your terms of interest and their synonyms, you should see the new synonyms!

Finally, using the `catch` command, you provide that `.json` of updated keyterms and your text file: you should see more posts in the output!
