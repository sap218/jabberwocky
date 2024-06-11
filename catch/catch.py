#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2024
@author: Samantha C Pendleton
@description: with words of interest, grep a text file
@GitHub: github.com/sap218/jabberwocky

@useful links:
    # https://matplotlib.org/stable/users/explain/colors/colormaps.html
"""

import re
import time
import json

import spacy
from spacy.matcher import PhraseMatcher
nlp = spacy.load("en_core_web_sm")

from wordcloud import WordCloud
import matplotlib.pyplot as plt

from params_catch import *

####################################################

if not_annotated: output_name = output_name + "_invert"
else:
    if grep_format: output_name = output_name + "_grep"
    else: output_name = output_name + "_tags"

if graph == "Yes": graph = True
elif graph == "No": graph = False

if grep_format == "grep": grep_format = True
elif grep_format == "tags": grep_format = False

if not_annotated == "No": not_annotated = False
elif not_annotated == "Yes": not_annotated = True

####################################################

from highlevel import *

''' stopWords '''
stopWords = [cleantext(x.lower()) for x in stopWords]

def remove_stop_words(text, stopWords):
    return ' '.join(word for word in text.split() if word.lower() not in stopWords)

####################################################
####################################################

words_of_interest = []

with open("%s.txt" % annotation_file, "r") as t:
    for word in t:
        words_of_interest.append(word.strip("\n").strip(" "))
del t, word

words_of_interest_clean = [cleantext(x.lower()) for x in words_of_interest]
#words_of_interest_clean_stpwrd = [remove_stop_words(text, stopWords) for text in words_of_interest_clean]

#del words_of_interest_clean

####################################################

list_of_posts = []

with open("%s.txt" % corpus, "r") as t:
    for post in t:
        list_of_posts.append(post.strip("\n").strip(" "))
del t, post
list_of_posts = list(filter(None, list_of_posts))

post_stats = []
for post in list_of_posts:
    post = post.split()
    post_stats.append(len(post))
del post

list_of_posts_clean = [cleantext(x.lower()) for x in list_of_posts]
#list_of_posts_clean_stpwrd = [remove_stop_words(text, stopWords) for text in list_of_posts_clean]

#del list_of_posts_clean

####################################################

statistics = [
    "concepts count: %s" % len(words_of_interest_clean),
    "post count: %s" % len(list_of_posts_clean),
    "average word count: %s" % (sum(post_stats)/len(post_stats)),
    ]
del post_stats

####################################################
####################################################

words_of_interest_clean_lemma_stpwrd = [] 

# preprocess concepts: Lemmatize & stopWords
concept_patterns = [] # for matcher
for concept in words_of_interest_clean:
        
    doc = nlp(concept)
    
    ''' lemma '''
    lemma_item = [token.lemma_ for token in doc]
    
    ''' stopWords '''
    lemma_item = [remove_stop_words(text, stopWords) for text in lemma_item]
    lemma_item = list(filter(None, lemma_item))
    
    concept_patterns.append(nlp(" ".join(lemma_item)))
    
    word_item = " ".join([token.lemma_ for token in doc])
    words_of_interest_clean_lemma_stpwrd.append(word_item)
    
del concept, doc, lemma_item, word_item
del words_of_interest, words_of_interest_clean

matcher = PhraseMatcher(nlp.vocab) # initialize phrase matcher
matcher.add("Concepts", None, *concept_patterns) # convert concepts into patterns

del concept_patterns

####################################################
####################################################

start_time = time.time()


matched_output_list = []
#matched_output_dictionary = {}

list_of_posts_clean_lemma_stpwrd = []

x = 0
#for response in list_of_posts_clean_stpwrd_lemma:
for post in list_of_posts_clean:
    print("Sentence iteration ", x, " out of ", len(list_of_posts_clean))
    
    doc = nlp(post)
    
    ''' lemma '''
    doc = [token.lemma_ for token in doc]
    
    ''' stopWords '''
    doc = [remove_stop_words(text, stopWords) for text in doc]
    doc = list(filter(None, doc))
    
    doc = nlp(" ".join(doc))
    
    
    post_item = " ".join([token.lemma_ for token in doc])
    list_of_posts_clean_lemma_stpwrd.append(post_item)
    

    matches = matcher(doc)
    
    if matches:
    
        matched_concepts = set()
        for match_id, start, end in matches:
            matched_span = doc[start:end]
            matched_concepts.add(matched_span.text)
            
        matched_output_list.append([ list(matched_concepts), list_of_posts[x] ])
        #matched_output_dictionary[list_of_posts[x]] = list(matched_concepts)
        
    else: 
        matched_output_list.append([ "NO ANNOTATION", list_of_posts[x] ])
        #matched_output_dictionary[list_of_posts[x]] = "NO ANNOTATION"

    x = x + 1


end_time = time.time() - start_time
print( "Seconds taken to annotate: %s" % str(round(end_time, 2)) )
del start_time, end_time

del doc, post, x, post_item
del matched_concepts, matches, matched_span, match_id, start, end

####################################################
####################################################

to_output = []

for x in matched_output_list:
    if not_annotated:
        if x[0] == "NO ANNOTATION": to_output.append(x[1])
    else:
        if grep_format:
            if x[0] != "NO ANNOTATION": to_output.append(x[1])
            
        else:
            if x[0] != "NO ANNOTATION": to_output.append( "%s # %s" % ( x[0] ,x[1]) )


with open('%s.txt' % output_name, 'w') as t:
    for word in to_output:
        t.write(word + '\n')

#with open('test/catch_output.json', 'w') as j:
#    json.dump(matched_output_dictionary, j, indent=4)
#del j

with open('%s.txt' % stats_output_name, 'w') as t:
    for word in statistics:
        t.write(word + '\n')

del t, word

####################################################
####################################################

if graph:
    wc = WordCloud(
        width = 2048, height = 1080,
        
        background_color='white',
        colormap = cm,
        contour_color='black', contour_width=10,
        
        max_words=30, min_font_size=10,
        #stopwords = ['word'], # words don't want to plot
        collocations = True, # words joined together
        normalize_plurals=False,
        
        prefer_horizontal=0.8,scale=2,
        random_state=123
        ).generate(" ".join(list_of_posts_clean_lemma_stpwrd))
    
    plt.figure(figsize=(10, 5))
    plt.axis("off")
    plt.tight_layout(pad = 0)
    plt.imshow(wc, interpolation="bilinear")
    plt.savefig('%s.png' % plot_output_name)

####################################################

# End of script
