#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2024
@author: Samantha Pendleton
@GitHub: github.com/sap218/jabberwocky
"""

####################################################
#
# PARAMETERS FOR GIMBLE
#
# Any completed fields below are an example for running the test data
#
####################################################

is_this_a_test = True

####################################################

dir_output = "output/"

excel_file_location = "input/" # example

the_name = "" # the name of the excel file/your ontology

git_uid = "" # username where repository is stored
git_repo = "" # repo where ontology is stored

# no need to edit this
namespace = f"https://github.com/{git_uid}/{git_repo}/blob/master/{the_name}.owl"

iri_prefix = "" # IRI of ontology, e.g. for space we used UFO
ontology_description = ""
developers = []
contributors = []
version = "" # e.g. v1.0
licensed = "https://creativecommons.org/licenses/by-nc/4.0/" # a common license

defined_annotations = {
    "synonym": f"{namespace}#hasSynonym",
    "definition": "http://www.w3.org/2000/01/rdf-schema#comment"
    }

####################################################

# End of script
