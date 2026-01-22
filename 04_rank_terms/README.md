# `rank terms` - `bite`

### `is_this_a_test`
+ set to `True` to run the test, see `test/` for results

***

### `dir_output`
+ any outputs will be stored here (including logs)
+ suggested to use `output/` but users are welcome to create their own dir

***

### `stopWord_filter_level`
+ `light` = small list consisting of 179 stopwords
+ `heavy` = much larger list of stopwords of 1160
+ `none` = to **not remove** stopwords
+ e.g. `stopWord_filter_level="heavy"`

### `file_concepts_to_remove`
+ a `.txt` file with concepts/words of interest separated by a new line 
+ these concepts will be removed from the corpus to improve TF-IDF statistical rankings by removing noise
+ can be an output from `snatch`
+ users can leave blank to use all terms in corpus

### `file_corpus`
+ a `.txt` file with individual posts/sentences on a new line
+ can be `catch` output, e.g. `grep` or `invertedgrep`

### `ngram_count`
+ a list of n-grams for TF-IDF
+ can modify for unigram only `[1]` or bi-grams only `[2]`
+ users can also request a list, for example: bi-grams & tri-grams `[2,3]`
+ e.g. `ngram_count=[1,2]` or `ngram_count = [3]`

***

### `plotTFIDF`
+ plot TF-IDF rankings

#### `plotTFIDFlimit` 
+ plot limit for top-N terms (default is 30)

#### `plotTFIDFcolormap`
+ plotting colour for bars, some recommendations: `mediumseagreen`, `steelblue`, or `lightcoral`

***

End of page
