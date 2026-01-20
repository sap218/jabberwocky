#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2025
@author: Samantha Pendleton
@description: convert an excel to an owl ontology
@GitHub: github.com/sap218/jabberwocky
"""

from datetime import datetime
start_timestamp = datetime.today().strftime('%Y%m%d-%H%M%S')

import logging
import sys

from rdflib import Graph, Namespace, URIRef, Literal
from rdflib import RDF, RDFS, OWL, DCTERMS

import pandas as pd
import re

####################################################

from params_gimble import *

if is_this_a_test:
    dir_output = "test/"
    #excel_file_location = "../test/CelestialObject/excel/"
    excel_file = "../test/CelestialObject/excel/space.xlsx"

    the_name = "space"
   
    #git_uid = "sap218"
    #git_repo = "CelestialObject"
    #namespace = f"https://github.com/{git_uid}/{git_repo}/blob/master/{the_name}.owl"
    git_uid_repo = "sap218/CelestialObject"
    namespace = f"https://raw.githubusercontent.com/{git_uid_repo}/main/{the_name}.owl"
    
    iri_prefix = "UFO"
    ontology_description = "A brief ontology capturing concepts in our solar system."
    developers = ["Samantha Pendleton"]
    contributors = []
    version = "v0.1"
    licensed = "https://creativecommons.org/licenses/by-nc/4.0/"

    defined_annotations = {
        "dbXref": "http://www.geneontology.org/formats/oboInOwl#DbXref",
        "synonym": f"{namespace}#hasSynonym",
        "definition": "http://www.w3.org/2000/01/rdf-schema#comment"
        }
    
    #cols_to_subset = ["class","subclass"]
    #cols_for_metadata = list(defined_annotations)
    #cols_to_subset.extend(cols_for_metadata)
    
#else:
#    cols_for_metadata = list(defined_annotations)
#    cols_to_subset.extend(cols_for_metadata)

cols_for_metadata = list(defined_annotations)

the_name = the_name.strip().replace(" ", "-")

####################################################

# Logging

logging.basicConfig(
    filename=f"{dir_output}{start_timestamp}_{the_name}.log",
    encoding="utf-8",
    filemode="a",
    format="{asctime} - {levelname} - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M",
    level=logging.INFO,
    force=True
    )
logging.info(f"Starting script for gimbles' {the_name} ontology")

if is_this_a_test: logging.warning("THIS IS A TEST")

# logging.info(
# logging.warning(
# logging.error(
# logging.critical(

####################################################

# Excel

try:
    xls = pd.ExcelFile(excel_file)
    logging.info("Sucessfully imported excel file")
except:
    logging.critical(f"Cannot find excel file - check this:\t{excel_file}")
    if not excel_file.endswith(".xlsx"):
        logging.critical("Seems like the the excel file does not end with .xlsx")
    sys.exit(1)
    

domains = xls.sheet_names
logging.info(f"A total of {len(domains)} superclasses found")

####################################################
####################################################
####################################################

# Defining ontology

ufo = Namespace(namespace+"#")

o = Graph()

o.bind(f"{iri_prefix}", ufo) # binding to prefixes (so they show up in the RDF output)
#o.bind("ufo", ufo)

####################################################

# Defining metadata

o.add((URIRef(namespace), RDF.type, OWL.Ontology))
o.add((URIRef(namespace), RDFS.label, Literal("%s ontology (%s)" % (the_name.capitalize(), iri_prefix.upper()) )))
o.add((URIRef(namespace), RDFS.comment, Literal(f"{ontology_description}")))
#o.add((URIRef(namespace), RDFS.seeAlso, URIRef(f"https://github.com/{git_uid}/{git_repo}")))
o.add((URIRef(namespace), RDFS.seeAlso, URIRef(f"https://github.com/{git_uid_repo}")))

#o.add((URIRef(namespace), URIRef(namespace+"#version"), Literal(f"{version}")))
#o.add((URIRef(namespace), URIRef(w3+"version"), Literal(f"{version}")))

o.add((URIRef(namespace), OWL.versionInfo, Literal(f"{version}")))

#o.add((URIRef(namespace), URIRef(namespace+"#license"), URIRef(f"{licensed}")))

o.add((URIRef(namespace), DCTERMS.license, URIRef(f"{licensed}")))

if developers:
    for d in developers:
        o.add((URIRef(namespace), URIRef(namespace+"#Developer"), Literal(d)))
    del d
if contributors:
    for c in contributors:
        o.add((URIRef(namespace), URIRef(namespace+"#Contributor"), Literal(c)))
    del c


for key,value in defined_annotations.items():
    o.add((URIRef(value), RDF.type, OWL.AnnotationProperty))
    defined_annotations[key] = URIRef(value)
del key, value


####################################################
####################################################
####################################################

###############
# Loop
###############

def get_next_iri():
    global iri
    iri += 1
    return f"{iri_prefix}_{str(iri).zfill(4)}"

iri = 0

#superclass = domains[0]
#superclass = domains[1]
#superclass = domains[3]

for superclass in domains:


    #
    # start tab here
    #
    
    
    superclass = superclass.strip().lower()
    #print("\n%s" % superclass)
    
    
    superclass_iri = get_next_iri()
    superclass_defined = ufo[superclass_iri]
    o.add((superclass_defined, RDF.type, OWL.Class))
    o.add((superclass_defined, RDFS.label, Literal(superclass, lang="en")))
    
    
    
    df = pd.read_excel(xls, superclass)
    
    classes = list(set(df["class"]))
    
    for classs in classes:
        
        class_iri = get_next_iri()
        class_defined = ufo[class_iri]
        o.add((class_defined, RDF.type, OWL.Class))
        o.add((class_defined, RDFS.label, Literal(classs, lang="en")))
        o.add((class_defined, RDFS.subClassOf, superclass_defined))
        
        df_filtered = df[df["class"] == classs]
        
        if len(df_filtered) == 1: # for classes only
            
            if "subclass" in list(df_filtered): # if class exists but no subclass
                
                if pd.isna(list(df_filtered["subclass"])[0]): # for only classes
                    
                    for col in cols_for_metadata:
                        if pd.isna(list(df_filtered[col])[0]):
                            pass
                        else:
                            if ";" in list(df_filtered[col])[0]:
                                items = re.split(r'[;,/]', list(df_filtered[col])[0])
                                items = [x.strip().lower() for x in items]
                                for item in items:
                                    o.add((class_defined, defined_annotations[col], Literal(item) ))
                            else:
                                o.add((class_defined, defined_annotations[col], Literal(list(df_filtered[col])[0]) ))
                
                else:
                    subclass_iri = get_next_iri()
                    subclass_defined = ufo[subclass_iri]
                    o.add((subclass_defined, RDF.type, OWL.Class))
                    o.add((subclass_defined, RDFS.label, Literal(list(df_filtered["subclass"])[0], lang="en")))
                    o.add((subclass_defined, RDFS.subClassOf, class_defined))
                    
                    for col in cols_for_metadata:
                        if pd.isna(list(df_filtered[col])[0]):
                            pass
                        else:
                            if ";" in list(df_filtered[col])[0]:
                                items = re.split(r'[;,/]', list(df_filtered[col])[0] )
                                items = [x.strip().lower() for x in items]
                                for item in items:
                                    o.add((subclass_defined, defined_annotations[col], Literal(item) ))
                            else:
                                o.add((class_defined, defined_annotations[col], Literal(list(df_filtered[col])[0]) ))
    
    
            else: # for tabs with only class 
                
                for col in cols_for_metadata:
                    if pd.isna(list(df_filtered[col])[0]):
                        pass
                    else:
                        if ";" in list(df_filtered[col])[0]:
                            items = re.split(r'[;,/]', list(df_filtered[col])[0])
                            items = [x.strip().lower() for x in items]
                            for item in items:
                                o.add((class_defined, defined_annotations[col], Literal(item) ))
                        else:
                            o.add((class_defined, defined_annotations[col], Literal(list(df_filtered[col])[0]) ))
    
        
        else: # for multiple subclasses per class
            
            for index, row in df_filtered.iterrows():
                row = dict(row)
                
                #print(classs, class_iri)
                subclasss = row["subclass"]
                
                subclass_iri = get_next_iri()
                #print(subclasss, subclass_iri)
                subclass_defined = ufo[subclass_iri]
                o.add((subclass_defined, RDF.type, OWL.Class))
                #o.add((subclass_defined, RDFS.label, Literal(row["subclass"], lang="en")))
                o.add((subclass_defined, RDFS.label, Literal(subclasss, lang="en")))
                o.add((subclass_defined, RDFS.subClassOf, class_defined))
                
                for col in cols_for_metadata:
                    if pd.isna(row[col]):
                        pass
                    else:
                        if ";" in row[col]:
                            items = re.split(r'[;,/]',  row[col])
                            items = [x.strip().lower() for x in items]
                            for item in items:
                                o.add((subclass_defined, defined_annotations[col], Literal(item) ))
                        else:
                            o.add((subclass_defined, defined_annotations[col], Literal(row[col]) ))
    
    #
    # end tab here
    # 


del index, col, row
del superclass_iri, superclass_defined
del class_iri, class_defined
del subclass_iri, subclass_defined

###############
# Exporting
###############

#o.serialize(f"output/{the_name}.owl", format="xml")
o.serialize(f"{dir_output}{the_name}.owl", format="pretty-xml") # RDF/XML
del o

logging.info(f"A total of {iri} concepts created")
logging.info(f"Exported: {dir_output}{the_name}.owl")

del xls, start_timestamp
del git_uid_repo#, git_uid, git_repo
del ontology_description, developers, contributors, version, licensed

####################################################

# End of script
