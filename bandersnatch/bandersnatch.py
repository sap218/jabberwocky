#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: May 2021
@author: Samantha C Pendleton
@description: to curate terms and their synonyms from an ontology file
@GitHub: github.com/sap218/jabberwocky

@useful links:
    # https://stackoverflow.com/questions/35898699/why-is-beautifulsoup-altering-the-format-of-my-xml
"""

import click 
from bs4 import BeautifulSoup
import json
import re

def clean_text(post):
    post = post.replace("-", "")
    post = (re.sub("[^A-Za-z0-9']+", " ", post)) # keeping '
    post = (re.sub("'", "", post))
    return post.lower().strip()

####################################################
####################################################

@click.command()
@click.option('-o', '--ontology', 'ontology', required=True, help='file of ontology.')
@click.option('-s', '--synonymtags', 'synonymtags', required=True, help='list of XML tags for synonym curation.')
@click.option('-k', '--keywords', 'keywords', required=True, help='list of class labels you want to use to search.')
def main(ontology, synonymtags, keywords):

    #with open("../test_data/pocketmonsters.owl", "rt") as o:
    with open(ontology, "rt") as o:
        ontology_file = o.read()  
    ontology_soup = BeautifulSoup(ontology_file,'xml') # BEAUTIFUL SOUP really is beautiful
    
    
    synonym_tags = [] #synonym_tags = ["oboInOWL:hasExactSynonym", "oboInOWL:hasRelatedSynonym"] # an example
    #with open("input/ontology_synonym_tags.txt", "r") as t:
    with open(synonymtags, "r") as t:
        for tag in t:
            synonym_tags.append(tag.strip("\n"))
    
    ####################################################
    
    find_all_concepts = ontology_soup.find_all('owl:Class') # this finds all concepts in the ontology
    concept_all_synonyms = {}
    for concept in find_all_concepts:
        label = concept.find("rdfs:label").get_text().lower() # gets label for concept
        list_synonyms = []
        for synonym_format in synonym_tags: 
            synonym_finding = concept.find_all(synonym_format) # a concept could have multiple "exact synonyms" 
            flatten = [clean_text(x.get_text().lower()) for x in synonym_finding] 
            list_synonyms.append(flatten)
        flatten = [item for sublist in list_synonyms for item in sublist]
        concept_all_synonyms[clean_text(label)] = flatten
    
    ####################################################
    
    words_of_interest = []
    #with open("input/words_of_interest.txt", "r") as t:
    with open(keywords, "r") as t:
        for word in t:
            words_of_interest.append(word.strip("\n").strip(" ").lower()) # words of interest
    
    searching_concepts_of_interest = {}
    for label,synonyms in concept_all_synonyms.items(): # matches the terms together!
        if label in words_of_interest:
            searching_concepts_of_interest[label] = synonyms
    
    ####################################################
    
    with open('output_ontology_label_synonyms.json', 'w') as j:
        json.dump(searching_concepts_of_interest, j, indent=4)
    
####################################################
####################################################

if __name__ == "__main__":
    main()