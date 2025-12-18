# README - `bite` 

## `corpus`
- file with each post/sentence on a new line
- can be `catch` output (grep)

## `concepts_to_remove`
- concepts file with each on a new line to remove from TF-IDF statistical rankings
- can be `snatch` output
- users can leave blank to use all terms in corpus

## `filter_level`
- parameter for which stop words list to use
- "light" is a smaller list consisting only of 179 stop words
- "heavy" is much larger list consisting of 1160 stop words

## `ngram_count`
- a list of n-grams for TF-IDF
- can modify for unigram only `[1]` or for bi-grams & tri-grams `[2,3]`

## `graph`
- plot TF-IDF rankings

### `cm`
- plotting colour for bars
- recommended to use mediumseagreen, steelblue, or lightcoral

### `limit` 
- plot limit for top-N terms (default is 30)

***

End of page
