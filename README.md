# Jabberwocky

[![DOI](https://joss.theoj.org/papers/10.21105/joss.02168/status.svg)](https://doi.org/10.21105/joss.02168) 

## Functionality
Jabberwocky is a toolkit for NLP and **ontologies**. 
Read the [documentation](https://sap218.github.io/jabberwocky/) for more detail.

|  | script | description
| --- | --- | ---
| 1. | `converter` | convert an excel to an ontology
| 2. | `snatch metadata` | extract metadata from classes
| 3. | `catch text` | annotate corpus with key terms/phrases
| 4. | `rank terms` | rank terms in order of importance
| 5. | `update entities` | update ontology with new classes and metadata
| 6. | `ontology plotting` | plot an ontology via web or tree format

When combining these Jabberwocky functions, users can create an NLP workflow.

![workflow](/docs/workflow.png)

## Running
Within each directory, there is a file `params_*.py` which users can edit.
Meaning users shouldn't need to edit the main/primary script.

Check the individual directory `READMEs` for parameter information.

## Resources

+ **Prerequisites** - check [`requirements.py`](https://github.com/sap218/jabberwocky/blob/master/requirements.py) for a list of packages and versions.

+ **Changelog / Version** - see the [**Changelog**](https://github.com/sap218/jabberwocky/blob/master/Changelog.md) (ordered by newest first).

+ **Contributing / Issues** - please read the [**Contributing Guidelines**](https://github.com/sap218/jabberwocky/blob/master/Contributing.md) also to see past contributors.

+ **License** - this [license](https://github.com/sap218/jabberwocky/blob/master/LICENSE) is **MIT** so users only need to cite if using (see citation below).

## Citing

```
@article{Pendleton2020,
  doi = {10.21105/joss.02168},
  url = {https://doi.org/10.21105/joss.02168},
  year = {2020},
  publisher = {The Open Journal},
  volume = {5},
  number = {51},
  pages = {2168},
  author = {Samantha C. Pendleton and Georgios V. Gkoutos},
  title = {Jabberwocky: an ontology-aware toolkit for manipulating text},
  journal = {Journal of Open Source Software}
}
```

## AOB

+ The poem, Jabberwocky, written by Lewis Carrol, is described as a *nonsense* poem :dragon:
+ You may think, why not use a Large Language Model (LMM)? Well I wrote a blog to compare w/ LLMs and how they overdo simple tasks, [read here](https://sap218.uk/posts/llms/).

***

End of page
