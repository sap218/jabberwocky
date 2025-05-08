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

import time
start_script = time.time()

from datetime import datetime
now = datetime.now()
output_timestamp = now.strftime("%Y%m%d-%H%M")
del now

import sys

import spacy
from spacy.matcher import PhraseMatcher
nlp = spacy.load("en_core_web_sm")

from wordcloud import WordCloud
import matplotlib.pyplot as plt

from params_catch import *

####################################################

if is_this_a_test:
    file_corpus = "../catch/test/social_media_posts.txt"
    file_words_of_interest = "../bandersnatch/test/snatch_output.txt"
    
    dirloc = "test/"
    output_name_catch = "%sannotation_%s.txt" % (dirloc, output_format)
    output_name_log = "%slog.txt" % (dirloc)
    if plotWORDCLOUD: output_name_wordcloud = "%swordcloud.png" % (dirloc)
    if plotCYANNOTATOR: output_name_cyannotator = "%scyannotator.html" % (dirloc)

else:
    dirloc = "output/"
    output_name_catch = "%sannotation_%s_%s_%s.txt" % (dirloc, output_format, output_name, output_timestamp)
    output_name_log = "%slog_%s_%s.txt" % (dirloc, output_name, output_timestamp)
    if plotWORDCLOUD: output_name_wordcloud = "%swordcloud_%s_%s.png" % (dirloc, output_name, output_timestamp)
    if plotCYANNOTATOR: output_name_cyannotator = "%scyannotator_%s_%s.html" % (dirloc, output_name, output_timestamp)
    
del dirloc, output_name

####################################################

from highlevel import *

''' stopWords '''
if filter_level == "none": stopWords = stopWords[0]
elif filter_level == "light": stopWords = stopWords[1]
elif filter_level == "heavy": stopWords = stopWords[2]

stopWords_lemma = []
stopWordsList = []
for word in stopWords:
    stopWords_lemma.append(clean_lower_lemma(word, "stopwords", stopWordsList))

stopWords_lemma_flat = [word for phrase in stopWords_lemma for word in phrase.split()]
stopWordsList = list(set(filter(None, stopWords_lemma_flat)))

del word, stopWords, stopWords_lemma, stopWords_lemma_flat#, doc

####################################################
####################################################

try:
    list_of_posts = []
    with open("%s" % file_corpus, "r") as t:
        for line in t:
            list_of_posts.append(line.strip("\n").strip(" "))
    del file_corpus, t, line
except FileNotFoundError:
    sys.exit("Cannot find [corpus] text file")

list_of_posts = list(filter(None, list_of_posts)) # remove empty lines

post_stats = [len(x.split()) for x in list_of_posts] # word count per line

####################################################
####################################################

if len(file_words_of_interest) > 0:
    try:
        words_of_interest = []
        with open("%s" % file_words_of_interest, "r") as t:
            for line in t:
                words_of_interest.append(line.strip("\n").strip(" "))
        del t, line
    except FileNotFoundError:
        #sys.exit("User attempted to provide a list of terms for annotation - unsuccessful")
        sys.exit("Cannot find [words of interest] file")
else: words_of_interest = [] #["nowordstofilter"]

words_of_interest = list(filter(None, words_of_interest)) # remove empty lines

####################################################

statistics = [
    "is this a test: %s" % str(is_this_a_test),
    "stopword filter level: %s" % filter_level,
    "concepts count: %s" % len(words_of_interest),
    "post count: %s" % len(list_of_posts),
    "average word count: %s" % (sum(post_stats)/len(post_stats)),
    ]
del post_stats, filter_level

if not words_of_interest: words_of_interest = ["PlaceholderAsThereAreNoWordsToFilter"]

####################################################
####################################################

words_of_interest_formatted = [] 
concept_patterns = [] # for matcher

# preprocess concepts: Lemmatize & stopWords
for concept in words_of_interest: 
    doc_lemma_stpwrd_filter = clean_lower_lemma(concept, "text", stopWordsList)

    if doc_lemma_stpwrd_filter:
        concept_patterns.append(nlp(" ".join(doc_lemma_stpwrd_filter).lower()))
        words_of_interest_formatted.append(" ".join(doc_lemma_stpwrd_filter).lower())
del concept

matcher = PhraseMatcher(nlp.vocab) # initialize phrase matcher
matcher.add("Concepts", None, *concept_patterns) # convert concepts into patterns
del concept_patterns

####################################################
####################################################

doc_lemma_stpwrd_filter_output = []
list_of_posts_formatted = []

for post in list_of_posts:
    doc_lemma_stpwrd_filter = clean_lower_lemma(post, "text", stopWordsList)
    
    list_of_posts_formatted.append(" ".join(doc_lemma_stpwrd_filter).lower())
    
    doc_lemma_stpwrd_filter_output.append(doc_lemma_stpwrd_filter)
    
del post, doc_lemma_stpwrd_filter
    
####################################################

if plotWORDCLOUD:
    if not colormapWC: colormapWC = "Set3"
    
    wc = WordCloud(
        width = 2048, height = 1080,
        
        background_color='white',
        colormap = colormapWC,
        contour_color='black', contour_width=10,
        
        max_words=30, min_font_size=10,
        #stopwords = ['word'], # words don't want to plot
        collocations = True, # words joined together
        normalize_plurals=False,
        
        prefer_horizontal=0.8,scale=2,
        random_state=123
        ).generate(" ".join(list_of_posts_formatted))
    
    plt.figure(figsize=(10, 5))
    plt.axis("off")
    plt.tight_layout(pad = 0)
    plt.imshow(wc, interpolation="bilinear")
    plt.savefig('%s' % output_name_wordcloud)

    del plotWORDCLOUD, colormapWC, wc, output_name_wordcloud

####################################################
    
# cyan with soft glow for highlighting, can use :cyan for original
if plotCYANNOTATOR:
    if not highlightcolour: highlightcolour = "#00bcd4"
    cyancolour = ["<span style='color: %s; text-shadow: 0 0 10px rgba(0, 188, 212, 0.5);'>" % highlightcolour,
               "</span>"]  # plain
    cyannotator_text = []

####################################################

start_annotation = time.time()

matched_output_list = []

y = 0
for post in doc_lemma_stpwrd_filter_output:  
    print("Sentence iteration ", y+1, " out of ", len(list_of_posts))
    
    post = " ".join(post)
    
    doc = nlp(post)
    matches = matcher(doc)
    
    if matches:
        matched_concepts = set()
        #if cyannotator: highlighting = " ".join(doc_lemma_stpwrd_filter).lower()

        cyaned = []
        for match_id, start, end in matches:
            matched_span = doc[start:end]
            matched_concepts.add(matched_span.text)
            
            if plotCYANNOTATOR:
                highlighting = re.sub(r'\b%s\b' % re.escape(matched_span.text),
                                          (cyancolour[0] + matched_span.text + cyancolour[1]), post)
                cyaned.append(highlighting)
        if plotCYANNOTATOR: cyannotator_text.append(cyaned[-1])
            
        matched_output_list.append([ list(matched_concepts), list_of_posts[y] ])
        
        del matched_concepts, match_id, start, end, matched_span, cyaned
        
    else: 
        matched_output_list.append([ "NO ANNOTATION", list_of_posts[y] ])
    
    y = y + 1

del y, post, doc, matches

####################################################

end_annotation = time.time() - start_annotation
end_annotation = str(round(end_annotation, 2))
statistics.append("time taken to annotate (seconds): %s" % end_annotation)
del start_annotation, end_annotation

####################################################
####################################################

matched_output_list_output = []

for x,content in enumerate(matched_output_list):
    
    if output_format == "wtags":
        if content[0] != "NO ANNOTATION": matched_output_list_output.append( "%s # %s" % (sorted(content[0]),content[1]) )
    elif output_format == "grep":
        if content[0] != "NO ANNOTATION": matched_output_list_output.append(content[1])
    elif output_format == "invertedgrep":
        if content[0] == "NO ANNOTATION": matched_output_list_output.append(content[1])

del x, content, output_format

if not matched_output_list_output:
    matched_output_list_output.append("NO ANNOTATIONS") 
    if not file_words_of_interest:
        statistics.append("NO ANNOTATIONS - this is due to an empty [words of interest] file")
    else: statistics.append("NO ANNOTATIONS")

####################################################

with open('%s' % output_name_catch, 'w') as t:
    for word in matched_output_list_output:
        t.write(word + '\n')
del t, word, output_name_catch

####################################################

if plotCYANNOTATOR:
    if not cyannotator_text:
        cyannotator_text = ["NO ANNOTATIONS"]
    
    html_content = "<html><body>"
    html_content += "<br>".join(cyannotator_text)
    html_content += "</body></html>"
    
    with open('%s' % output_name_cyannotator, 'w') as f:
        f.write(html_content)
    del f, output_name_cyannotator

####################################################

end_script = time.time() - start_script
end_script = str(round(end_script, 2))
statistics.append("time taken to run script (seconds): %s" % end_script)
del start_script, end_script

with open(output_name_log, 'w') as t:
    for word in statistics:
        t.write(word + '\n')
del t, word, output_name_log

####################################################

# End of script
