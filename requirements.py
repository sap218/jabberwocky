#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2024
@author: Samantha C Pendleton
@description: versions
@GitHub: github.com/sap218/jabberwocky
"""

# Modules used in Jabberwocky

import sys # this includes: import time
print("Python \t v%s" % sys.version.split(" ")[0])

import bs4
print("BeautifulSoup4 \t v%s" % bs4.__version__)

'''
# Base modules

import re
print("re \t v%s" % re.__version__)

import json
print("json \t v%s" % json.__version__)
'''

import contractions
import pkg_resources
version = pkg_resources.get_distribution("contractions").version
print("contractions \t v%s" % version)
del version

import pandas as pd
print("pandas \t v%s" % pd.__version__)

import matplotlib
print("matplotlib \t v%s" % matplotlib.__version__)

import sklearn
print("scikit-learn \t v%s" % sklearn.__version__) 

import spacy
print("spaCy \t v%s" % spacy.__version__)

import wordcloud 
print("wordcloud \t v%s" % wordcloud.__version__)

import nltk
print("nltk \t v%s" % nltk.__version__)

import networkx
print("networkx \t v%s" % networkx.__version__)

print("additional information: \t %s" % "".join(sys.version.split("|")[1:]))

# When running Jabberwocky, users need these versions minimum

'''
Python 	 v3.12.3
BeautifulSoup4 	 v4.12.3
contractions 	 v0.1.73
pandas 	 v2.2.2
matplotlib 	 v3.9.2
scikit-learn 	 v1.5.1
spaCy 	 v3.7.2
wordcloud 	 v1.9.4
nltk 	 v3.9.1
networkx 	 v3.3
additional information: 	  packaged by conda-forge  (main, Apr 15 2024, 18:20:11) [MSC v.1938 64 bit (AMD64)]
'''

####################################################

# End of script
