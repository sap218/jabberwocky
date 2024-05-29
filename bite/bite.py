#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2024
@author: Samantha C Pendleton
@description: conducts TF-IDF
@GitHub: github.com/sap218/jabberwocky

@useful links:
    # https://python-charts.com/matplotlib/styles/
"""

import re
import time
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MinMaxScaler

import spacy
nlp = spacy.load("en_core_web_sm")

####################################################

from highlevel import *

''' stopWords '''
stopWords = [cleantext(x.lower()) for x in stopWords]

def remove_stop_words(text, stopWords):
    return ' '.join(word for word in text.split() if word.lower() not in stopWords)

####################################################

concepts_to_remove = True

if concepts_to_remove:

    words_of_interest = []
    # with open(keywords, "r") as t:
    
    with open("../bandersnatch/test/words_of_interest.txt", "r") as t:
        for word in t:
            words_of_interest.append(word.strip("\n").strip(" "))
    
    with open("../bandersnatch/test/snatch_output.txt", "r") as t:
        for word in t:
            words_of_interest.append(word.strip("\n").strip(" "))
    
    del t, word
    
    words_of_interest_clean = [cleantext(x.lower()) for x in words_of_interest]
    #words_of_interest_clean_stpwrd = [remove_stop_words(text, stopWords) for text in words_of_interest_clean]
    
    # preprocess concepts: Lemmatize
    words_of_interest_clean_lemma = []
    for concept in words_of_interest_clean:
        doc = nlp(concept)
        lemma_item = " ".join([token.lemma_ for token in doc])
        words_of_interest_clean_lemma.append(lemma_item)
    del doc, concept, lemma_item    
    
    words_of_interest_clean_lemma_stpwrd = [remove_stop_words(text, stopWords) for text in words_of_interest_clean_lemma]
    
    del words_of_interest_clean, words_of_interest_clean_lemma


else:
    words_of_interest_clean_lemma_stpwrd = []


####################################################
####################################################

# original social media posts

list_of_posts = []
# with open(textfile, "r") as t:
with open("../catch/test/social_media_posts.txt", "r") as t:
    for post in t:
        list_of_posts.append(post.strip("\n").strip(" "))
del t, post
list_of_posts = list(filter(None, list_of_posts))

list_of_posts_clean = [cleantext(x.lower()) for x in list_of_posts]

#list_of_posts_clean_stpwrd = [remove_stop_words(text, stopWords) for text in list_of_posts_clean]
#del list_of_posts_clean

####################################################

# catch output but looking at no annotations

list_of_posts = []
# with open(textfile, "r") as t:
with open("../catch/test/catch_output.txt", "r") as t:
    for post in t:
        post = post.strip("\n").strip(" ")
        list_of_posts.append(post)
del t, post

list_of_posts_clean = [cleantext(x.lower()) for x in list_of_posts]

#list_of_posts_clean_stpwrd = [remove_stop_words(text, stopWords) for text in list_of_posts_clean]
#del list_of_posts_clean

####################################################

# preprocess sentences: Lemmatize
list_of_posts_clean_lemma = []
for post in list_of_posts_clean:
    doc = nlp(post)
    lemma_item = " ".join([token.lemma_ for token in doc])
    list_of_posts_clean_lemma.append(lemma_item)
del doc, post, lemma_item, list_of_posts_clean

list_of_posts_clean_lemma_stopwrd = [remove_stop_words(text, stopWords) for text in list_of_posts_clean_lemma]
del list_of_posts_clean_lemma

####################################################
####################################################

list_of_posts_clean_lemma_stpwrd_filtered = []
for sentence in list_of_posts_clean_lemma_stopwrd:
    sentence = sentence.split()
    
    for word in words_of_interest_clean_lemma_stpwrd:
        word = word.split()
        
        sentence = [w for w in sentence if w not in word]
        
    list_of_posts_clean_lemma_stpwrd_filtered.append(" ".join(sentence))

del sentence, word
del list_of_posts_clean_lemma_stopwrd

####################################################
####################################################

start_time = time.time()

tfidf_vectorizer = TfidfVectorizer()
tfidf_matrix = tfidf_vectorizer.fit_transform(list_of_posts_clean_lemma_stpwrd_filtered)
feature_names = tfidf_vectorizer.get_feature_names_out()

end_time = time.time() - start_time
print( "Seconds taken to run tf-idf: %s" % str(round(end_time, 3)) )
del start_time, end_time

tfidf_df = pd.DataFrame(tfidf_matrix.toarray(), columns=feature_names)
tfidf_df['Sentence'] = list_of_posts_clean_lemma_stpwrd_filtered # col to show original sentences
tfidf_df = tfidf_df[['Sentence'] + [col for col in tfidf_df.columns if col != 'Sentence']] # sentence first col
del tfidf_matrix, tfidf_vectorizer, feature_names


summary_scores = tfidf_df.drop(columns=['Sentence']).agg('mean', axis=0)
tfidf_df_sum = pd.DataFrame({'Word': summary_scores.index, 'Score': summary_scores.values})
del summary_scores


scaler = MinMaxScaler()
tfidf_df_sum['Score'] = scaler.fit_transform(tfidf_df_sum[['Score']])
tfidf_df_sum = tfidf_df_sum.sort_values("Score", ascending=False)
del scaler

tfidf_df_sum.to_csv('test/bite_output.tsv', index=False, sep="\t")

####################################################
####################################################

graph = True
limit = "NULL"

if limit == "NULL":
    limit = 30
    
colours = [
    "mediumseagreen",
    "steelblue",
    "lightcoral",
    ] 
color = colours[0]

plt.style.use("seaborn-poster")

if graph:
    fig = plt.figure()
    ax = fig.add_axes([0,0,1,1])
    ax.bar(tfidf_df_sum["Word"][:limit],tfidf_df_sum["Score"][:limit], color=color)
    plt.xticks(rotation=90)
    ax.set_ylabel('Average score (normalised)')
    ax.set_xlabel('Terms')
    ax.set_title("Bar plot of top %s terms TF-IDF rankings" % limit)
    #plt.savefig('test/tfidf_plot.pdf', bbox_inches='tight')
    plt.savefig('test/top%s_terms.png' % limit, bbox_inches='tight')
del ax, fig

####################################################

# End of script
