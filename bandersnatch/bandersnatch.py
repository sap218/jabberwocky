#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2024
@author: Samantha C Pendleton
@description: curate classes (& synonyms) from an ontology
@GitHub: github.com/sap218/jabberwocky

@useful links:
    # https://stackoverflow.com/questions/35898699/why-is-beautifulsoup-altering-the-format-of-my-xml
"""

from bs4 import BeautifulSoup

####################################################

"""PARAMS"""

ontology_name = "pocketmonsters"
ontology_tags = "ontology_tags"

to_use_own_defined_concepts = True
# if True, need a txt of ontology classes
# if False, script extracts all annotations of all class
classes_of_interest = "words_of_interest" # file if above is True

####################################################

with open("test/%s.owl" % ontology_name, "rt") as o:
    ontology_file = o.read()  
ontology_soup = BeautifulSoup(ontology_file,'xml') # BEAUTIFUL SOUP really is beautiful
del o, ontology_file

annotation_tags = []
with open("test/%s.txt" % ontology_tags, "r") as t:
    for tag in t:
        annotation_tags.append(tag.strip("\n"))
del tag, t

####################################################

find_all_concepts = ontology_soup.find_all('owl:Class') # this finds all concepts in the ontology
classes_and_annotations = {}
for concept in find_all_concepts:
    label = concept.find("rdfs:label").get_text() # gets label for concept
    list_annotations = []
    for tag_format in annotation_tags: 
        finding_tags = concept.find_all(tag_format) # a concept could have multiple "exact synonyms" 
        flatten = [x.get_text() for x in finding_tags] 
        list_annotations.extend(flatten)
    classes_and_annotations[label] = list_annotations
del find_all_concepts, flatten, label, list_annotations, finding_tags, tag_format, annotation_tags

####################################################

if to_use_own_defined_concepts:
    try:
        words_of_interest = []
        with open("test/%s.txt" % classes_of_interest, "r") as t:
            for word in t:
                words_of_interest.append(word.strip("\n").strip(" ")) # words of interest
        print("User has provided a list of ontology classes of interest - success")
        del t, word
        
    except FileNotFoundError:
        words_of_interest = None
        print("User has provided a list of ontology classes of interest - file not found! Using all classes for annotations")

else:
    words_of_interest = None
    print("User not providing a list of ontology classes of interest - using all classes for annotations")

####################################################

if words_of_interest: 
    search_concepts = {key: classes_and_annotations[key] for key in words_of_interest}
else:
    search_concepts = classes_and_annotations.copy()

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
