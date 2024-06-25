# README - `catch`

## `corpus`
- file with each post/sentence on a new line

## `annotation_file`
- annotation file with concepts on a new line
- can be `snatch` output
- if left empty, script will still run

## `filter_level`
- parameter for which stop words list to use
- "light" is a smaller list consisting only of 179 stop words
- "heavy" is much larger list consisting of 1160 stop words

## `grep_format`
- output in grep (`True`) format or with tags (`False`) that were found in post

## `not_annotated`
- to output posts that were NOT annotated make `True`

## `graph`
- plot wordcloud
- make `annotation_file` empty to only plot

### `cm`
- plotting colour - users can provide [any of interest](https://matplotlib.org/stable/users/explain/colors/colormaps.html)
- recommended to use `Set3` (pastel) or `viridis` (purple -> green)

***

End of page
