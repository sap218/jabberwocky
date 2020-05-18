# example use-case of Jabberwocky

#### **note** we are running these command in the `jabberwocky-test/process` directory...

### scenario
you have some textual data: **blog** posts from a social media platform. these posts include individuals discussing a topic which you are interested in. in this scenario the users are talking about [*pokemon*](https://simple.wikipedia.org/wiki/Pok%C3%A9mon).

for example, you may have some posts (formatted differently) such as:
> I think only gen 6 pokemon are on this path, try route 2 - wanderer wendy
> No thanks, I'm, trying to catch a flying type in the mountains with the clear air - trainer penelope

your **aim** is to extract particular **posts** which individuals use specific terms, e.g. "gen" or "flying".

This is where **ontologies** are **useful**. ontologies are a controlled set of vocabulary with terms logically related to the other, e.g. our anatomy is that the iris is a part of the eye, but ontologies will have this defined in much more detail and logically. **however** the purpose of **jabberwocky** is not the logical relationships: but the **terms** themselves. ontologies store synonyms: an alternative version of a term, e.g. "eye" has synonyms, "eyeball", "globe", or "organ of sight". 

in [jabberwocky-tests/ontology/](https://github.com/sap218/jabberwocky-tests/tree/master/ontology), there is the file, `pocketmonsters.owl`. here is the example ontology for our scenario, it can be expanded with additional terms or relationships however it is a useful start for the scenario.


### catch
using the `catch` command, you are trying to extract the posts which include key terms, e.g. "generation one", "dragon", and more. in [jabberwocky-tests/process/](https://github.com/sap218/jabberwocky-tests/tree/master/process) you will see the `listofwords.txt` which is a simple text file of these terms you are looking for, they match the exact terms from the ontology. there is also the textual data file: `public_forum` with a **total of 24 posts**, but split into 5 threads. 

```
$ catch -o ../ontology/pocketmonsters.owl -k listofwords.txt -t public_forum.json -p post > catch_01_output.txt
```
after using `catch` you will be given a file: `ontology_dict_class_synonyms.json` which is for your reference to observe the terms you want to use and their synonyms (for the scenario it was renamed to `catch_01_ontology_dict_class_synonyms.json`). it is worth noting that if you don't provide any keywords, the script will use every term from the ontology.

**finally**, the `catch_01_output.txt` file a plain file with each post that includes one of the terms (or synonyms). this file will include **11 posts (out of 24)** which have the terms. 

#### however
you want to find out what terms are use most frequently, **plus** you notice in `catch_01_ontology_dict_class_synonyms.json` there lacks synonyms...


### bite
the `bite` command runs a tf-idf statistical analysis: searching for **important** (most frequrntly used) terms in a text corpus.
```
$ bite -t public_forum.json -p post
```

the main output is in [jabberwocky-tests/process/](https://github.com/sap218/jabberwocky-tests/tree/master/process), the file: `tfidf_results.csv` (renamed to `bite_01_tfidf_results.csv` for the scenario). this shows the tf-idf rankings in tabular form. this file is important to see which terms you may want to be included in your study, or to be added to the ontology as additional synonyms...

| words   | count              |
|---------|--------------------|
| route   | 0.9693123548553331 |
| pokemon | 0.8661273891167867 |
| pokedex | 0.7561604589465487 |
| path    | 0.7399254994619547 |
| gen     | 0.7107711593211153 |
| evolve  | 0.672293913917355  |


### arise
now that you know the which words which should be additional synonyms to some terms from the tf-idf results, you can improve the `pocketmonsters.owl` ontology

you will need to provide these new (in the example it is named, `new_synonyms_tfidf.csv`) synonyms in a tabular format: the synonym column is the term from the tf-idf results, the class column are the terms from the ontology, and the type column explains the type of synonym you want to add. 

| synonym | class      | type    |
|---------|------------|---------|
| path    | route      | related |
| evolve  | generation | broad   |

the output is `updated-ontology.owl` which is newly improved ontology with those added synonyms, see in [jabberwocky-tests/process/](https://github.com/sap218/jabberwocky-tests/tree/master/process).
```
$ arise -o ../ontology/pocketmonsters.owl -f new_synonyms_tfidf.csv 
```


### second round of bite
we need to know if we extracted as much as possible from the textual data. we will run a second round of `bite`, whilst using `pocketmonsters.owl` to remove all terms from the text which match a term from the ontology: to observe the left over terms.

```
$ bite -o updated-ontology.owl -t public_forum.json -p post
```
the output includes `tfidf_results.csv` **but also** `ontology_all_terms.txt` (both renamed to `bite_02_tfidf_results.csv` & `bite_02_ontology_all_terms.txt`). the all terms file includes every term from the ontology which were removed from the textual data for your reference. and the tf-idf results tabular data shows the newly ranked terms, below the new tf-idf results (because of the updated ontology synonyms and removal of ontology terms) - we can now use this to show the first round of tf-idf was successful and we can proceed...

| words     | count               |
|-----------|---------------------|
| pokemon   | 1.0323383562353856  |
| pokedex   | 0.8403213855890346  |
| fashioned | 0.6350907205215048  |
| dislike   | 0.6350907205215048  |
| skitty    | 0.5218234880251023  |
| catch     | 0.46094438609224664 |


### final catch
now for a **final** round of `catch` we want to use these new synonyms in our search for posts. our posts output in `catch_02_output.txt` we have **16 posts (out of 24)** which is an improvement from the original `catch` use which returned only 11 posts. showing altogether the usefulness of each command, the outputs, and how they can be strung together. 
```
$ catch -o updated-ontology.owl -k listofwords.txt -t public_forum.json -p post > catch_02_output.txt
```
