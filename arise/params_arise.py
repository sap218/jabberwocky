#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2024
@author: Samantha C Pendleton
@GitHub: github.com/sap218/jabberwocky
"""

####################################################
#
# PARAMETERS FOR ARISE
#
####################################################

is_this_a_test = True

####################################################

if is_this_a_test:
    ontology_name = "../bandersnatch/test/pocketmonsters"
    annotation_file = "../arise/test/new_annotations"
    output_name = "../arise/test/%s" % ontology_name.split("/")[-1]
    
else:
    ontology_name = ""
    annotation_file = ""
    
    output_name = "%s" % ontology_name.split("/")[-1]

####################################################

# End of script
