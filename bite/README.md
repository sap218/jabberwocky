# README

`bite` runs a tf-idf statistical analysis: searching for important terms in a text corpus. a user can use a list of key terms to remove from the text in order to avoid being in the statistical model - meaning other terms may be ranked higher. **note**: again with `catch`, if you provide a `.json` of text data, you need specify the field that contains the textual data to process. Using `-g True` means you'll get a bar plot of the (default) 30-top terms.
```
$ jab-bite -k label_with_synonyms.json -t twitter_posts.txt -g True
```

***

End of page.
