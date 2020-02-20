# Contributing Guildelines / Issues for jabberwocky :dragon_face:


## Contributing Code
* know how to fix a bug or want a new feature, consider either creating an issue or opening a pull request
* if i think it is suited i will merge to master branch
* frequent contributors will be added to a contributors list for thanks and acknowledgement
* **note**: additional code should be commented and w/ your username to acknowledge contribution, e.g. <br> 
```
new_list = []
for word in old_list:      # cycles through old list
  if len(word) > 10:       # if word greater than 10 characters
    new_list.append(word)  # append to new list
    print(word)            # printing word as users may want to see as a reference - @yourusername
``` 


## Issues
when errors appear and you don't know why - it's frustrating. 

* to make it easier for me to understand, when creating an issue you can include in your description one of the labels
* see [`labels`](https://github.com/sap218/jabberwocky/labels) in issues - or below (`bug`, `documentation`, `duplicate`, `help`, `request`, `wontfix`)
* this way i will be able to understand if your issue is possibly a `help` question rather than a `bug` notice

#### bug
* first know what error you are getting: e.g. if your `ontology_dict_class_synonyms.json` file is empty then your keywords may not be exact classes from your chosen ontology
* add an issue with a clear description & title
* please accept that sometimes information may not be fully understood so there could be follow-up questions

#### documentation
* if you have an issue with the `README` please do say so! i encourage help to make it better, perhaps you have a better ideas than me
* any issues which i believe can be fixed by a better documentation i will label it accordingly

#### duplicate
* if you have a question which you believe could have been asked before, ask anyway! I'll label as `duplicate`
* i will try my best to ensure a link to the original issue will be provided

#### help
* if you have an question about how it works, perhaps check out [`jabberwocky-tests`](https://github.com/sap218/jabberwocky-tests)
* if the tests repository doesn't help, please ask away - no question is stupid

#### request
* have an idea as a new feature? please tell me! 

#### wontfix
* sometimes people can confuse tools as something they are not, if there is an issue which i believe is not something designed for jabberwocky i will label accordingly
* after labelling as `wontfix` i will comment why, giving you a few days to perhaps give a rebuttal otherwise i will close the issue if lack of activity
* please accept this label, if i think a different tool is doing what you want i will redirect you



