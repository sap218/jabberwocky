#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2024
@author: Samantha C Pendleton
@description: annotate ontology classes
@GitHub: github.com/sap218/jabberwocky

@useful links:
    # https://www.crummy.com/software/BeautifulSoup/bs4/doc/#insert
"""

from bs4 import BeautifulSoup
import pandas as pd

from params_arise import *

####################################################

with open("%s.owl" % ontology_name, "rt") as o:
    ontology_file = o.read()  
ontology_soup = BeautifulSoup(ontology_file,'xml') # BEAUTIFUL SOUP really is beautiful
del o, ontology_file

####################################################

try:
    annotations = pd.read_csv('%s.tsv' % annotation_file, sep='\t', header=0)
except:
    annotations = pd.read_csv('%s.csv' % annotation_file, header=0)

####################################################

finding = ontology_soup.find_all('owl:Class') # finding all owl classes
for concept in finding:
    label = concept.find("rdfs:label").get_text()#.lower() # getting labels
    
    for term_iteration in range(len(annotations)): # going through each row on the tf-idf dataframe
    
        class_match_label = list(annotations['class'])[term_iteration]
        class_new_annotations = list(annotations['annotation'])[term_iteration]
        new_annotation_tag = list(annotations['tag'])[term_iteration]

        if label == class_match_label:
            tag = ontology_soup.new_tag(new_annotation_tag)
            tag.string = class_new_annotations 
            concept.insert(1, tag) # insert after line one (line one is declaring the ontology concept)

####################################################

updated_ont = str(ontology_soup).replace('<?xml version="1.0" encoding="utf-8"?>', '<?xml version="1.0"?>') # replacing first line - very important

####################################################

with open("%s_updated.owl" % output_name, "w") as file: # exporting # encoding="utf-8"
    file.write(updated_ont)

####################################################

# End of script
