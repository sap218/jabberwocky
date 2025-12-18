#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2024
@author: Samantha Pendleton
@description: with words of interest, grep a text file
@GitHub: github.com/sap218/jabberwocky

@useful links:
    # https://matplotlib.org/stable/users/explain/colors/colormaps.html
"""

from datetime import datetime
start_timestamp = datetime.today().strftime('%Y%m%d-%H%M%S')

import logging
import sys

import spacy
from spacy.matcher import PhraseMatcher
nlp = spacy.load("en_core_web_sm")

import time

from wordcloud import WordCloud
import matplotlib.pyplot as plt

import warnings
warnings.filterwarnings("ignore", message=r".*The rule-based lemmatizer did not find POS.*")

#########################

from params_catch import *

if is_this_a_test:
    dir_output = "test/"
    files_location = "../test/CelestialObject/corpus/"
    stopWord_filter_level = "heavy"
    file_corpus = "social_media_posts"
    plotWORDCLOUDcolormap = "plasma"
    stop_here = False
    file_words_of_interest = "../../../02_snatch_metadata/test/bandersnatch_output_requested"
    plotCYANNOTATORhighlightcolour = "#00bcd4"
    output_format = "wtags"
    output_style = "original"

#########################

# Logging

logging.basicConfig(
    filename=f"{dir_output}{start_timestamp}.log",
    encoding="utf-8",
    filemode="a",
    format="{asctime} - {levelname} - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M",
    level=logging.INFO,
    force=True
    )
logging.info("Starting script for catch")

if is_this_a_test: logging.warning("THIS IS A TEST")

#########################

from highlevel import *

# stopWords 
if stopWord_filter_level == "none": stopWords = stopWords[0]
elif stopWord_filter_level == "light": stopWords = stopWords[1]
elif stopWord_filter_level == "heavy": stopWords = stopWords[2]
else:
    logging.critical(f"Input for stopWord_filter_level:\t[{stopWord_filter_level}],\tplease choose a valid option")
    sys.exit(1)

stopWords_lemma = []
stopWordsList = []

for word in stopWords:
    stopWords_lemma.append(clean_lower_lemma(word, "stopwords", stopWordsList))

stopWords_lemma_flat = [word for phrase in stopWords_lemma for word in phrase.split()]
stopWordsList = list(set(filter(None, stopWords_lemma_flat)))

del word, stopWords, stopWords_lemma, stopWords_lemma_flat#, doc

logging.info(f"Chosen stopWord filter level\t[{stopWord_filter_level}],\tcount:\t{len(stopWordsList)}")

##################################################

# Corpus

try:
    list_of_posts = []
    with open(f"{files_location}{file_corpus}.txt", "r") as t:
        for line in t:
            list_of_posts.append(line.strip("\n").strip(" "))
    del t, line
    list_of_posts = list(filter(None, list_of_posts))
    logging.info(f"Sucessfully imported corpus:\t{file_corpus}.txt")
except:
    logging.critical(f"Cannot find corpus, recheck:\t{files_location}{file_corpus}.txt")
    sys.exit(1)


logging.info(f"Corpus line count:\t{len(list_of_posts)}")


word_count_average = [len(x.split()) for x in list_of_posts]
word_count_average = (sum(word_count_average)/len(word_count_average))

logging.info(f"Average word count in corpus:\t{round(word_count_average, 1)}")
del word_count_average

#########################

# Clean corpus

#doc_lemma_stpwrd_filter_output = []
list_of_posts_lemma_stpwrd = []
list_of_posts_lemma_stpwrd_joined = []

for post in list_of_posts:
    doc_lemma_stpwrd_filter = clean_lower_lemma(post, "corpus", stopWordsList)
    
    list_of_posts_lemma_stpwrd_joined.append(" ".join(doc_lemma_stpwrd_filter).lower())
    list_of_posts_lemma_stpwrd.append(doc_lemma_stpwrd_filter)
    
del post, doc_lemma_stpwrd_filter

#list_of_posts_lemma_stpwrd = [lst for lst in list_of_posts_lemma_stpwrd if lst]
#list_of_posts_lemma_stpwrd_joined = [lst for lst in list_of_posts_lemma_stpwrd_joined if lst]

##################################################

# WordCloud

if plotWORDCLOUD:
    logging.info(f"Plotting WordCloud")
    
    if plotWORDCLOUDcolormap not in list(plt.colormaps()):
        plotWORDCLOUDcolormap = "Set3"
        
    wc = WordCloud(
        width = 2048, height = 1080,
        
        background_color='white',
        colormap = plotWORDCLOUDcolormap,
        contour_color='black', contour_width=10,
        
        max_words=30, min_font_size=10,
        #stopwords = ['word'], # words don't want to plot
        collocations = True, # words joined together
        normalize_plurals=False,
        
        prefer_horizontal=0.8,scale=2,
        random_state=123
        ).generate(" ".join(list_of_posts_lemma_stpwrd_joined))
    
    plt.figure(figsize=(10, 5))
    plt.axis("off")
    plt.tight_layout(pad = 0)
    plt.imshow(wc, interpolation="bilinear")
    plt.savefig(f"{dir_output}{start_timestamp}_wordcloud.png")
    del wc

del plotWORDCLOUD, plotWORDCLOUDcolormap, list_of_posts_lemma_stpwrd_joined

##################################################
##################################################

if stop_here:
    logging.warning("Requested to stop here!")
    sys.exit(0)

##################################################
##################################################

# Words of interest

words_of_interest = []

try:
    words_of_interest = []
    with open(f"{files_location}{file_words_of_interest}.txt", "r") as t:
        for line in t:
            words_of_interest.append(line.strip("\n").strip(" "))
    del t, line
    words_of_interest = list(filter(None, words_of_interest))
    logging.info(f"Sucessfully imported words of interest:\t{file_words_of_interest}.txt")
except:
    logging.critical(f"Cannot find words of interest, recheck:\t{files_location}{file_words_of_interest}.txt")
    sys.exit(1)
    
if len(words_of_interest) == 0:
    #logging.warning("Words of interest is empty file, if not expected, recheck this, otherise able to proceed...")
    #words_of_interest = ["PlaceholderAsThereAreNoWordsToFilter"]
    logging.critical(f"No words of interest found, recheck:\t{files_location}{file_words_of_interest}.txt")
    sys.exit(1)
else:
    logging.info(f"Words of interest count:\t{len(words_of_interest)}")

#########################

# Clean words of interest

words_of_interest_formatted = [] 
concept_patterns = [] # for matcher

# preprocess concepts: Lemmatize & stopWords
for concept in words_of_interest: 
    doc_lemma_stpwrd_filter = clean_lower_lemma(concept, "wordsInterest", stopWordsList)

    if doc_lemma_stpwrd_filter:
        concept_patterns.append(nlp(" ".join(doc_lemma_stpwrd_filter).lower(),
                                    disable=["tagger", "parser", "ner"] ))
        
        words_of_interest_formatted.append(" ".join(doc_lemma_stpwrd_filter).lower())
del concept

matcher = PhraseMatcher(nlp.vocab) # initialize phrase matcher
matcher.add("Concepts", None, *concept_patterns) # convert concepts into patterns
del concept_patterns, doc_lemma_stpwrd_filter

####################################################

# Cyannotator

# cyan with soft glow for highlighting, can use :cyan for original
if plotCYANNOTATOR:
    if not plotCYANNOTATORhighlightcolour: plotCYANNOTATORhighlightcolour = "cyan"
    cyancolour = ["<span style='color: %s; text-shadow: 0 0 10px rgba(0, 188, 212, 0.5);'>" % plotCYANNOTATORhighlightcolour,
               "</span>"]  # plain
    cyannotator_text = []

####################################################
####################################################

# Annotating

start_annotation = time.time()

matched_output_list = []

y = 0
#for post in doc_lemma_stpwrd_filter_output:  
for post in list_of_posts_lemma_stpwrd:  
    print(f"Sentence iteration {y+1} of {len(list_of_posts_lemma_stpwrd)}")
    
    post = " ".join(post)
    
    doc = nlp(post, disable=["tagger", "parser", "ner"])
    
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
        if plotCYANNOTATOR:
            cyannotator_text.append(cyaned[-1])
            del cyaned, highlighting
            
        matched_output_list.append([
            list(matched_concepts), list_of_posts[y], 
            " ".join(list_of_posts_lemma_stpwrd[y]) if list_of_posts_lemma_stpwrd[y] else "",
            ])
        
        del matched_concepts, match_id, start, end, matched_span
        
    else: 
        matched_output_list.append([
            "NO ANNOTATION", list_of_posts[y],
            " ".join(list_of_posts_lemma_stpwrd[y]) if list_of_posts_lemma_stpwrd[y] else "",
            ])
    
    y = y + 1

del y, post, doc, matches

#########################

end_annotation = time.time() - start_annotation
end_annotation = str(round(end_annotation, 2))
logging.info(f"Time taken to annotate (seconds):\t{end_annotation}")
del start_annotation, end_annotation

####################################################
####################################################

# Formatting for output

matched_output_list_output = []

if output_format != "wtags" and output_format != "grep" and output_format != "invertedgrep":
    output_format == "wtags"
    logging.warning(f"Input for output_format:\t[{output_format}],\tplease choose a valid option otherwise default to:\twtags")
else:
    logging.info(f"Requested output_format:\t[{output_format}]")
if output_style != "original" and output_style != "formatted":
    output_style == "original"
    logging.warning(f"Input for output_style:\t[{output_style}],\tplease choose a valid option otherwise default to:\toriginal")
else:
    logging.info(f"Requested output_style:\t[{output_style}]")

for x,content in enumerate(matched_output_list):
    
    if output_format == "wtags":
        if content[0] != "NO ANNOTATION":
            if output_style == "original":
                matched_output_list_output.append( f"{sorted(content[0])} | {content[1]}")
            elif output_style == "formatted":
                matched_output_list_output.append( f"{sorted(content[0])} | {content[2]}")

    elif output_format == "grep":
        if content[0] != "NO ANNOTATION":
            if output_style == "original":
                matched_output_list_output.append(content[1])
            elif output_style == "formatted":
                matched_output_list_output.append(content[2])
    
    elif output_format == "invertedgrep":
        if content[0] == "NO ANNOTATION":
            if output_style == "original":
                matched_output_list_output.append(content[1])
            elif output_style == "formatted":
                matched_output_list_output.append(content[2])
    
del x, content

#########################

# Outputting

if not matched_output_list_output:
    matched_output_list_output.append("NO ANNOTATIONS")
    logging.warning("NO ANNOTATIONS, exiting...")
    sys.exit(0)
else:
    with open(f"{dir_output}{start_timestamp}_{output_style}_{output_format}.txt", 'w') as t:
        for word in matched_output_list_output:
            t.write(word + '\n')
    del t, word

del output_format, output_style

####################################################

# Cyannotator

if plotCYANNOTATOR:
    logging.info(f"Typing Cyannotator")
    html_content = "<html><body>"
    html_content += "<br>".join(cyannotator_text)
    html_content += "</body></html>"
    
    with open(f"{dir_output}{start_timestamp}_cyannotator.html", 'w') as f:
        f.write(html_content)
    del f, cyannotator_text, html_content

####################################################

logging.info(f"Completed - caught!")

del dir_output, file_corpus, file_words_of_interest, files_location
del plotCYANNOTATOR, plotCYANNOTATORhighlightcolour, cyancolour

# End of script
