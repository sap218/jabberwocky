#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: May 2021
@author: Samantha C Pendleton
@description: to grep posts from a text file, output those which include terms of interest
@GitHub: github.com/sap218/jabberwocky
"""

import click 
import json
import re
import spacy
from spacy.matcher import PhraseMatcher
nlp=spacy.load("en_core_web_sm")

def clean_text(post):
    post = post.replace("-", "")
    post = (re.sub("[^A-Za-z0-9']+", " ", post)) # keeping '
    post = (re.sub("'", "", post))
    return post.lower().strip()
     
####################################################
####################################################

@click.command()
@click.option('-k', '--keywords', 'keywords', required=True, help='list of terms and synonyms you want for grep, can be from the ontology output.')
@click.option('-t', '--textfile', 'textfile', required=True, help='JSON or TXT file of text you want annotate.')
@click.option('-p', '--parameter', 'parameter', default='NULL', help='parameter of the the JSON text data.')
@click.option('-i', '--innerparameter', 'innerparameter', default='NULL', help='inner parameter of the the JSON text data if expecting replies.')
def main(keywords, textfile, parameter, innerparameter):

    #keywords = "input/word_of_interest_with_synonyms.json"
    #keywords = "../ontology/output_ontology_label_synonyms.json"

    with open(keywords) as j: # if no ontology is given, use this json
        searching_concepts_of_interest = json.load(j)
    
    ####################################################
    
    #textfile = "../test_data/example_textfile.txt"
    
    #textfile = "../test_data/example_textfile.json"
    #parameter = "post"
    #innerparameter = "reply"
    
    if textfile.endswith('.txt'):
        with open(textfile) as t:
            raw_posts = [clean_text(post.rstrip()) for post in t]
            all_threads = [[]]
            for post in raw_posts:
                if not post: all_threads.append([])
                else: all_threads[-1].append(post)
    #elif textfile.endswith('.json'):
    else:
        parameter_comment = parameter
        parameter_inner_comment = innerparameter
        with open(textfile) as j:
            raw_json_text = json.load(j)
        all_threads = []
        for item,thread in raw_json_text.items():
            current_thread_posts = []
            for user_info in thread:
                current_thread_posts.append(clean_text(user_info[parameter_comment]))
                if parameter_inner_comment:
                    try:
                        for inner_user in user_info[parameter_inner_comment]:
                            current_thread_posts.append(clean_text(inner_user[parameter_comment]))
                            for inner_inner_user in inner_user[parameter_inner_comment]:
                                current_thread_posts.append(clean_text(inner_inner_user[parameter_comment]))
                    except:
                        pass
            all_threads.append(current_thread_posts)
    
    all_posts = [item for sublist in all_threads for item in sublist]
    
    ####################################################
     
    searching_concepts_of_interest_lemma = {}
    for term,term_synonyms in searching_concepts_of_interest.items():
        doc=nlp(term)
        lemma_term = []
        for token in doc:
            lemma_term.append(token.lemma_)
        lemma_synonym = []
        for synonym in term_synonyms:
            doc=nlp(synonym)
            lemma_ss = []
            for token in doc:
                lemma_ss.append(token.lemma_)
            lemma_synonym.append(" ".join(lemma_ss))
        searching_concepts_of_interest_lemma[" ".join(lemma_term)] = lemma_synonym
    
    ####################################################
    
    matched_term_posts = {}
    for term,synonyms in searching_concepts_of_interest_lemma.items():
        matcher = PhraseMatcher(nlp.vocab, attr='LEMMA')
        terminology_list = [term] + synonyms
        termFinder = [nlp(text) for text in terminology_list]
        matcher.add("termFinder", None, *termFinder)
        
        matched_posts_for_term = []
        for post in all_posts:
            spacy_doc = nlp(post)
            matches = matcher(spacy_doc)
            if not matches: # if empty then post did not match the symptom
                pass
            else:
                matched_posts_for_term.append(post) 
        matched_term_posts[term] = matched_posts_for_term
    
    with open('output_terms_match.json', 'w') as j:
        json.dump(matched_term_posts, j, indent=4)
    
    matched_posts = []
    for term,posts in matched_term_posts.items():
        for post in posts:
            matched_posts.append(post)
    with open('output_terms_match_raw.txt', 'w') as t:
        for post in list(set(matched_posts)):
            t.write("%s\n" % post)
        
####################################################
####################################################

if __name__ == "__main__":
    main()