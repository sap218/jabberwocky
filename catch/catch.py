#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: Tue Jan 21 12:15:00 2020
@author: Samantha C Pendleton
@description: to catch
@GitHub: github.com/sap218/jabberwocky
"""

import click 
from bs4 import BeautifulSoup
import re
import json

####################################################
####################################################
####################################################
####################################################
####################################################

def souping(ontology_file):
    myfile = open(ontology_file, "rt") 
    contents = myfile.read()  
    myfile.close() 
    soup = BeautifulSoup(contents,'xml')
    return soup

def ontology_search(soup):
    finding = soup.find_all('owl:Class')
    class_synonyms = {}
    for item in finding:
        try:
            label = item.find("rdfs:label").get_text().lower()
            e = item.find_all('oboInOwl:hasExactSynonym')
            b = item.find_all('oboInOwl:hasBroadSynonym')
            n = item.find_all('oboInOwl:hasNarrowSynonym')
            r = item.find_all('oboInOwl:hasRelatedSynonym')
            current_synonyms = [[x.get_text().lower() for x in e]] # rmv []
            current_synonyms.append([x.get_text().lower() for x in b])
            current_synonyms.append([x.get_text().lower() for x in n])
            current_synonyms.append([x.get_text().lower() for x in r])
            class_synonyms[label] = current_synonyms
        except Exception as e:
            #print(e, s, item)
            pass
    return class_synonyms


def getting_search_terms_purl(keywords): # inputting the list of words file
    search_words_file = open(keywords, "r")
    words = []
    for item in search_words_file:
        words.append(item.strip("\n").strip(" ").lower())
    return words

def extracting_keywords_ontology(keywords, ontology_dict):
    searching = {}
    for item in ontology_dict:
        if item in keywords:
            searching.update({item:ontology_dict[item]})
    return searching


def finalising_terms_purl(keywords):
    for i in keywords: # flattening the lists 
        keywords[i] = [i for sublist in keywords[i] for i in sublist]    
        
    for item in keywords:
        syns = []
        for i in keywords[item]:
            i = re.sub("[)(,]", "", i)
            syns.append(i)
        keywords[item] = syns
    return keywords

def ontologyPurl(ontology, keywords):
    souped = souping(ontology) # Reading in the ontology file
    class_synonyms = ontology_search(souped) # Getting class and synonyms

    if keywords == False:
        pass
    else:
        search_terms = getting_search_terms_purl(keywords) # Reading in the list of search terms - these should be classes!  
    
    if keywords == False:
        search_terms = class_synonyms # Make all
    else:
        search_terms = extracting_keywords_ontology(search_terms, class_synonyms) # Finding those synonyms
    

    search_terms = finalising_terms_purl(search_terms) # Removing special characters and flattenning list
    
    jsonfile = json.dumps(search_terms)
    f = open("ontology_dict_class_synonyms.json","w")
    f.write(jsonfile)
    f.close()
    
    return search_terms # jsonfile

####################################################
####################################################
####################################################
####################################################
####################################################
####################################################

def opening_ontology(ontology_file): # opening the ontology
    ontology = open(ontology_file, "rt")
    contents = ontology.read()
    ontology.close()
    soup = BeautifulSoup(contents,'xml') # souped it 
    return soup

def ontology_classes(soup): # getting classes
    concepts = {}
    finding = soup.find_all('AnnotationProperty', {'abbreviatedIRI':'rdfs:label'}) 
    for item in finding:
        try:
            iri = item.find_next_sibling('IRI').get_text() # plus IRIs
            #iri = iri[1:]
            classes = item.find_next_sibling('Literal').get_text()
            concepts.update({classes.lower() : iri})
        except:
            pass
    return concepts

def ontology_synonyms(soup): # getting synonyms
    synonyms = {}
    finding = soup.find_all('AnnotationProperty', {'abbreviatedIRI':'rdfs:hasExactSynonym'})
    for item in finding:
        try:
            iri = item.find_next_sibling('IRI').get_text() # plus IRIs
            #iri = iri[1:]
            synonym = item.find_next_sibling('Literal').get_text()
            synonyms.update({synonym.lower() : iri})
        except:
            pass
    finding = soup.find_all('AnnotationProperty', {'abbreviatedIRI':'rdfs:hasBroadSynonym'})
    for item in finding:
        try:
            iri = item.find_next_sibling('IRI').get_text() # plus IRIs
            #iri = iri[1:]
            synonym = item.find_next_sibling('Literal').get_text()
            synonyms.update({synonym.lower() : iri})
        except:
            pass
    finding = soup.find_all('AnnotationProperty', {'abbreviatedIRI':'rdfs:hasNarrowSynonym'})
    for item in finding:
        try:
            iri = item.find_next_sibling('IRI').get_text() # plus IRIs
            #iri = iri[1:]
            synonym = item.find_next_sibling('Literal').get_text()
            synonyms.update({synonym.lower() : iri})
        except:
            pass
    finding = soup.find_all('AnnotationProperty', {'abbreviatedIRI':'rdfs:hasRelatedSynonym'})
    for item in finding:
        try:
            iri = item.find_next_sibling('IRI').get_text() # plus IRIs
            #iri = iri[1:]
            synonym = item.find_next_sibling('Literal').get_text()
            synonyms.update({synonym.lower() : iri})
        except:
            pass
    return synonyms


def getting_search_terms_w3(file): # inputting the list of words file
    search_words_file = open(file, "r")
    search_words = {}
    for word in search_words_file:
        search_words[(word.strip("\n").strip(" ").lower())] = [] # as a dictionary
    search_words_file.close()
    return search_words
def get_classterms_synonyms(classterms, classes, synonyms): # getting the words/classes their synonyms
    for item in classterms:
        try:
            iri = classes[item]
            for syn in synonyms:
                if synonyms[syn] == iri:
                    classterms[item].append(syn)
        except:
            pass
    return classterms
def matching_class_syns(classes, synonyms):
    for iri in classes:
        i = classes[iri]
        list_of_syns = []
        for syn in synonyms:
            s = synonyms[syn]
            if i == s:
                list_of_syns.append(syn)
        classes[iri] = list_of_syns
    return classes


def finalising_terms_w3(keywords):
    for item in keywords:
        syns = []
        for i in keywords[item]:
            i = re.sub("[)(,]", "", i)
            syns.append(i)
        keywords[item] = syns
    return keywords




def ontologyW3(ontology, keywords):
    soup = opening_ontology(ontology) # Reading in the ontology
    ontology_class_terms = ontology_classes(soup) # Extracting the classes
    ontology_synonym_terms = ontology_synonyms(soup) # Extracting the synonyms
    
    if keywords == False:
        pass
    else:
        search_terms = getting_search_terms_w3(keywords) # Reading in the list of search terms, these should be classes     

    if keywords == False:
        search_terms = matching_class_syns(ontology_class_terms, ontology_synonym_terms)
    else:
        search_terms = get_classterms_synonyms(search_terms, ontology_class_terms, ontology_synonym_terms) # Getting their synonyms
    
    search_terms = finalising_terms_w3(search_terms) # Removing special characters
    # search_terms
    
    #############################
    
    jsonfile = json.dumps(search_terms)
    f = open("ontology_dict_class_synonyms.json","w")
    f.write(jsonfile)
    f.close()
    
    return search_terms #jsonfile

####################################################
####################################################
####################################################
####################################################
####################################################

def unformatted_file(textfile):
    list_of_text = []
    with open(textfile) as inputfile:
        for line in inputfile:
            if line == "\n":
                pass
            else:
                list_of_text.append(line.strip())
    inputfile.close()
    return list_of_text


def json_get(filename):
    with open(filename) as f_in:
        return(json.load(f_in)) # importing JSON
        
def querying_list_of_dicts(file, parameter):
    posts = []
    for item in file:
        if parameter in item:
            posts.append(item[parameter])
        else:
            for further_item in item:
                if parameter in further_item:
                    posts.append(further_item[parameter])
    return posts

def querying_dicts(file, parameter):
    posts = []
    for k,v in file.items():
        if parameter in v:
            posts.append(v[parameter])
        else:
            for ik,iv in v.items():
                if parameter in iv:
                    posts.append(iv[parameter])
    return posts


def organising(list_of_posts):
    posts = []
    for item in list_of_posts:
        if type(item) is str:
            posts.append(item)
        else:
            posts.append(" ".join(item))
    return posts

def cleaning_special_characters(list_of_posts):
    cleaned_posts = []
    for posts in list_of_posts:
        post = (re.sub("[^A-Za-z0-9']+", " ", posts)) # keeping '
        p = (re.sub("'", "", post)) # now removing '
        cleaned_posts.append(p.lower())
    return cleaned_posts

def tokenising(cleaned_threads):
    tokens = []
    for post in cleaned_threads:
        tokens.append(post.split()) # single words
    return tokens

def ngram_function(input, n): # https://stackoverflow.com/a/13424002
    input = input.split(' ')
    output = []
    for i in range(len(input)-n+1):
        output.append(input[i:i+n])
    return output
def performing_ngrams(list_of_posts, n):
    ngrams = []
    for post in list_of_posts:
        bigrams = [' '.join(x) for x in ngram_function(post, n)]
        ngrams.append(bigrams)
    return ngrams

def textmining(textfile, parameter):
    if textfile.endswith('.txt'):
        unstructured_posts = unformatted_file(textfile)
    
    elif textfile.endswith('.json'):
        jsonfile = json_get(textfile) # Retrieved text file
        try:
            unstructured_posts = querying_dicts(jsonfile, parameter)
        except:
            unstructured_posts = querying_list_of_dicts(jsonfile, parameter)

    structured_posts = organising(unstructured_posts) # Combing potential lists together
    cleaned_posts = cleaning_special_characters(structured_posts) # Cleaned posts file of special characters
    
    post_tokens = tokenising(cleaned_posts) # Tokenised for indivdual words
    
    return cleaned_posts, post_tokens

####################################################
####################################################

def dictionary_to_list(dictionary):
    list_of_terms = []
    for key, value in dictionary.items():
        temp = [key,value]
        list_of_terms.append(temp)
    dictionary = [item for sublist in list_of_terms for item in sublist] # flattening inner lists
    return dictionary

def flattening_dict_list(dictionary_list):
    flat_dict_list = []
    for item in dictionary_list:
        if type(item) is str:
            flat_dict_list.append(item)
        else:
            for i in item:
                flat_dict_list.append(i)  
    return flat_dict_list


def searching_indexes(keywords, post_tokens, list_of_posts):
    result = []
    for term in keywords:
        if " " in term:
            x = 0
            
            n = (term.count(" ")+1)
            ngramming = performing_ngrams(list_of_posts, n)
            
            for post in ngramming:
                for gram in post:
                    if term == gram:
                        #result.append(post)
                        result.append(x)
                x = x + 1
        else:
            x = 0
            for post in post_tokens:
                for token in post:
                    if term == token:
                        #result.append(post)
                        result.append(x)
                x = x + 1
    result = list(set(result))
    return result

def index_to_post(indexes, posts):
    result = []
    for number in indexes:
        result.append(posts[number])
    return result

def annotating(jsonfile, cleaned_posts, post_tokens):
    ontology_class_syns = json_get("ontology_dict_class_synonyms.json")
    #ontology_class_syns = json_get(jsonfile)
    list_of_dictionary_terms = dictionary_to_list(ontology_class_syns) # Making dictionary into list & flattening inner lists
    search_terms = flattening_dict_list(list_of_dictionary_terms) # Flattening inner lists
    indexes = searching_indexes(search_terms, post_tokens, cleaned_posts) # Searching & retrieving indexes 
    result = index_to_post(indexes, cleaned_posts)  # Getting the post from the index

    return result

####################################################
####################################################
####################################################
####################################################
####################################################
####################################################
####################################################
####################################################
####################################################
####################################################

@click.command()
@click.option('--ontology', default='NULL', help='file of ontology.')
@click.option('--keywords', default='NULL', help='list of classes/terms you want to use to search.')
@click.option('--textfile', default='NULL', help='JSON ot TXT file of text you want annotate.')
@click.option('--parameter', default='NULL', help='parameter for the JSON file text.')
def main(ontology, keywords, textfile, parameter):
    if ontology == "NULL":
        print("No ontology file provided. Cannot continue.")
        exit()
    if keywords == "NULL":
        keywords = False
        #print("No keywords file provided. Cannot continue.")
        #exit()
    if textfile == "NULL":
        print("No text file provided. Cannot continue.")
        exit()
    if textfile.endswith('.json') and parameter == "NULL":
        print("Need parameter for tags extraction w/ JSON.")
        exit()
    
    
    #print("trying purl")
    search_term_dictionary = ontologyPurl(ontology, keywords)
    #print("purl" + str(search_term_dictionary), len(search_term_dictionary))
    if len(search_term_dictionary) == 0:
        #print("falling back to w3")
        search_term_dictionary = ontologyW3(ontology, keywords)
        #print("w3" + search_term_dictionary)
    
    texts = textmining(textfile, parameter)
    
    annotations = annotating(search_term_dictionary, texts[0], texts[1])
    
    for post in annotations:
        print(post + "\n")
    
#############################

if __name__ == "__main__":
    main()
