# README

`catch` essentially "catches" key elements / sentences from textual data using a `.json` of key terms and their synonyms, you can use the outcome from `bandersnatch`. A user will also provide a `.txt` or `.json` of the text data. **note**: if a `.json` of text data is provided, you need specify the parameter for the field that contains the textual data to process.
```
$ jab-catch -k label_with_synonyms.json -t facebook_posts.json -p user-comment -i inner-user-comment-reply
```

***

End of page.
