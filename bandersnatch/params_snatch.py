#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2024
@author: Samantha C Pendleton
@GitHub: github.com/sap218/jabberwocky
"""

####################################################
#
# PARAMETERS FOR SNATCH
#
####################################################

is_this_a_test = True

####################################################

if is_this_a_test:
    ontology_name = "test/pocketmonsters"
    ontology_tags = "test/ontology_tags"
    classes_of_interest = "test/words_of_interest" # if empty, extract all annotations of all classes
    output_name = "test/snatch_output"
    
else:
    ontology_name = ""
    ontology_tags = ""
    classes_of_interest = ""
    
    output_name = "snatch_output"

####################################################

# End of script
