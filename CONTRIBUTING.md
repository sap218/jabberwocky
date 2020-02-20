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
* don't hesitate to create an issue
* issues can be regarding anything: error reporting, feature request, or questions for help
* add an issue with a clear description & title
* try to know what error you are getting and make sure the input files are correct
* i will label the issue accordingly (see [`labels`](https://github.com/sap218/jabberwocky/labels) - or below (`bug`, `documentation`, `duplicate`, `help`, `request`, `wontfix`))
* please accept that sometimes information may not be fully understood so there could be follow-up questions
* if you have an issue with the `README` please do say so! i encourage help to make it better, perhaps you have a better ideas than me

#### bug
* error reporting if there is a clear issue
* if you know how to fix it yourself, consider doing it and creating a pull request
* e.g. "my list of ontology classes and synonyms is empty and I'm using HPO"

#### documentation
* any issues which i believe can be fixed by better documentation, i will label with `documentation`

#### duplicate
* if you have a question which you believe could have been asked before, ask anyway! I'll label as `duplicate`
* i will try my best to ensure a link to the original issue will be provided

#### help
* if you have a general question about how it works/etc. - check out [`jabberwocky-tests`](https://github.com/sap218/jabberwocky-tests)
* if the tests repository doesn't help, please ask away - no question is stupid
* e.g. "can i use my own created ontology?" (FYI: yes)

#### request
* have an idea as a new feature? please tell me! 
* if you know how to make it yourself, consider doing it and creating a pull request

#### wontfix
* sometimes people can confuse tools as something they are not - if there is an `bug` or `request` which i believe is not suitably designed for jabberwocky, i will label accordingly
* after labelling as `wontfix` i will comment why, giving you a few days (perhaps to give a rebuttal) before i close the issue from lack of response/activity
* please accept this label, if i think a different tool is doing what you want i will redirect you

