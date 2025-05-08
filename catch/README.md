# README - `catch`

## `test/` & `output/`
- directories for results

***

## `is_this_a_test`
- set to `True` to run the test, see `test/` for the results

***

## `file_corpus`
- a `.txt` file with each post/sentence on a new line

## `file_words_of_interest`
- a `.txt` file with concepts/words of interest separated by a new line
- can be `snatch` output
- script will run if empty so users can use other features - please ensure you check outputs

## `filter_level`
- parameter for which list of stop words to use
- `light` is a small list consisting of 179 stop words
- `heavy` is much larger consisting of 1160 stop words
- `none` to not remove stop words

## `output_format`
- `wtags` = each annotated post **with** the terms that were annotated
- `grep` = output in grep format (simply the annotated posts only)
- `invertedgrep` = posts that were NOT annotated

## `output_name`
- users should edit the output name, these will be stored in `output/`
- all outputs are timestamped to avoid overwriting files

## `plotWORDCLOUD`
- set `True` to plot a wordcloud of `file_corpus`
- if you intend to plot, it is recommended to use a filter level for stop words

### `colormapWC`
- colour scheme for the wordcloud - users can provide [any palette](https://matplotlib.org/stable/users/explain/colors/colormaps.html)
- default is `Set3` (pastel) but a nice recommendation is `viridis` (purple -> green)

## `plotCYANNOTATOR`
- set `True` to output an `HTML` of annotated posts with the highlighted concepts

### `highlightcolour`
- colour of highlighting - default is cyan (`#00bcd4`)

***

End of page
