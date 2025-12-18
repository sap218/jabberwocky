#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2024
@author: Samantha Pendleton
@GitHub: github.com/sap218/jabberwocky
"""

####################################################
#
# PARAMETERS FOR EYES
#
####################################################

is_this_a_test = True

####################################################

if is_this_a_test:
    ontology = "../bandersnatch/test/pocketmonsters"
    #ontology = "test/other_ontologies/space"
    
    ontology_name = ontology.split("/")[-1]
    
    plot_type = "tree"
    plot_type = "web"
    
    superclass_colour = "orange"
    subclass_colour = "skyblue"
    
    to_annotate_subclasses = True # False
    
    output_name = "test/%s" % ontology_name
    
else:
    ont = ""
    ontology_name = ontology.split("/")[-1]
    
    plot_type = "web"
    
    superclass_colour = "orange"
    subclass_colour = "skyblue"
    
    to_annotate_subclasses = False
    
    output_name = "%s" % ontology_name

####################################################

# End of script
