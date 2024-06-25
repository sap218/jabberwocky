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

####################################################

from highlevel import *

''' stopWords '''
if filter_level == "light": stopWords = stopWords[0]
elif filter_level == "heavy": stopWords = stopWords[1]

stopWords_lemma = []
for word in stopWords:
    word = cleantext(word.lower())
    doc = nlp(word)
    doc_lemma = " ".join([token.lemma_ for token in doc])
    stopWords_lemma.append(doc_lemma)
stopWords_lemma_filt = list(filter(None, stopWords_lemma))
stopWords_lemma_filt_flat = [word for phrase in stopWords_lemma_filt for word in phrase.split()]

stopWords = list(set(stopWords_lemma_filt_flat))
del word, doc, doc_lemma, stopWords_lemma, stopWords_lemma_filt, stopWords_lemma_filt_flat

####################################################
####################################################

try:
    list_of_posts = []
    with open("%s.txt" % corpus, "r") as t:
        for post in t:
            list_of_posts.append(post.strip("\n").strip(" "))
    del t, post
except FileNotFoundError:
    sys.exit("Cannot find text file")

list_of_posts = list(filter(None, list_of_posts))

post_stats = []
for post in list_of_posts:
    post = post.split()
    post_stats.append(len(post))
del post

####################################################
####################################################

if len(annotation_file) > 0:
    try:
        words_of_interest = []
        with open("%s.txt" % annotation_file, "r") as t:
            for word in t:
                words_of_interest.append(word.strip("\n").strip(" "))
        del t, word
    except FileNotFoundError:
        sys.exit("User attempted to provide a list of terms for annotation - unsuccessful")
else: words_of_interest = ["nowordstofilter"]

words_of_interest = list(filter(None, words_of_interest))

####################################################

words_of_interest_clean_lemma_stpwrd = [] 
concept_patterns = [] # for matcher

# preprocess concepts: Lemmatize & stopWords
for concept in words_of_interest: 
    concept = cleantext(concept.lower())
    
    doc = nlp(concept)
    
    ## lemma
    doc_lemma = [token.lemma_ for token in doc]
    ## stopwords
    doc_lemma_stpwrd = [remove_stop_words(text, stopWords) for text in doc_lemma]
    doc_lemma_stpwrd = list(filter(None, doc_lemma_stpwrd))
    
    if doc_lemma_stpwrd:
        concept_patterns.append(nlp(" ".join(doc_lemma_stpwrd).lower()))
        words_of_interest_clean_lemma_stpwrd.append(" ".join(doc_lemma_stpwrd).lower())
    
del concept, doc, doc_lemma, doc_lemma_stpwrd

matcher = PhraseMatcher(nlp.vocab) # initialize phrase matcher
matcher.add("Concepts", None, *concept_patterns) # convert concepts into patterns
del concept_patterns

####################################################
####################################################

statistics = [
    "concepts count: %s" % len(words_of_interest),
    "post count: %s" % len(list_of_posts),
    "average word count: %s" % (sum(post_stats)/len(post_stats)),
    ]
del post_stats

####################################################
####################################################

start_time = time.time()

matched_output_list = []
list_of_posts_clean_lemma_stpwrd = []

x = 0
y = 0
for post in list_of_posts:
    x = x + 1
    print("Sentence iteration ", x, " out of ", len(list_of_posts))
    post = cleantext(post.lower())
    
    doc = nlp(post)
    
    ## lemma
    doc_lemma = [token.lemma_ for token in doc]
    ## stopwords
    doc_lemma_stpwrd = [remove_stop_words(text, stopWords) for text in doc_lemma]
    doc_lemma_stpwrd = list(filter(None, doc_lemma_stpwrd))
        
    list_of_posts_clean_lemma_stpwrd.append(" ".join(doc_lemma_stpwrd).lower())
    
    doc = nlp(" ".join(doc_lemma_stpwrd).lower())
    matches = matcher(doc)
    
    if matches:
        matched_concepts = set()
        for match_id, start, end in matches:
            matched_span = doc[start:end]
            matched_concepts.add(matched_span.text)
            
        matched_output_list.append([ list(matched_concepts), list_of_posts[y] ])
        
        del matched_concepts, match_id, start, end, matched_span
        
    else: 
        matched_output_list.append([ "NO ANNOTATION", list_of_posts[y] ])
    
    y = y + 1

end_time = time.time() - start_time
end_time = str(round(end_time, 2))
print("Seconds taken to annotate: %s" % end_time)
del start_time

statistics.append("time taken to annotate (seconds): %s" % end_time)

del x, y, post, doc, doc_lemma, doc_lemma_stpwrd, matches

####################################################
####################################################

matched_output_list_output = []

for x,content in enumerate(matched_output_list):
    if not_annotated:
        if content[0] == "NO ANNOTATION": matched_output_list_output.append(content[1])
    else:
        if grep_format:
            if content[0] != "NO ANNOTATION": matched_output_list_output.append(content[1])
            
        else:
            if content[0] != "NO ANNOTATION": matched_output_list_output.append( "%s # %s" % (content[0],content[1]) )
del x, content

if not matched_output_list_output: matched_output_list_output.append("NO ANNOTATIONS") 

####################################################

with open('%s.txt' % output_name, 'w') as t:
    for word in matched_output_list_output:
        t.write(word + '\n')
del t,word

#with open('test/catch_output.json', 'w') as j:
#    json.dump(matched_output_dict_output, j, indent=4)
#del j

####################################################

with open('%s.txt' % stats_output_name, 'w') as t:
    for word in statistics:
        t.write(word + '\n')
del t,word

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
