#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2025
@author: Samantha C Pendleton
@description: flask app
@GitHub: github.com/sap218/jabberwocky

@useful links:
    # https://python-adv-web-apps.readthedocs.io/en/latest/flask.html
"""

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../catch')))
from params_catch import *
#from ..catch.params_catch import *

file_corpus = "../../catch/test/social_media_posts.txt"
file_words_of_interest = "../../bandersnatch/test/snatch_output.txt"

is_this_a_test = False
plotWORDCLOUD = True
plotCYANNOTATOR = True

'''
filter_level = "light" # or "none" or "heavy"
output_format = "wtags" # ["wtags","grep","invertedgrep"]

output_name = "test"

colormapWC = "Set3" # default
highlightcolour = "#00bcd4" # default = cyan
'''

from flask import Flask, render_template, request, send_file
import os

app = Flask(__name__)

####################################################

@app.route('/', methods=['GET', 'POST'])
def index():
    
    corpus = ''
    concepts = ''

    if request.method == 'POST':
        
        # CORPUS
        uploaded_corpus_file = request.files.get('corpus_file')
        if uploaded_corpus_file and uploaded_corpus_file.filename.endswith('.txt'):
            corpus = uploaded_corpus_file.read().decode('utf-8')
        elif not uploaded_corpus_file:  # use TEST
            if os.path.exists(file_corpus):
                with open(file_corpus, 'r') as file:
                    corpus = file.read()

        # CONCEPTS
        uploaded_concepts_file = request.files.get('concepts_file')
        if uploaded_concepts_file and uploaded_concepts_file.filename.endswith('.txt'):
            concepts = uploaded_concepts_file.read().decode('utf-8').replace('\n', ', ')
        elif not uploaded_concepts_file: # use TEST
            if os.path.exists(file_words_of_interest):
                with open(file_words_of_interest, 'r') as file:
                    concepts = file.read()#.replace('\n', ', ')

    else: # this is the TEST data
        if os.path.exists(file_corpus):
            with open(file_corpus, 'r') as file:
                corpus = file.read()
        
        if os.path.exists(file_words_of_interest):
            with open(file_words_of_interest, 'r') as file:
                concepts = file.read().replace('\n', ', ')

    return render_template('index.html', corpusFunction=corpus, conceptsFunction=concepts)

####################################################

##

####################################################
'''
@app.route('/about')
def about():
    return render_template('about.html')
'''
####################################################

if __name__ == '__main__':
    app.run(debug=False) # False for Spyder

####################################################

# End of script
