# Jabberwocky
Full-depth explanation, informative scenarios, and working examples for the Jabberwocky toolkit - for installation instructions, see the [Jabberwocky](https://github.com/sap218/jabberwocky) repository. Here 

### see [SCENARIO](SCENARIO.md) for a working tutorial

## About the Commands

---

## bandersnatch
`bandersnatch` curates synonyms for a list of key terms / or words of interest from an ontology of your choice, you provide a list of ontology synonym tags. **note**: it is recommended your list of keywords are exactly the classes from your chosen ontology (all in lowercase).

#### Usage
```
$ jab-bandersnatch --help
Usage: jab-bandersnatch [OPTIONS]

Options:
  -o, --ontology TEXT     file of ontology.  [required]
  -s, --synonymtags TEXT  list of XML tags for synonym curation.  [required]
  -k, --keywords TEXT     list of class labels you want to use to search.
                          [required]
  --help                  Show this message and exit.
```
#### Running
```
$ jab-bandersnatch -o pocketmonsters.owl -s ontology_synonym_tags.txt -k words_of_interest.txt
```

###### Output
* a `.json` file: `output_ontology_label_synonyms.json` of the classes and synonyms for your reference - this can be used for the `catch` command
* see [`jabberwocky-tests`](https://github.com/sap218/jabberwocky-tests) for an example of `bandersnatch` with input and outputs

---

## catch
`catch` essentially "catches" key elements / sentences from textual data using a `.json` of key terms and their synonyms. **note**: if a `.json` is provided, you need specify the parameter for the field that contains the textual data to process.

#### Usage
```
$ jab-catch --help
Usage: jab-catch [OPTIONS]

Options:
  -k, --keywords TEXT        list of terms and synonyms you want for grep, can
                             be from the ontology output.  [required]
  -t, --textfile TEXT        JSON or TXT file of text you want annotate.
                             [required]
  -p, --parameter TEXT       parameter of the the JSON text data.
  -i, --innerparameter TEXT  inner parameter of the the JSON text data if
                             expecting replies.
  --help                     Show this message and exit.
```
#### Running
```
$ jab-catch -k output_ontology_label_synonyms.json -t example_textfile.json -p user-comment -i inner-user-comment-reply
```

###### Output
* a `.json` file: `output_terms_match.json` which includes the posts for each word of interest
* a `.txt` file: `output_terms_match_raw.txt` which includes all elements / sentences from the text file which includes a term of interest
* see [`jabberwocky-tests`](https://github.com/sap218/jabberwocky-tests) for an example of `catch` with input and outputs

---

## bite
`bite` runs a tf-idf statistical analysis: searching for important terms in a text corpus. a user can use a list of key terms to remove from the text in order to avoid being in the statistical model - meaning other terms may be ranked higher. **note**: with the `.json` input you need specify the field inside the JSON that contains the textual data to process.

#### Usage
```
$ jab-bite --help
Usage: jab-bite [OPTIONS]

Options:
  -k, --keywords TEXT        list of terms and synonyms you want to remove
                             from tf-idf analysis.
  -t, --textfile TEXT        JSON or TXT file of text you want annotate.
                             [required]
  -p, --parameter TEXT       parameter of the the JSON text data.
  -i, --innerparameter TEXT  inner parameter of the the JSON text data if
                             expecting replies.
  -g, --graph TEXT           make True if you want a plot of top 30 terms.
  -l, --limit TEXT           change if want a different plot limit.
  --help                     Show this message and exit.

```
#### Running
```
$ jab-bite -k output_ontology_label_synonyms.json -t example_textfile.json -p user-comment -i inner-user-comment-reply -g True -l 20
```

###### Output
* a `.tsv` file: `tfidf_results.tsv` of all terms and their tf-idf score
* a `.pdf` file: `tfidf_plot.pdf` the plot output which is requested if a user makes `--graph True` and presents the 20 (default=30) top scoring terms
* see [`jabberwocky-tests`](https://github.com/sap218/jabberwocky-tests) for an example of `bite` with input and outputs

---

## arise
`arise` inserts synonyms in an ontology: **you** define these synonyms (e.g. "exact", "broad", "related", or "narrow") - these new synonyms may be based on the tf-idf statistical analysis from `bite`.

#### Usage
```
$ jab-arise --help
Usage: jab-arise [OPTIONS]

Options:
  -o, --ontology TEXT  file of ontology.  [required]
  -f, --tfidf TEXT     TSV file of the synonyms you want to add, can be based
                       from the tf-idf results.  [required]
  --help               Show this message and exit.
```
#### Running
```
$ jab-arise -o pocketmonsters.owl -f tfidf_new_synonyms.tsv
```

###### Output
* a `.owl` file: `updated_ontology.owl`
* see [`jabberwocky-tests`](https://github.com/sap218/jabberwocky-tests) for an example of `arise` with input and outputs


