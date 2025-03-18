# README - `catch`

## `corpus`
- file with each post/sentence on a new line

## `annotation_file`
- file with concepts/keyterms on a new line
- can be `snatch` output
- script will run if empty so users can use other features - please ensure you check outputs

## `filter_level`
- parameter for which list of stop words to use
- `light` is a small list consisting of 179 stop words
- `heavy` is much larger consisting of 1160 stop words
- `none` to avoid removing stop words

## `output_format`
- `wtags` = each annotated post **with** the terms that were annotated
- `grep` = output in grep format (simply the annotated posts only)
- `invertedgrep` = posts that were NOT annotated

## `*_name`
- users can edit the output names for each experiment

## `plotWORDCLOUD`
- plot wordcloud of corpus
- if you intend to plot, it is recommended to use a filter level for stop words

### `cm`
- plotting colour - users can provide [any palette](https://matplotlib.org/stable/users/explain/colors/colormaps.html)
- default is `Set3` (pastel) but a nice recommendation is `viridis` (purple -> green)

## `plotCYANNOTATOR`
- set `True` is users wish to have an output of highlighted tags in posts
- output is `HTML` format

### `highlightcolour`
- colour of highlighting - defult is cyan (`#00bcd4`)

***

End of page
