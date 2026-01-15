#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2024
@author: Samantha Pendleton
@description: conducts TF-IDF
@GitHub: github.com/sap218/jabberwocky

@useful links:
    # https://python-charts.com/matplotlib/styles/
"""

from datetime import datetime
start_timestamp = datetime.today().strftime('%Y%m%d-%H%M%S')

import logging
import sys
import time

from nltk import ngrams
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MinMaxScaler

import pandas as pd
import matplotlib.pyplot as plt

#########################

from params_bite import *

if is_this_a_test:
    dir_output = "test/"
    stopWord_filter_level = "heavy"
    file_concepts_to_remove = "../02_snatch_metadata/test/20260114-230425_allClasses.txt"
    file_corpus = "../03_catch_text/test/20260114-231442_original_invertedgrep.txt"    
    ngram_count = [1,3]
    plotTFIDF = True
    plotTFIDFlimit = 30
    plotTFIDFcolormap = "mediumseagreen"

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
logging.info("Starting script for ranking terms (TF-IDF)")

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

####################################################
####################################################

# Concepts to remove

if file_concepts_to_remove:
    try:
        concepts_to_remove = []
        with open(file_concepts_to_remove, "r") as t:
            for line in t:
                concepts_to_remove.append(line.strip("\n").strip(" "))
        del t, line
        concepts_to_remove = list(filter(None, concepts_to_remove))
        logging.info("Sucessfully imported concepts to remove")
    except:
        logging.critical(f"Cannot find file of concepts to remove, recheck:\t{file_concepts_to_remove}")
        if not file_concepts_to_remove.endswith(".txt"):
            logging.critical("Seems like the the file of concepts to remove does not end with .txt")
        sys.exit(1)
else: concepts_to_remove = []

logging.info(f"Concepts to remove count:\t{len(file_concepts_to_remove)}")
if len(concepts_to_remove) == 0:
    logging.warning(f"If the above is not expected, recheck:\t{file_concepts_to_remove}")

#########################

concepts_to_remove_formatted = [] 

# preprocess concepts: Lemmatize & stopWords
for concept in concepts_to_remove: 
    doc_lemma_stpwrd_filter = clean_lower_lemma(concept, "wordsInterest", stopWordsList)
    if doc_lemma_stpwrd_filter:
        concepts_to_remove_formatted.append(" ".join(doc_lemma_stpwrd_filter).lower())
del concept, doc_lemma_stpwrd_filter

####################################################
####################################################

# Corpus

try:
    list_of_posts = []
    with open(file_corpus, "r") as t:
        for line in t:
            list_of_posts.append(line.strip("\n").strip(" "))
    del t, line
    list_of_posts = list(filter(None, list_of_posts))
    logging.info("Sucessfully imported corpus")
except:
    logging.critical(f"Cannot find corpus, recheck:\t{file_corpus}")
    if not file_corpus.endswith(".txt"):
        logging.critical("Seems like the the corpus file does not end with .txt")
    sys.exit(1)

logging.info(f"Corpus line count:\t{len(list_of_posts)}")

word_count_average = [len(x.split()) for x in list_of_posts]
word_count_average = (sum(word_count_average)/len(word_count_average))

logging.info(f"Average word count in corpus:\t{round(word_count_average, 1)}")
del word_count_average

#########################

# Clean corpus

list_of_posts_lemma_stpwrd = []
#list_of_posts_lemma_stpwrd_joined = []

for post in list_of_posts:
    doc_lemma_stpwrd_filter = clean_lower_lemma(post, "corpus", stopWordsList)
    
    #list_of_posts_lemma_stpwrd_joined.append(" ".join(doc_lemma_stpwrd_filter).lower())
    list_of_posts_lemma_stpwrd.append(doc_lemma_stpwrd_filter)
    
del post, doc_lemma_stpwrd_filter

list_of_posts_lemma_stpwrd = list(filter(None, list_of_posts_lemma_stpwrd))

####################################################
####################################################

# Remove concepts from corpus

list_of_posts_lemma_stpwrd_concepts = []
for post in list_of_posts_lemma_stpwrd:
    words = []
    for word in post:
        if word not in concepts_to_remove_formatted:
            words.append(word)
    if len(words) > 0:
        list_of_posts_lemma_stpwrd_concepts.append(" ".join(words))
del post, word, words

####################################################
####################################################

# Sorting n-grams

list_of_posts_lemma_stpwrd_concepts_grams = {}

x = 0
for post in list_of_posts_lemma_stpwrd_concepts:    
    ngram_list = []
    for n in ngram_count:
        ngrammed = ngrams(post.split(), n)
        for gram in ngrammed:
            ngram_list.append( "_".join(gram) )
    list_of_posts_lemma_stpwrd_concepts_grams[x] = [ngram_list, post, list_of_posts[x]]
    x = x + 1
del x, post, ngram_list, ngrammed, n, gram

first_index_values = [" ".join(values[0]) for values in list_of_posts_lemma_stpwrd_concepts_grams.values()]

####################################################
####################################################

# TF-IDF

start_tfidf = time.time()

tfidf_vectorizer = TfidfVectorizer()
tfidf_matrix = tfidf_vectorizer.fit_transform(first_index_values)
tfidf_df = pd.DataFrame(data=tfidf_matrix.toarray(), columns=tfidf_vectorizer.get_feature_names_out())
del tfidf_matrix, tfidf_vectorizer, first_index_values

end_tfidf = time.time() - start_tfidf
end_tfidf = str(round(end_tfidf, 2))
logging.info(f"Time taken to run TF-IDF (seconds):\t{end_tfidf}")
del start_tfidf, end_tfidf

#########################

tfidf_df['Sentence'] = list_of_posts_lemma_stpwrd_concepts # col to show original sentences
tfidf_df = tfidf_df[['Sentence'] + [col for col in tfidf_df.columns if col != 'Sentence']] # sentence first col

#########################

summary_scores = tfidf_df.drop(columns=['Sentence']).agg('mean', axis=0)
tfidf_df_sum = pd.DataFrame({'Word': summary_scores.index, 'Raw score': summary_scores.values})
del summary_scores, tfidf_df

####################################################

# Scaling

scaler = MinMaxScaler()
tfidf_df_sum['Normalised score'] = scaler.fit_transform(tfidf_df_sum[['Raw score']])
tfidf_df_sum = tfidf_df_sum.sort_values("Normalised score", ascending=False)
del scaler

#########################

df = tfidf_df_sum.copy()
df = df[df['Normalised score'] != 0]
del tfidf_df_sum

df['Raw score'] = df['Raw score'].round(decimals=3)
df['Normalised score'] = df['Normalised score'].round(decimals=3)

####################################################
####################################################

# IDEA add post for users to extrapolate/add context

#df['Post'] = df['Word'].apply(lambda x: [v[2] for v in posts_cln_lmm_stpwrd_flt_ngrm.values() if x in v[0]])
#df['Post'] = [list(set(x)) for x in df['Post'] ]
#dfexplode = df.explode('Post')

####################################################
####################################################

# Output

df.to_csv(f"{dir_output}{start_timestamp}_ranked.tsv", index=False, sep="\t")

####################################################
####################################################

if plotTFIDF:
    if not plotTFIDFlimit: plotTFIDFlimit = 30
    if not plotTFIDFcolormap: plotTFIDFcolormap = "mediumseagreen"
    
    #if plotWORDCLOUDcolormap not in list(plt.colormaps()):
    #    plotWORDCLOUDcolormap = "Set3"
    
    plt.figure(figsize=(10, 5))
    plt.style.use("seaborn-v0_8-poster")
    plt.bar(df["Word"][:plotTFIDFlimit],df["Normalised score"][:plotTFIDFlimit], color=plotTFIDFcolormap)
    plt.xticks(rotation=90, fontsize=8)
    plt.xlabel('Terms', fontsize=10)
    plt.yticks(fontsize=8)
    plt.ylabel('Average score (normalised)', fontsize=10)
    plt.title(f"Bar plot of top {plotTFIDFlimit} TF-IDF ranked terms", fontsize=12)
    plt.savefig(f"{dir_output}{start_timestamp}_ranked_plot.png", bbox_inches="tight")
    
    del plotTFIDF, plotTFIDFlimit, plotTFIDFcolormap
    
####################################################

# End of script
