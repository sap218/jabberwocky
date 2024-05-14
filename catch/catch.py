#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2024
@author: Samantha C Pendleton
@description: to grep posts from a text file, output those which include terms of interest
@GitHub: github.com/sap218/jabberwocky
"""

import json
import re
import time

import spacy
from spacy.matcher import PhraseMatcher
nlp = spacy.load("en_core_web_sm")

'''
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

'''
@click.command()
@click.option('-t', '--textfile', 'textfile', required=True, help='JSON or TXT file of text you want annotate.')
'''
#def main(keywords, textfile, parameter, innerparameter):

#keywords = "input/word_of_interest_with_synonyms.json"
#keywords = "../ontology/output_ontology_label_synonyms.json"

#with open(keywords) as j: # if no ontology is given, use this json
#    searching_concepts_of_interest = json.load(j)


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

del words_of_interest_clean

####################################################

list_of_posts = []
# with open(textfile, "r") as t:
with open("test/social_media_posts.txt", "r") as t:
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
list_of_posts_clean_stpwrd = [remove_stop_words(text, stopWords) for text in list_of_posts_clean]

del list_of_posts_clean

####################################################

statistics = [
    "concepts count: %s" % len(words_of_interest_clean_stpwrd),
    "post count: %s" % len(list_of_posts_clean_stpwrd),
    "average word count: %s" % (sum(post_stats)/len(post_stats)),
    ]
del post_stats

####################################################
####################################################

# preprocess concepts: Lemmatize
words_of_interest_clean_stpwrd_lemma = [] 
concept_patterns = [] # for matcher
for concept in words_of_interest_clean_stpwrd:
    doc = nlp(concept)
    
    lemma_item = [token.lemma_ for token in doc]
    concept_patterns.append(nlp(" ".join(lemma_item)))
    
    lemma_item = " ".join([token.lemma_ for token in doc])
    words_of_interest_clean_stpwrd_lemma.append(lemma_item)
    
del concept, doc, lemma_item
del words_of_interest, words_of_interest_clean_stpwrd

matcher = PhraseMatcher(nlp.vocab) # initialize phrase matcher
matcher.add("Concepts", None, *concept_patterns) # convert concepts into patterns

del concept_patterns

####################################################

'''
# preprocess sentences: Lemmatize
list_of_posts_clean_stpwrd_lemma = []
for response in list_of_posts_clean_stpwrd:
    doc = nlp(response)
    lemma_item = " ".join([token.lemma_ for token in doc])
    list_of_posts_clean_stpwrd_lemma.append(lemma_item)
del doc, response, lemma_item, list_of_posts_clean_stpwrd
'''

####################################################
####################################################

start_time = time.time()


matched_output_list = []
matched_output_dictionary = {}


x = 0
#for response in list_of_posts_clean_stpwrd_lemma:
for post in list_of_posts_clean_stpwrd:
    print("Sentence iteration ", x, " out of ", len(list_of_posts_clean_stpwrd))
    
    doc = nlp(post)
    
    ##
    doc = [token.lemma_ for token in doc]
    doc = nlp(" ".join(doc))
    ##

    matches = matcher(doc)
    
    if matches:
    
        matched_concepts = set()
        for match_id, start, end in matches:
            matched_span = doc[start:end]
            matched_concepts.add(matched_span.text)
            
        matched_output_list.append("ANNOTATED (%s): %s" % ( matched_concepts, list_of_posts[x]) )#post) )
        #matched_output_dictionary[post] = {"key":"ANNOTATED", "annotated":list(matched_concepts)}
        matched_output_dictionary[list_of_posts[x]] = list(matched_concepts)
        
    else: 
        matched_output_list.append("NO ANNOTATION: %s" % list_of_posts[x]) #post)
        #matched_output_dictionary[post] = {"key":"NO ANNOTATION"}
        matched_output_dictionary[list_of_posts[x]] = "NO ANNOTATION"

    x = x + 1


end_time = time.time() - start_time
print( "Seconds taken to annotate: %s" % str(round(end_time, 2)) )
del start_time, end_time

del doc, post, x
del matched_concepts, matches, matched_span, match_id, start, end


## outputs to consider:

# txt with only annotated?
# json - can include all?


####################################################
####################################################

with open('test/catch_output.json', 'w') as j:
    json.dump(matched_output_dictionary, j, indent=4)

with open('test/catch_output.txt', 'w') as t:
    for word in matched_output_list:
        t.write(word + '\n')
del t, word

####################################################

# End of script
