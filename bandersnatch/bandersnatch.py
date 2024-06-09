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

import sys
from bs4 import BeautifulSoup

####################################################

"""PARAMS"""

is_this_a_test = True

if is_this_a_test:
    ontology_name = "test/pocketmonsters"
    ontology_tags = "test/ontology_tags"
    classes_of_interest = "test/words_of_interest" # if empty, extract all annotations of all classes
    output_name = "test/snatch_output"
else:
    ontology_name = input("Ontology:\t")
    ontology_tags = input("Tags file:\t")
    classes_of_interest = input(
        "File with ontology classes of interest (leave blank if using all classes):\t"
        )
    output_name = "snatch_output"

####################################################

with open("%s.owl" % ontology_name, "rt") as o:
    ontology_file = o.read()  
ontology_soup = BeautifulSoup(ontology_file,'xml') # BEAUTIFUL SOUP really is beautiful
del o, ontology_file

annotation_tags = []
with open("%s.txt" % ontology_tags, "r") as t:
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

if len(classes_of_interest) > 0:
    try:
        words_of_interest = []
        with open("%s.txt" % classes_of_interest, "r") as t:
            for word in t:
                words_of_interest.append(word.strip("\n").strip(" ")) # words of interest
        print("User has provided a list of ontology classes of interest - success")
        del t, word
        
    except FileNotFoundError:
        sys.exit("User attempted to provide a list with ontology classes of interest - unsuccessful")

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

with open('%s.txt' % output_name, 'w') as t:
    for word in search_concepts:
        t.write(word + '\n')
del t, word

####################################################

# End of script
