#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2024
@author: Samantha Pendleton
@description: versions
@GitHub: github.com/sap218/jabberwocky
"""

# Modules used in Jabberwocky

import sys # this includes: import time
print(f"Python \t v{sys.version.split(" ")[0]}")

import rdflib
print(f"rdflib \t v{rdflib.__version__}")

import bs4 # BeautifulSoup4
print(f"bs4 \t v{bs4.__version__}")

import contractions
import pkg_resources
version = pkg_resources.get_distribution("contractions").version
print(f"contractions \t v{version}")
del version

import pandas as pd
print(f"pandas v{pd.__version__}")

import matplotlib
print(f"matplotlib \t v{matplotlib.__version__}")

import sklearn # scikit-learn
print(f"sklearn \t v{sklearn.__version__}") 

import spacy
print(f"spaCy \t v{spacy.__version__}")

import wordcloud 
print(f"wordcloud \t v{wordcloud.__version__}")

import nltk
print(f"nltk \t v{nltk.__version__}")

import networkx
print(f"networkx \t v{networkx.__version__}")

additional_info = "".join(sys.version.split("|")[1:])
print(f"additional information: \t {additional_info}")
del additional_info

# When running Jabberwocky, users need these versions minimum

'''
Python 	 v3.12.3
rdflib 	 v7.1.3
bs4 	 v4.12.3
contractions 	 v0.1.73
pandas v2.2.2
matplotlib 	 v3.9.2
sklearn 	 v1.5.1
spaCy 	 v3.7.2
wordcloud 	 v1.9.4
nltk 	 v3.9.1
networkx 	 v3.3
additional information: 	  packaged by conda-forge  (main, Apr 15 2024, 18:20:11) [MSC v.1938 64 bit (AMD64)]
'''

####################################################

# End of script
