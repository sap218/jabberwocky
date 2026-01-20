#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2024
@author: Samantha Pendleton
@description: annotate ontology classes
@GitHub: github.com/sap218/jabberwocky

@useful links:
    # https://www.crummy.com/software/BeautifulSoup/bs4/doc/#insert
"""

from datetime import datetime
start_timestamp = datetime.today().strftime('%Y%m%d-%H%M%S')

import logging
import sys

from bs4 import BeautifulSoup
import pandas as pd

from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, RDFS, OWL

from params_arise import *

if is_this_a_test:
    dir_output = "test/"
    ontology_filepath = "../test/CelestialObject/space.owl"
    #update_entities = "../test/CelestialObject/corpus/new_annotations.tsv"
    update_entities = "test/new_annotations.tsv"

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
logging.info("Starting script for updating an ontology")

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

#########################

def get_next_iri():
    global iri
    iri += 1
    return f"{iri_prefix}_{str(iri).zfill(4)}"
    #global max_iri
    #max_iri += 1
    #return f"{iri_prefix}_{str(max_iri).zfill(4)}"

# Max IRI

iris = []
finding = ontology_soup.find_all('owl:Class') # finding all owl classes
for concept in finding:
    iri_prefix = concept.get("rdf:about").split("#")[1].split("_")[0]
    iris.append( int( concept.get("rdf:about").split("#")[1].split("_")[1] ) )
max_iri = max(iris)
del iris

##################################################

# Entities file

try:
    if update_entities.endswith(".csv"): 
        entities = pd.read_csv(update_entities)
    elif update_entities.endswith(".tsv"): 
        entities = pd.read_csv(update_entities, sep="\t")
    logging.info("Sucessfully imported entities file")
except:
    logging.critical(f"Cannot find entities file - check this:\t{update_entities}")
    if not update_entities.endswith(".csv") or update_entities.endswith(".tsv"):
        logging.critical("Seems like the the entity file does not end with .csv or .tsv")
    sys.exit(1)

if len(entities) == 0:
    logging.critical("Entity file has no data")
    sys.exit(1)   

#entities = entities.fillna("NANHERE")
entities.sort_values('tag')

##################################################

# Getting entities

all_annotations = []
finding = ontology_soup.find_all("AnnotationProperty")
for entity in finding:
    all_annotations.append( entity.get("rdf:about").split("#")[1] )

all_classes = []
finding = ontology_soup.find_all('owl:Class') # finding all owl classes
for entity in finding:
    all_classes.append( entity.find("rdfs:label").get_text().strip() )

del entity, finding

##################################################

# Updating

def get_class_by_label(graph, label):
    for s in graph.subjects(RDF.type, OWL.Class):
        for l in graph.objects(s, RDFS.label):
            if str(l).strip() == label:
                return s
    return None


g = Graph()
g.parse(ontology_filepath)   # works for RDF/XML, TTL, OWL, etc.


for prefix, namespaces in g.namespaces():
    if prefix == iri_prefix:
        the_namespace = Namespace(str(namespaces))
        break
del prefix, namespaces

g.bind(iri_prefix, the_namespace)



ns_map = {
    prefix: Namespace(str(ns))
    for prefix, ns in g.namespaces()
}




entities = entities[:-1]


iri = max_iri + 1


for index, row in entities.iterrows():
    the_class = row["class"].strip()
    the_annotation = row["annotation"]
    the_tag = row["tag"]  # e.g. "rdfs:comment"

    class_uri = get_class_by_label(g, the_class) # finding URI

    if class_uri is None:
        #print(f"Class not found: {the_class}")
        
        newclass_iri = get_next_iri()
        newclass_defined = the_namespace[newclass_iri]
        g.add((newclass_defined, RDF.type, OWL.Class))
        g.add((newclass_defined, RDFS.label, Literal(the_class, lang="en")))
        logging.info(f"Created new class:\t{the_class}")
        iri = iri + 1
        
        del newclass_iri, newclass_defined
        
        
    else:
        #prefix, local = the_tag.split(":")
        #prop = the_namespace[local]
        #g.add(( class_uri, prop, Literal(the_annotation) ))
        
        prefix, local = the_tag.split(":")
        if prefix not in ns_map:
            raise ValueError(f"Unknown prefix: {prefix}")
        prop = ns_map[prefix][local]

        g.add(( class_uri, prop, Literal(the_annotation) ))



del index, iri, row


###############
# Exporting
###############

output_name = ontology_filepath.split("/")[-1:][0]

g.serialize(f"{dir_output}{start_timestamp}_{output_name}", format="pretty-xml") # RDF/XML

logging.info(f"Exported:\t{dir_output}{start_timestamp}_{output_name}")
del g, output_name

# End of script
