#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: May 2021
@author: Samantha C Pendleton
@description: to update an ontology
@GitHub: github.com/sap218/jabberwocky

@useful links:
    # https://stackoverflow.com/questions/35898699/why-is-beautifulsoup-altering-the-format-of-my-xml
    # https://www.crummy.com/software/BeautifulSoup/bs4/doc/#insert
"""

import click 
from bs4 import BeautifulSoup
import pandas as pd

@click.command()
@click.option('-o', '--ontology', 'ontology', required=True, help='file of ontology.')
@click.option('-f', '--tfidf', 'tfidf', required=True, help='TSV file of the synonyms you want to add, can be based from the tf-idf results.')
def main(ontology, tfidf):

    #tfidf = 'input/tfidf_new_synonyms.tsv'
    tfidf_df = pd.read_csv(tfidf, sep='\t', header=0)
    
    #ontology = "../test_data/pocketmonsters.owl"
    with open(ontology, "rt") as o:
        ontology_file = o.read()  
    ontology_soup = BeautifulSoup(ontology_file,'xml') # BEAUTIFUL SOUP really is beautiful
    
    finding = ontology_soup.find_all('owl:Class') # finding all owl classes
    for concept in finding:
        label = concept.find("rdfs:label").get_text().lower() # getting labels
        for term_iteration in range(len(tfidf_df)): # going through each row on the tf-idf dataframe
            class_match_label = list(tfidf_df['class'])[term_iteration]
            class_new_synonym = list(tfidf_df['synonym'])[term_iteration]
            class_synonym_tag = list(tfidf_df['type'])[term_iteration]
    
            if label == class_match_label:
                tag = ontology_soup.new_tag(class_synonym_tag)
                tag.string = class_new_synonym 
                concept.insert(1, tag) # insert after line one (line one is declaring the ontology concept)
    
    updated_ont = str(ontology_soup).replace('<?xml version="1.0" encoding="utf-8"?>', '<?xml version="1.0"?>') # replacing first line - very important
    
    with open("updated-ontology.owl", "w") as file: # exporting
        file.write(updated_ont)
        
####################################################

if __name__ == "__main__":
    main()