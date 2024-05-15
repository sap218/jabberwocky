#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2024
@author: Samantha C Pendleton
@description: to curate terms and their synonyms from an ontology file
@GitHub: github.com/sap218/jabberwocky

@useful links:
    # https://stackoverflow.com/questions/35898699/why-is-beautifulsoup-altering-the-format-of-my-xml
"""

from bs4 import BeautifulSoup

####################################################

# with open(ontology, "rt") as o:
with open("test/pocketmonsters.owl", "rt") as o:
    ontology_file = o.read()  
ontology_soup = BeautifulSoup(ontology_file,'xml') # BEAUTIFUL SOUP really is beautiful
del o, ontology_file

synonym_tags = []
#with open(synonymtags, "r") as t:
with open("test/ontology_tags.txt", "r") as t:
    for tag in t:
        synonym_tags.append(tag.strip("\n"))
del tag, t

####################################################

find_all_concepts = ontology_soup.find_all('owl:Class') # this finds all concepts in the ontology
classes_and_synonyms = {}
for concept in find_all_concepts:
    label = concept.find("rdfs:label").get_text() # gets label for concept
    list_synonyms = []
    for synonym_format in synonym_tags: 
        synonym_finding = concept.find_all(synonym_format) # a concept could have multiple "exact synonyms" 
        flatten = [x.get_text() for x in synonym_finding] 
        list_synonyms.extend(flatten)
    classes_and_synonyms[label] = list_synonyms
del find_all_concepts, flatten, label, list_synonyms, synonym_finding, synonym_format, synonym_tags

####################################################

to_use_own_defined_concepts = False

if to_use_own_defined_concepts:
    try:
        words_of_interest = []
        # with open(keywords, "r") as t:
        with open("test/words_of_interest.txt", "r") as t:
            for word in t:
                words_of_interest.append(word.strip("\n").strip(" ")) # words of interest
        print("Concepts file found")
        del t, word
        
    except FileNotFoundError:
        words_of_interest = None
        print("Concepts file not found - using all ontology classes and synonyms (from tags)")

else:
    words_of_interest = None
    print("Using all ontology classes and synonyms (from tags)")

####################################################

if words_of_interest: 
    search_concepts = {key: classes_and_synonyms[key] for key in words_of_interest}
else:
    search_concepts = classes_and_synonyms.copy()

####################################################

#with open('test/snatch_output.json', 'w') as j:
#    json.dump(search_concepts, j, indent=4)
#del j

####################################################

search_concepts = [key_val for key, value in search_concepts.items() for key_val in [key] + value]

with open('test/snatch_output.txt', 'w') as t:
    for word in search_concepts:
        t.write(word + '\n')
del t, word


####################################################

# End of script
