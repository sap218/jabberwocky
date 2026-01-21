#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2024
@author: Samantha Pendleton
@description: plot an ontology
@GitHub: github.com/sap218/jabberwocky

@useful links:
    # https://stackoverflow.com/a/21990980
"""

from datetime import datetime
start_timestamp = datetime.today().strftime('%Y%m%d-%H%M%S')

import logging
import sys

from bs4 import BeautifulSoup
import networkx as nx
import matplotlib.pyplot as plt
from textwrap import wrap

from params_eyes import *

if is_this_a_test:
    dir_output = "test/"
    ontology_filepath = "../05_update_entities/test/20260121-215122_space.owl"

    #plot_type = "tree"
    plot_type = "web"
    
    superclass_colour = "orange"
    subclass_colour = "skyblue"
    
    to_annotate_subclasses = True
    
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
logging.info("Starting script for plotting ontology")

if is_this_a_test: logging.warning("THIS IS A TEST")

##################################################

# Ontology file

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

####################################################

# Graph

G = nx.DiGraph()

#########################

# Adding concepts to graph

finding = ontology_soup.find_all('owl:Class') # finding all owl classes
concepts = []

for concept in finding:
    label = concept.find("rdfs:label").get_text() 
    concepts.append(label)
    iri = concept.get('rdf:about')
    
    G.add_node(label, id=iri) # node for each class

    # find superclass and add edges
    subclasses = concept.find_all("rdfs:subClassOf")
    for subclass in subclasses:
        superclass = subclass.get('rdf:resource')
        # now get label of superclass...
        subclass_label = ontology_soup.find(attrs={"rdf:about": superclass}).find("rdfs:label").get_text()
        G.add_edge(subclass_label, label) # add edge for relationship

del finding, iri, label, subclass_label, subclass, superclass, subclasses

####################################################

# G.remove_node("Space Ontology (UFO)")

high_level_classes = [node for node, degree in G.in_degree() if degree == 0]
color_map = [superclass_colour if node in high_level_classes else subclass_colour for node in G.nodes()]

#########################

plt.figure(figsize=(18, 10))

if plot_type == "tree":
    pos = nx.nx_agraph.graphviz_layout(G, prog='dot')       
elif plot_type == "web": 
    pos = nx.nx_agraph.graphviz_layout(G, prog='sfdp')

#########################

node_degrees = dict(G.degree())
node_sizes = [30 * node_degrees[node] for node in G.nodes()]

#if plot_type == "web":
min_lim = int( sorted(node_sizes,reverse=True)[:11][-1] )
node_sizes = [150 if n <= min_lim else n for n in node_sizes]

#########################

nx.draw_networkx_nodes(G, pos, 
                       node_size=node_sizes,
                       node_color=color_map,
                       alpha=0.8)

nx.draw_networkx_edges(G, pos, edge_color="gray", alpha=0.5, width=1.0, arrows=True)

#########################

if to_annotate_subclasses:
    highlevelfontsize = 8
    lowlevelfontsize = 6
else: highlevelfontsize = 14

#########################

labels = {node: '\n'.join(wrap(node, width=11)) if node in high_level_classes else node for node in G.nodes() if node in high_level_classes}
nx.draw_networkx_labels(G, pos, font_size=highlevelfontsize, font_weight="bold",labels=labels)

labels = {node: '\n'.join(wrap(node, width=15)) if node not in high_level_classes else node for node in G.nodes() if node not in high_level_classes}
if to_annotate_subclasses: nx.draw_networkx_labels(G, pos, font_size=lowlevelfontsize, labels=labels)

####################################################

# Exporting

#plt.title("Ontology")
plt.axis('off')
plt.savefig(f"{dir_output}{start_timestamp}_{plot_type}-plot.png", format="PNG", dpi=300, bbox_inches='tight')
plt.show()

####################################################

# End of script
