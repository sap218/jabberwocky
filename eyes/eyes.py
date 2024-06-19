#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2024
@author: Samantha C Pendleton
@description: plot an ontology
@GitHub: github.com/sap218/jabberwocky

@useful links:
    # https://stackoverflow.com/a/21990980
"""

from bs4 import BeautifulSoup
import networkx as nx
import matplotlib.pyplot as plt
from textwrap import wrap

from params_eyes import *

####################################################

with open("%s.owl" % ontology, "rt") as o:
    ontology_file = o.read()  
ontology_soup = BeautifulSoup(ontology_file,'xml') # BEAUTIFUL SOUP really is beautiful
del o, ontology

####################################################

G = nx.DiGraph() # graph

####################################################

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

####################################################

plt.figure(figsize=(18, 10))

if plot_type == "tree":
    pos = nx.nx_agraph.graphviz_layout(G, prog='dot')       
elif plot_type == "web": 
    pos = nx.nx_agraph.graphviz_layout(G, prog='sfdp')

####################################################

node_degrees = dict(G.degree())
node_sizes = [15 * node_degrees[node] for node in G.nodes()]

if plot_type == "web":
    min_lim = int( sorted(node_sizes,reverse=True)[:11][-1] )
    node_sizes = [15 if n <= min_lim else n for n in node_sizes]

####################################################

nx.draw_networkx_nodes(G, pos, 
                       node_size=node_sizes,
                       node_color=color_map,
                       alpha=0.8)

nx.draw_networkx_edges(G, pos, edge_color="gray", alpha=0.5, width=1.0, arrows=True)

####################################################

if to_annotate_subclasses:
    highlevelfontsize = 8
    lowlevelfontsize = 6
else: highlevelfontsize = 14

####################################################

labels = {node: '\n'.join(wrap(node, width=11)) if node in high_level_classes else node for node in G.nodes() if node in high_level_classes}
nx.draw_networkx_labels(G, pos, font_size=highlevelfontsize, font_weight="bold",labels=labels)

labels = {node: '\n'.join(wrap(node, width=15)) if node not in high_level_classes else node for node in G.nodes() if node not in high_level_classes}
if to_annotate_subclasses: nx.draw_networkx_labels(G, pos, font_size=lowlevelfontsize, labels=labels)

####################################################

#plt.title("Ontology")
plt.axis('off')
plt.savefig("%s_%s.png" % (output_name, plot_type), format="PNG", dpi=300, bbox_inches='tight')
plt.show()

####################################################

# End of script
