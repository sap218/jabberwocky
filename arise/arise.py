#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: Tue Jan 21 12:15:00 2020
@author: Samantha C Pendleton
@description: to catch
@GitHub: github.com/sap218/jabberwocky
"""

import click 
from bs4 import BeautifulSoup
import pandas as pd

####################################################
####################################################

def souping(ontology_file):
    soup = BeautifulSoup(open(ontology_file, 'rb'), 'xml') # r
    return soup # https://stackoverflow.com/questions/35898699/why-is-beautifulsoup-altering-the-format-of-my-xml

def inserting_synonyms(soup, df):
    finding = soup.find_all('owl:Class') # finding all owl classes
    for concept in finding:
        try:
            label = concept.find("rdfs:label").get_text().lower() # getting labels
            for term in df['class']: # matching labels to user's classes
                if label == term:
                    tag = soup.new_tag("oboInOwl:has%sSynonym" % (str(df.loc[df['class'] == term, 'type'].iloc[0]).capitalize()))
                    tag.string = str(df.loc[df['class'] == term, 'synonym'].iloc[0]) # iloc for the string not series
                    concept.insert(1, tag) # insert after line one 
        except: # sometimes there isn't a label
            pass
    return soup, finding # https://www.crummy.com/software/BeautifulSoup/bs4/doc/#insert

####################################################
####################################################
    
def ontology_purl(ontology_file, tfidf_df):
    soup = souping(ontology_file) # importing ontology
    
    class_synonyms_df = pd.read_csv(tfidf_df) # csv of user's synonyms and classes
    updated_ont = inserting_synonyms(soup, class_synonyms_df) # updating ontology w/ correct synonym types
    
    edited_ont = str(updated_ont[0]).replace('<?xml version="1.0" encoding="utf-8"?>', '<?xml version="1.0"?>') # replacing first line
    
    return edited_ont, updated_ont[1]

####################################################
####################################################
####################################################
####################################################
####################################################

def opening_ontology(ontology_file): # opening the ontology
    ontology = open(ontology_file, "rt")
    contents = ontology.read()
    ontology.close()
    soup = BeautifulSoup(contents,'xml') # souped it 
    return soup

def ontology_classes(soup): # getting classes
    concepts = {}
    finding = soup.find_all('AnnotationProperty', {'abbreviatedIRI':'rdfs:label'}) 
    for item in finding:
        try:
            iri = item.find_next_sibling('IRI').get_text() # plus IRIs
            #iri = iri[1:]
            classes = item.find_next_sibling('Literal').get_text()
            concepts.update({classes.lower() : iri})
        except:
            pass
    return concepts

def pairing_iri(ontology_class_terms, df):
    matched_csv = {} # matching the synonyms w/ iri
    for synonym in df['synonym']:
        for term in ontology_class_terms:
            if (str(df.loc[df['synonym'] == synonym, 'class'].iloc[0])) == term:
                matched_csv[synonym] = ontology_class_terms[term]
    return matched_csv

def appending_to_ont(soup, matched_csv, class_synonyms_df):
    finding = soup.find_all('Ontology') # finding all owl classes
    for concept in finding:
        for synonym in matched_csv:
            concept.append(BeautifulSoup(('<AnnotationAssertion><AnnotationProperty abbreviatedIRI="oboInOWL:has%sSynonym"/><IRI>%s</IRI><Literal>%s</Literal></AnnotationAssertion>' % (((str(class_synonyms_df.loc[class_synonyms_df['synonym'] == synonym, 'type'].iloc[0]).capitalize())), 
                                                                                                                                                                                     matched_csv[synonym], synonym)),
                                           'xml',
                                           ))
    return soup

####################################################
####################################################
    
def ontology_w3(ontology_file, tfidf_df):
    soup = opening_ontology(ontology_file) # Reading in the ontology
    ontology_class_terms = ontology_classes(soup) # Extracting the classes
    
    class_synonyms_df = pd.read_csv(tfidf_df)
    matched_csv = pairing_iri(ontology_class_terms, class_synonyms_df) # Matching synonyms w/ IRI using classes
    updated_ontology = appending_to_ont(soup, matched_csv, class_synonyms_df) # Adding the synonyms 
        
    editing_ontology = str(updated_ontology).replace('<?xml version="1.0" encoding="utf-8"?>','') # removing all
    index = editing_ontology.find('<Ontology')
    output_line = '<?xml version="1.0"?>\n' + editing_ontology[index:] # adding at first element
    
    updated_ont = output_line
    
    return updated_ont

####################################################
####################################################
####################################################
####################################################
####################################################
####################################################
####################################################
####################################################
####################################################
####################################################

@click.command()
@click.option('-o', '--ontology', 'ontology', required=True, help='file of ontology.')
@click.option('-f', '--tfidf', 'tfidf', required=True, help='tf-idf CSV file of the synonyms you want to add.')
def main(ontology, tfidf):
    
    updated_ont = ontology_purl(ontology, tfidf)
    if len(updated_ont[1]) == 0:
        updated_ont = ontology_w3(ontology, tfidf)
        with open("updated-ontology.owl", "w") as file: # exporting
            file.write(updated_ont)
    else:
        with open("updated-ontology.owl", "w") as file: # exporting
            file.write(updated_ont[0])
        
        
####################################################
####################################################

if __name__ == "__main__":
    main()
