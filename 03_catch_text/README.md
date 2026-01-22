# `catch text`

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

### `file_corpus`
+ a `.txt` file with individual posts/sentences on a new line

***

### `plotWORDCLOUD`
+ set `True` to plot a wordcloud of `file_corpus`
+ will filter corpus of the stopword filter level

#### `plotWORDCLOUDcolormap`
+ colour scheme for the wordcloud - users can provide [any palette](https://matplotlib.org/stable/users/explain/colors/colormaps.html)
+ some other recommendations: "Set3" (default, pastels), "plasma" (purple -> red -> yellow), "viridis" (purple -> green -> yellow)

***

### `stop_here`
+ a `True` or `False` boolean, if `True` the script will stop here (essentially useful if users only want a wordcloud)
+ e.g. `stop_here=False` means the whole script will run and so users need to complete the below...

***

### `file_words_of_interest`
+ a `.txt` file with concepts/words of interest separated by a new line 
+ can be an output from `snatch`

### `output_format`
+ `wtags` = each annotated post **with** the terms that were annotated separated by `|`
+ `grep` = output in grep format (meaning **only** the annotated posts)
+ `invertedgrep` = posts that were **NOT** annotated
+ e.g. `output_format="wtags"`

### `output_style`
+ `original` = output the original format (without any text cleaning)
+ `formatted` = output in the cleaned format
+ e.g. `output_style="original"`

***

### `plotCYANNOTATOR`
+ set `True` to output `HTML` of corpus with the highlighted matches (text is cleaned/formatted)

#### `plotCYANNOTATORhighlightcolour`
+ colour of highlighting
+ e.g. `plotCYANNOTATORhighlightcolour="#00bcd4"` or `plotCYANNOTATORhighlightcolour="cyan"`

***

End of page
