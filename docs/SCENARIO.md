# Jabberwocky Scenario

go back to [main page](https://sap218.github.io/jabberwocky/)

You have extracted textual data: blog posts from a social media platform. These social media posts include varios individuals discussing a topic, which you are researching. In this scenario the users are talking about [*pokemon*](https://simple.wikipedia.org/wiki/Pok%C3%A9mon).

Some example posts from the text data:

> I think only gen 6 pokemon are on this path, try route 2 - wanderer wendy

> No thanks, I'm, trying to catch a flying type in the mountains with the clear air - trainer penelope

Your aim is to extract particular posts which individuals use specific terms, e.g. "gen" or "flying".

This is where ontologies are **useful**. Ontologies are a controlled set of vocabulary with terms logically related to the other, e.g. in anatomy our hand is a part of the arm. The purpose of Jabberwocky is looking at these terms and their synonyms, as in the example above that the arm has a synonym "upper limb". 

You have access to `pocketmonsters.owl` - an ontology with some concepts of pokemon, e.g. pokemon types. You have some terms of interest, e.g. *** ***

Using the `catch` command, 

you are trying to extract the posts which include key terms, e.g. "generation one", "dragon", and more. in [jabberwocky-tests/process/](https://github.com/sap218/jabberwocky-tests/tree/master/process) you will see the `listofwords.txt` which is a simple text file of these terms you are looking for, they match the exact terms from the ontology. there is also the textual data file: `public_forum` with a **total of 24 posts**, but split into 5 threads. 
