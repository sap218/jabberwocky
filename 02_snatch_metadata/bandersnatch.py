#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2024
@author: Samantha Pendleton
@description: curate classes (& synonyms) from an ontology
@GitHub: github.com/sap218/jabberwocky

@useful links:
    # https://stackoverflow.com/questions/35898699/why-is-beautifulsoup-altering-the-format-of-my-xml
"""

from datetime import datetime
start_timestamp = datetime.today().strftime('%Y%m%d-%H%M%S')

import logging
import sys

from bs4 import BeautifulSoup

from params_snatch import *

if is_this_a_test:
    dir_output = "test/"
    ontology_filepath = "../test/CelestialObject/space.owl"
    
    ontology_tags_file = "../test/CelestialObject/corpus/ontology_tags.txt"
    
    classes_of_interest = "../test/CelestialObject/corpus/classes_of_interest.txt"
    #classes_of_interest = ""

#########################

# Logging

logging.basicConfig(
    filename=f"{dir_output}{start_timestamp}.log",
    encoding="utf-8",
    filemode="a",
    format="{asctime} - {levelname} - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M",
    level=logging.INFO,
    force=True
    )
logging.info(f"Starting script for snatching metadata from {ontology_file}")

if is_this_a_test: logging.warning("THIS IS A TEST")

##################################################

# Ontology files

try:
    with open(ontology_filepath, "rt") as o:
        ontology_file = o.read()  
    ontology_soup = BeautifulSoup(ontology_file,'xml') # BEAUTIFUL SOUP really is beautiful
    del o, ontology_file
    logging.info("Sucessfully imported ontology file")
except:
    logging.critical(f"Cannot find ontology file - check this:\t{ontology_filepath}")
    if not ontology_filepath.endswith(".owl"):
        logging.critical("Seems like the the ontology file does not end with .owl")
    sys.exit(1)

try:
    annotation_tags = []
    with open(ontology_tags_file, "r") as t:
        for tag in t:
            annotation_tags.append(tag.strip("\n"))
    del tag, t
    logging.info("Sucessfully imported ontology tags file")
except:
    logging.critical(f"Cannot find ontology tags file - check this:\t{ontology_tags_file}")
    if not ontology_tags_file.endswith(".txt"):
        logging.critical("Seems like the the ontology tags file does not end with .txt")
    sys.exit(1)    
if len(annotation_tags) == 0:
    logging.critical("Ontology tags file has no entries")
    sys.exit(1)   

#########################

# Snatching all classes and synonyms

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

##################################################

# Classes of interest

if len(classes_of_interest) > 0:
    try:
        words_of_interest = []
        with open(classes_of_interest, "r") as t:
            for word in t:
                words_of_interest.append(word.strip("\n").strip(" "))
        del t, word
        logging.info("Sucessfully imported classes of interest")
        
        words_of_interest = list(filter(None, words_of_interest))
        if words_of_interest == 0:
            logging.warning("Classes of interest is an empty file")
        
    except FileNotFoundError:
        logging.critical(f"Cannot find classes of interest file - check this:\t{classes_of_interest}")
        if not classes_of_interest.endswith(".txt"):
            logging.critical("Seems like the the classes of interest file does not end with .txt")
        sys.exit(1)  

else:
    words_of_interest = []
    logging.info("User did not provide a list of ontology classes so will proceed to extract all classes and requested metadata")

##################################################

if words_of_interest: 
    search_concepts = {key: classes_and_annotations[key] for key in words_of_interest}
    output_name = "bandersnatch_output_requested"
    logging.info("Requested classes exported")
else:
    search_concepts = classes_and_annotations.copy()
    output_name = "bandersnatch_output_allClasses"
    logging.info("All classes and metadata exported")

##################################################

search_concepts = [key_val for key, value in search_concepts.items() for key_val in [key] + value]

with open(f'{dir_output}{output_name}.txt', 'w') as t:
    for word in search_concepts:
        t.write(word + '\n')
del t, word

##################################################

# End of script
