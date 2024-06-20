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

import sys
import re
import time
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MinMaxScaler

import spacy
nlp = spacy.load("en_core_web_sm")

from params_bite import *

####################################################

from highlevel import *

''' stopWords '''
if filter_level == "light": stopWords = stopWords[0]
elif filter_level == "heavy": stopWords = stopWords[1]
stopWords = [cleantext(x.lower()) for x in stopWords]

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

if len(concepts_to_remove) > 0:
    try:
        words_of_interest = []
        with open("%s.txt" % concepts_to_remove, "r") as t:
            for word in t:
                words_of_interest.append(word.strip("\n").strip(" "))
        del t, word
    except FileNotFoundError:
        sys.exit("User attempted to provide a list of concepts to remove from TF-IDF - unsuccessful")
else: words_of_interest = ["nowordstofilter"]

words_of_interest = list(filter(None, words_of_interest))

####################################################

words_of_interest_clean_lemma_stpwrd = [] 

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
        words_of_interest_clean_lemma_stpwrd.append(" ".join(doc_lemma_stpwrd))
    
del concept, doc, doc_lemma, doc_lemma_stpwrd

####################################################
####################################################

list_of_posts = []

with open("%s.txt" % corpus, "r") as t:
    for post in t:
        list_of_posts.append(post.strip("\n").strip(" "))
del t, post
list_of_posts = list(filter(None, list_of_posts))

####################################################

list_of_posts_clean_lemma_stpwrd = []

for post in list_of_posts:
    post = cleantext(post.lower())
    
    doc = nlp(post)
    
    ## lemma
    doc_lemma = [token.lemma_ for token in doc]
    ## stopwords
    doc_lemma_stpwrd = [remove_stop_words(text, stopWords) for text in doc_lemma]
    doc_lemma_stpwrd = list(filter(None, doc_lemma_stpwrd))
        
    list_of_posts_clean_lemma_stpwrd.append(" ".join(doc_lemma_stpwrd))
del post,doc,doc_lemma,doc_lemma_stpwrd

####################################################
####################################################

words_of_interest_clean_lemma_stpwrd.append("evolve")
words_of_interest_clean_lemma_stpwrd.append("team rocket")

list_of_posts_clean_lemma_stpwrd.append("evolve")

####################################################
####################################################

def remove_phrases(sentences, phrases):
    cleaned_sentences = []
    for sentence in sentences:
        for phrase in phrases:
            sentence = sentence.replace(phrase, '')
        sentence = re.sub(' +', ' ', sentence).strip() # remove double whitespace
        cleaned_sentences.append(sentence)
    return cleaned_sentences

list_of_posts_clean_lemma_stpwrd_filtered = remove_phrases(list_of_posts_clean_lemma_stpwrd, words_of_interest_clean_lemma_stpwrd)

####################################################
####################################################

start_time = time.time()

tfidf_vectorizer = TfidfVectorizer()
tfidf_matrix = tfidf_vectorizer.fit_transform(list_of_posts_clean_lemma_stpwrd_filtered)
feature_names = tfidf_vectorizer.get_feature_names_out()

end_time = time.time() - start_time
end_time = str(round(end_time, 3))
print( "Seconds taken to run tf-idf: %s" % end_time)
del start_time

tfidf_df = pd.DataFrame(tfidf_matrix.toarray(), columns=feature_names)
tfidf_df['Sentence'] = list_of_posts_clean_lemma_stpwrd_filtered # col to show original sentences
tfidf_df = tfidf_df[['Sentence'] + [col for col in tfidf_df.columns if col != 'Sentence']] # sentence first col
del tfidf_matrix, tfidf_vectorizer, feature_names

summary_scores = tfidf_df.drop(columns=['Sentence']).agg('mean', axis=0)
tfidf_df_sum = pd.DataFrame({'Word': summary_scores.index, 'Raw score': summary_scores.values})
del summary_scores, tfidf_df

####################################################

scaler = MinMaxScaler()
tfidf_df_sum['Normalised score'] = scaler.fit_transform(tfidf_df_sum[['Raw score']])
tfidf_df_sum = tfidf_df_sum.sort_values("Normalised score", ascending=False)
del scaler

####################################################

df = tfidf_df_sum.copy()
df = df[df['Normalised score'] != 0]

df['Raw score'] = df['Raw score'].round(decimals=3)
df['Normalised score'] = df['Normalised score'].round(decimals=3)

df.to_csv('%s.tsv' % output_name, index=False, sep="\t")

####################################################

statistics = [
    "time taken to run tf-idf: %s" % end_time,
    "tf-idf raw df length: %s" % str(len(tfidf_df_sum)),
    "tf-idf adj. df length: %s" % str(len(df))
    ]
del end_time, tfidf_df_sum

with open('%s.txt' % stats_output_name, 'w') as t:
    for word in statistics:
        t.write(word + '\n')
del t,word

####################################################

if graph:
    plt.style.use("seaborn-poster")
    fig = plt.figure()
    ax = fig.add_axes([0,0,1,1])
    ax.bar(df["Word"][:limit],df["Normalised score"][:limit], color=cm)
    plt.xticks(rotation=90)
    ax.set_ylabel('Average score (normalised)')
    ax.set_xlabel('Terms')
    ax.set_title("Bar plot of top %s TF-IDF ranked terms" % limit)
    plt.savefig('%s.png' % plot_output_name, bbox_inches='tight')
del ax, fig

####################################################

# End of script
