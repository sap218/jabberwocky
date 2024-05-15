#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2024
@author: Samantha C Pendleton
@description: to curate terms of interest via tf-idf
@GitHub: github.com/sap218/jabberwocky

@useful links:
    # https://gist.github.com/sebleier/554280#gistcomment-2860409
    # https://towardsdatascience.com/natural-language-processing-feature-engineering-using-tf-idf-e8b9d00e7e76
"""

import json
import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
import matplotlib.pyplot as plt

import spacy
nlp = spacy.load("en_core_web_sm")

####################################################

'''
def tokenising(post):
    post_tokens = post.split()
    return post_tokens

def clean_text(post):
    post = post.replace("-", "")
    post = (re.sub("[^A-Za-z0-9']+", " ", post)) # keeping '
    post = (re.sub("'", "", post))
    return post.lower().strip()
'''

def cleantext(post):
    post = re.sub(' +', ' ', post) # double spaces
    post = re.sub("[^A-Za-z0-9']+", " ", post).replace("'", "").strip()
    return post

# https://gist.github.com/sebleier/554280?permalink_comment_id=2639949#gistcomment-2639949
stopWords = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"]
stopWords = [cleantext(x.lower()) for x in stopWords]

def remove_stop_words(text, stopWords):
    return ' '.join(word for word in text.split() if word.lower() not in stopWords)

####################################################

#@click.option('-g', '--graph', 'graph', default=False, help='make True if you want a plot of top 30 terms.')
#@click.option('-l', '--limit', 'limit', default='NULL', help='change if want a different plot limit.')
#def main(keywords, textfile, parameter, innerparameter, graph, limit):


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
    words_of_interest_clean_stpwrd = [remove_stop_words(text, stopWords) for text in words_of_interest_clean]
    
    # preprocess concepts: Lemmatize
    words_of_interest_clean_stpwrd_lemma = []
    for concept in words_of_interest_clean_stpwrd:
        doc = nlp(concept)
        lemma_item = " ".join([token.lemma_ for token in doc])
        words_of_interest_clean_stpwrd_lemma.append(lemma_item)
    del doc, concept, lemma_item    
    
    del words_of_interest_clean, words_of_interest_clean_stpwrd


else:
    words_of_interest_clean_stpwrd_lemma = []




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
list_of_posts_clean_stpwrd = [remove_stop_words(text, stopWords) for text in list_of_posts_clean]

del list_of_posts_clean

####################################################

# catch output but looking at no annotations

list_of_posts = []
# with open(textfile, "r") as t:
with open("../catch/test/catch_output.txt", "r") as t:
    for post in t:
        post = post.strip("\n").strip(" ")
        post = post.split(":", 1)
        if "NO ANNOTATION" in post[0]:
            list_of_posts.append(post[1])
del t, post

list_of_posts_clean = [cleantext(x.lower()) for x in list_of_posts]
list_of_posts_clean_stpwrd = [remove_stop_words(text, stopWords) for text in list_of_posts_clean]

del list_of_posts_clean

####################################################

# preprocess sentences: Lemmatize
list_of_posts_clean_stpwrd_lemma = []
for post in list_of_posts_clean_stpwrd:
    doc = nlp(post)
    lemma_item = " ".join([token.lemma_ for token in doc])
    list_of_posts_clean_stpwrd_lemma.append(lemma_item)
del doc, post, lemma_item, list_of_posts_clean_stpwrd

####################################################
####################################################

list_of_posts_clean_stpwrd_lemma_filtered = []
for sentence in list_of_posts_clean_stpwrd_lemma:
    sentence = sentence.split()
    
    for word in words_of_interest_clean_stpwrd_lemma:
        word = word.split()
        
        sentence = [w for w in sentence if w not in word]
        
    list_of_posts_clean_stpwrd_lemma_filtered.append(" ".join(sentence))

del sentence, word
del list_of_posts_clean_stpwrd_lemma

####################################################
####################################################


tfidf_vectorizer = TfidfVectorizer()
tfidf_matrix = tfidf_vectorizer.fit_transform(list_of_posts_clean_stpwrd_lemma_filtered)
feature_names = tfidf_vectorizer.get_feature_names_out()


tfidf_df = pd.DataFrame(tfidf_matrix.toarray(), columns=feature_names)
tfidf_df['Sentence'] = list_of_posts_clean_stpwrd_lemma_filtered # col to show original sentences
tfidf_df = tfidf_df[['Sentence'] + [col for col in tfidf_df.columns if col != 'Sentence']] # sentence first col
del tfidf_matrix, tfidf_vectorizer, feature_names


summary_scores = tfidf_df.drop(columns=['Sentence']).agg('mean', axis=0)
summary_df = pd.DataFrame({'Word': summary_scores.index, 'Score': summary_scores.values})
del summary_scores, tfidf_df


from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()
summary_df['Score'] = scaler.fit_transform(summary_df[['Score']])
summary_df = summary_df.sort_values("Score", ascending=False)
summary_df.to_csv('test/tfidf.tsv', index=False, sep="\t")


####################################################
####################################################
'''
#graph = True
#limit = "NULL"

if limit == "NULL":
    limit = 30

if graph:
    fig = plt.figure()
    ax = fig.add_axes([0,0,1,1])
    ax.bar(tfidf["words"][:limit],tfidf["count"][:limit], color='steelblue')
    plt.xticks(rotation=90)
    ax.set_ylabel('Score')
    ax.set_xlabel('Term')
    ax.set_title('Bar plot of mean tf-idf for top %s terms' % limit)
    #plt.show()
    plt.savefig('tfidf_plot.pdf', bbox_inches='tight')
'''

####################################################

# End of script
