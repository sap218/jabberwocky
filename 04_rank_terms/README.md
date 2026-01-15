# `rank terms` - `bite`

### `is_this_a_test`
+ set to `True` to run the test, see `test/` for results

***

### `dir_output`
+ any outputs will be stored here (including logs)
+ suggested to use `output/` but users are welcome to create their own dir

***

### `stopWord_filter_level`
+ `light` is a small list consisting of 179 stopwords
+ `heavy` is much larger list of stopwords of 1160
+ `none` to **not remove** stopwords
+ e.g. `stopWord_filter_level = "heavy"`

### `file_concepts_to_remove`
- concepts file with each on a new line to remove from TF-IDF statistical rankings
- can be `snatch` output
- users can leave blank to use all terms in corpus

### `file_corpus`
- file with each post/sentence on a new line
- can be `catch` output (grep)

### `ngram_count`
- a list of n-grams for TF-IDF
- can modify for unigram only `[1]` or bi-grams only `[2]`
- users can also request a list, for example: bi-grams & tri-grams `[2,3]`

***

### `plotTFIDF`
- plot TF-IDF rankings

#### `plotTFIDFlimit` 
- plot limit for top-N terms (default is 30)

#### `plotTFIDFcolormap`
- plotting colour for bars
- recommended to use mediumseagreen, steelblue, or lightcoral

***

End of page
