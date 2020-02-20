#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: Tue Jan 21 12:15:00 2020
@author: Samantha C Pendleton
@description: to catch
@GitHub: github.com/sap218/jabberwocky
"""

import click 
import json
import re
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
from bs4 import BeautifulSoup

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


def flattening_classes_purl(class_synonyms):
    ontology_terms = []
    for classes,synonyms in class_synonyms.items(): # unraveling the dictionary
        ontology_terms.append(classes)
        for value in synonyms:
            ontology_terms.append(value)
            
    final_terms = []
    for item in ontology_terms:
        if type(item) is str:
            final_terms.append(item)
        else:
            for v in item:
                final_terms.append(v) # removes blank lists only adds list items
    return final_terms
    
def cleaning_purl_terms(ontology_terms):
    final_terms = []
    for term in ontology_terms:
        term = (re.sub("[^A-Za-z0-9']+", " ", term))
        t = (re.sub("'", "", term)) # now removing '
        final_terms.append(t.lower())
    return final_terms



def ontology_purl(ontology):  
    souped = souping(ontology) # Reading in the ontology file
    class_synonyms = ontology_search(souped) # Getting class and synonyms
    
    ontology_terms = flattening_classes_purl(class_synonyms) # Unraveling the dictionary
    final_terms = cleaning_purl_terms(ontology_terms) # Cleaning special chars
    
    with open('ontology_all_terms.txt', 'w') as writer:
        for term in final_terms:
            writer.write(term + "\n")
    writer.close()
    
    return final_terms

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



def flattening_w3(ontology_class_terms, ontology_synonym_terms):
    ontology_terms = []
    for k in ontology_class_terms:
        ontology_terms.append(k)
    for k in ontology_synonym_terms:
        ontology_terms.append(k)
    return ontology_terms

def cleaning_w3_terms(ontology_terms):
    final_terms = []
    for term in ontology_terms:
        term = (re.sub("[^A-Za-z0-9']+", " ", term))
        t = (re.sub("'", "", term)) # now removing '
        final_terms.append(t.lower())
    return final_terms



def ontology_w3(ontology):
    soup = opening_ontology(ontology) # Reading in the ontology
    ontology_class_terms = ontology_classes(soup) # Extracting the classes
    ontology_synonym_terms = ontology_synonyms(soup) # Extracting the synonyms
    
    ontology_terms = flattening_w3(ontology_class_terms, ontology_synonym_terms) # Flattening classes & synonyms
    final_terms = cleaning_w3_terms(ontology_terms) # Removing special chars
    
    with open('ontology_all_terms.txt', 'w') as writer:
        for term in final_terms:
            writer.write(term + "\n")
    writer.close()
    
    return final_terms

####################################################
####################################################
####################################################
####################################################
####################################################

def json_get(filename):
    with open(filename) as f_in:
        return(json.load(f_in)) # importing JSON
        
        
def querying_list_of_dicts(jsonfile, parameter):
    posts = []
    for item in jsonfile:
        p = []
        if parameter in item:
            p.append(item[parameter])
        else:
            for further_item in item:
                if parameter in further_item:
                    p.append(further_item[parameter])
        posts.append(p)
    return posts

def querying_dicts(jsonfile, parameter):
    posts = []
    for k,v in jsonfile.items():
        p = []
        if parameter in v:
            p.append(v[parameter])
        else:
            for ik,iv in v.items():
                if parameter in iv:
                    p.append(iv[parameter])
        posts.append(p)
    return posts
    

def flattens(unstructured_posts):
    try: # small
        threads = []
        for posts in unstructured_posts:
            posts = " ".join(posts)
            threads.append(posts)
    except: # larger
        flat_threads = []
        for thread in unstructured_posts:
            flat_posts = [item for sublist in thread for item in sublist]
            flat_threads.append(flat_posts)
        
        threads = []
        for item in flat_threads:
            item = " ".join(item)
            threads.append(item)
    return threads


def cleaning_special_characters(list_of_threads):
    cleaned_posts = []
    for thread in list_of_threads:
        post = (re.sub("[^A-Za-z0-9']+", " ", thread)) # keeping '
        p = (re.sub("'", "", post)) # now removing '
        cleaned_posts.append(p.lower())
    return cleaned_posts


def tokenising(cleaned_threads):
    tokens = []
    for post in cleaned_threads:
        tokens.append(post.split()) # single words
    return tokens



def stopword_deletion(post_tokens):
    stop_words = [ # https://gist.github.com/sebleier/554280#gistcomment-2860409
            "a","about","ain","any","aren","aren't","arent","arnt","as","at","able","abst","accordance","according","accordingly","across","act","actually","added","adj","affected","affecting","affects","afterwards","ah","almost","alone","along","already","also","although","always","among","amongst","announce","another","anybody","anyhow","anymore","anyone","anything","anyway","anyways","anywhere","apparently","approximately","arise","aside","ask","asking","auth","available","away","awfully","a's","ain't","aint","allow","allows","apart","appear","appreciate","appropriate","associated","above","after","again","against","all","am","amoungst","amount","and","are","around",
            "b","begin","beginning","beginnings","begins","believe","biol","brief","briefly","best","better","back","became","because","become","becomes","becoming","been","before","beforehand","behind","being","below","beside","besides","between","beyond","bill","both","bottom","but","by",
            "c","can","could","couldn","couldn't","couldnt","ca","came","cannot","can't","cant","cause","causes","certain","certainly","com","come","comes","contain","containing","contains","c'mon","cmon","c's","changes","clearly","concerning","consequently","consider","considering","corresponding","course","currently","call","con","cry",
            "d","did","didn","didn't","didnt","does","doesn","doesn't","doesnt","doing","don","don't","dont","down","during","date","different","done","downwards","due","definitely","described","despite","describe","detail",
            "e","edu","effect","eighty","end","ending","especially","everybody","entirely","exactly","example","each","eg","eight","either","eleven","else","elsewhere","empty","enough","etc","even","ever","every","everyone","everything","everywhere","except",
            "f","far","fifth","fix","followed","following","follows","forth","furthermore","few","fifteen","fify","fill","find","fire","first","five","for","former","formerly","forty","found","four","from","front","full","further",
            "g","gave","get","gets","getting","give","given","gives","giving","goes","gone","got","gotten","going","greetings",
            "h","hadn","hadn't","hadnt","hasn","hasn't","haven","haven't","havent","having","here","he'd","he'll","hell","he's","here's","how's","hows","happens","happened","hardly","hed","heres","hes","hid","hither","home","howbeit","hello","help","hopefully","had","has","hasnt","have","he","hence","her","hereafter","hereby","herein","hereupon","hers","herself","him","himself","his","how","however","hundred",
            "i","isn","is","isn't","isnt","it","it's","its","itself","i'd","id","i'll","ill","i'm","im","i've","ive","immediate","immediately","importance","important","indeed","index","information","instead","invention","inward","itd","it'll","itll","ignored","inasmuch","indicate","indicated","indicates","inner","insofar","it'd","if","inc","interest","into",
            "j","just",
            "k","keep","keeps","kept","know","known","knows",
            "l","ll","let's","lets","largely","lately","later","latterly","least","less","lest","let","like","liked","likely","line","little","'ll","look","looking","looks","last","latter","ltd",
            "m","ma","mightn","mightn't","mightnt","mustn","mustn't","mustnt","mainly","make","makes","maybe","mean","means","meantime","merely","mg","million","miss","mr","mrs","mug","made","many","may","me","meanwhile","might","mill","mine","more","moreover","most","mostly","move","much","must","my","myself",
            "n","needn","needn't","neednt","na","nay","near","nearly","necessarily","necessary","need","needs","new","ninety","non","nonetheless","normally","nos","noted","novel","name","namely","neither","never","nevertheless","next","nine","no","nobody","none","noone","nor","not","nothing","now","nowhere",
            "o","ought","obtain","obtained","obviously","oh","ok","okay","old","omitted","ones","ord","outside","overall","owing","off","often","once","one","only","onto","other","others","otherwise","our","ours","ourselves","out","over","own",
            "p","page","pages","part","particular","particularly","past","per","perhaps","placed","please","plus","poorly","possible","possibly","potentially","predominantly","present","previously","primarily","probably","promptly","proud","provides","put","presumably",
            "q","quickly","quite","qv",
            "r","ran","readily","really","recent","recently","ref","refs","regarding","regardless","regards","related","relatively","research","respectively","resulted","resulting","results","right","run","reasonably","rather","re",
            "s","shan","shan't","shant","she's","should've","shouldve","shouldn","shouldn't","shouldnt","she'd","she'll","shell","said","saw","say","saying","says","sec","section","seeing","seen","self","selves","sent","seven","shall","shes","showed","shown","showns","shows","significant","significantly","similar","similarly","slightly","somebody","somethan","somewhat","soon","sorry","specifically","specified","specify","specifying","stop","strongly","sub","substantially","successfully","sufficiently","suggest","sup","second","secondly","sensible","seriously","sure","same","see","seem","seemed","seeming","seems","serious","several","she","should","show","side","since","sincere","six","sixty","so","some","somehow","someone","something","sometime","sometimes","somewhere","still","such","system", 
            "t","that'll","thatll","theirs","that's","there's","they'd","they'll","theyll","they're","they've","theyve","taken","taking","tell","tends","thank","thanks","thanx","thats","that've","thatve","thered","there'll","therell","thereof","therere","theres","thereto","there've","thereve","theyd","theyre","think","thou","thousand","throug","til","tip","took","tried","tries","truly","try","trying","twice","t's","thorough","thoroughly","take","ten","than","that","the","their","them","themselves","then","thence","there","thereafter","thereby","therefore","therein","thereupon","these","they","thickv","thin","third","this","those","though","three","through","throughout","thru","thus","to","together","too","top","toward","towards","twelve","twenty","two",
            "u","under","until","up","unfortunately","unless","unlike","unlikely","unto","upon","ups","us","use","used","useful","usefully","usefulness","uses","using","usually",
            "v","ve","very","value","various","'ve","via","viz","vols","vs",
            "w","wasn","wasn't","weren","weren't","won","won't","wouldn","wouldn't","we'd","we'll","we're","we've","weve","what's","when's","whens","where's","who's","why's","whys","want","wants","wasnt","way","wed","welcome","went","werent","what'll","whatll","whats","wheres","whim","whod","who'll","wholl","whomever","whos","widely","willing","wish","wont","words","world","wouldnt","www","wonder","was","we","well","were","what","whatever","when","whence","whenever","where","whereafter","whereas","whereby","wherein","whereupon","wherever","whether","which","while","whither","who","whoever","whole","whom","whose","why","will","with","within","without","would",
            "x"
            "y","you","you'd","youd","you'll","youll","you're","youre","you've","youve","your","yours","yourself","yourselves","yes","yet",
            "z","zero",
            
            "co","op","research-articl","pagecount","cit","ibid","les","le","au","que","est","pas","vol","los","pp","u201d","well-b","http","volumtype","par",
            "0o","0s","3a","3b","3d","6b","6o",
            "a1","a2","a3","a4","ab","ac","ad","ae","af","ag","aj","al","an","ao","ap","ar","av","aw","ax","ay","az",
            "b1","b2","b3","ba","bc","bd","be","bi","bj","bk","bl","bn","bp","br","bs","bt","bu","bx",
            "c1","c2","c3","cc","cd","ce","cf","cg","ch","ci","cj","cl","cm","cn","cp","cq","cr","cs","ct","cu","cv","cx","cy","cz",
            "d2","da","dc","dd","de","df","di","dj","dk","dl","do","dp","dr","ds","dt","du","dx","dy",
            "e2","e3","ea","ec","ed","ee","ef","ei","ej","el","em","en","eo","ep","eq","er","es","et","eu","ev","ex","ey",
            "f2","fa","fc","ff","fi","fj","fl","fn","fo","fr","fs","ft","fu","fy",
            "ga","ge","gi","gj","gl","go","gr","gs","gy",
            "h2","h3","hh","hi","hj","ho","hr","hs","hu","hy",
            "i2","i3","i4","i6","i7","i8","ia","ib","ic","ie","ig","ih","ii","ij","il","in","io","ip","iq","ir","iv","ix","iy","iz",
            "jj","jr","js","jt","ju",
            "ke","kg","kj","km","ko",
            "l2","la","lb","lc","lf","lj","ln","lo","lr","ls","lt",
            "m2","ml","mn","mo","ms","mt","mu",
            "n2","nc","nd","ne","ng","ni","nj","nl","nn","nr","ns","nt","ny",
            "oa","ob","oc","od","of","og","oi","oj","ol","om","on","oo","oq","or","os","ot","ou","ow","ox","oz",
            "p1","p2","p3","pc","pd","pe","pf","ph","pi","pj","pk","pl","pm","pn","po","pq","pr","ps","pt","pu","py",
            "qj","qu",
            "r2","ra","rc","rd","rf","rh","ri","rj","rl","rm","rn","ro","rq","rr","rs","rt","ru","rv","ry",
            "s2","sa","sc","sd","se","sf","si","sj","sl","sm","sn","sp","sq","sr","ss","st","sy","sz",
            "t1","t2","t3","tb","tc","td","te","tf","th","ti","tj","tl","tm","tn","tp","tq","tr","ts","tt","tv","tx",
            "ue","ui","uj","uk","um","un","uo","ur","ut",
            "va","wa","vd",
            "wi","vj","vo","wo","vq","vt","vu",
            "x1","x2","x3","xf","xi","xj","xk","xl","xn","xo","xs","xt","xv","xx",
            "y2","yj","yl","yr","ys","yt",
            "zi","zz",
            ]
    
    threads_wout_stopwords = [] 
    for post in post_tokens:
        posts_wout_stopwords = []
        for token in post:
            if token not in stop_words:
                posts_wout_stopwords.append(token)
        threads_wout_stopwords.append(posts_wout_stopwords)
    return threads_wout_stopwords


##### ontology handling

def get_ontology_terms(ont_file):
    ontology_terms = []
    with open(ont_file, 'r') as reader:
        for line in reader:
            ontology_terms.append(line.strip())
    reader.close()
    return ontology_terms

def splitting_ontology_terms(ontol_terms):
    terms_split = []
    for term in ontol_terms:
        terms_split.append(term.split(" "))
        
    ontol_terms_split = []
    for list_terms in terms_split:
        for item in list_terms:
            ontol_terms_split.append(item)
    
    return list(set(ontol_terms_split))




def remove_ont_terms_from_text(ontol_terms, post_tokens):
    post_tokens_wout_sw_wout_ont = []
    
    for post in post_tokens:
        post_wout_ont = []
        for token in post:
            if token in ontol_terms:
                pass
            else:
                post_wout_ont.append(token)
        post_tokens_wout_sw_wout_ont.append(post_wout_ont)
        
        
    threads_list = []
    for posts in post_tokens_wout_sw_wout_ont:
        threads_list.append(" ".join(posts))
    
    return threads_list



def tfidf_analysis(threads_list):
    vectorizer = TfidfVectorizer() # https://towardsdatascience.com/natural-language-processing-feature-engineering-using-tf-idf-e8b9d00e7e76
    vectors = vectorizer.fit_transform(threads_list)
    
    feature_names = vectorizer.get_feature_names() # each word
    dense = vectors.todense()
    denselist = dense.tolist()
    tfidf_density = pd.DataFrame(denselist, columns=feature_names) # word and word density
    
    tfidf_sums = tfidf_density.sum(axis = 0, skipna = True) # counting each word densities
    tfidf_word_sums = tfidf_sums.to_dict() # zipping sum to the word
    
    tfidf = pd.DataFrame(tfidf_word_sums.items(), columns=['words', 'count']) # putting into dataframe
    tfidf = tfidf.sort_values("count", ascending=False)
    tfidf.to_csv('tfidf_results.csv', index=False)
    
    return tfidf




def text_statistics(textfile, parameter, ontology, final_terms):
    jsonfile = json_get(textfile) # Retrieved text file
    
    try:
        unstructured_posts = querying_dicts(jsonfile, parameter)
    except:
        unstructured_posts = querying_list_of_dicts(jsonfile, parameter)
    
    structured_posts = flattens(unstructured_posts) # Flattening posts for threads
    cleaned_posts = cleaning_special_characters(structured_posts) # Cleaned posts file of special characters
    post_tokens = tokenising(cleaned_posts) # Tokenised for indivdual words
    post_tokens_wout_stopwords = stopword_deletion(post_tokens) # Removing stop words
    
    
    if ontology == False:
        threads_list = []
        for post in post_tokens_wout_stopwords:
            threads_list.append(" ".join(post))
    else:
        #ontol_file = 'ontology_all_terms.txt'
        #ontol_terms = get_ontology_terms(ontol_file) # Getting the ontology terms
        ontol_terms_split = splitting_ontology_terms(final_terms) # Splitting the ontology terms
        
        threads_list = remove_ont_terms_from_text(ontol_terms_split, post_tokens_wout_stopwords) # Removing ontology terms from text & joining the tokens back up
    
    
    return tfidf_analysis(threads_list) # TF-IDF 


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
@click.option('-o', '--ontology', 'ontology', default=False, help='file of ontology.')
@click.option('-t', '--textfile', 'textfile', required=True, help='JSON file of text you want to observe.')
@click.option('-p', '--parameter', 'parameter', required=True, help='parameter for the JSON file text.')
def main(ontology, textfile, parameter):
    
    if ontology == False:
        final_terms = False
    else:
        final_terms = ontology_purl(ontology)
        if len(final_terms) == 0:
            final_terms = ontology_w3(ontology)
    
    results = text_statistics(textfile, parameter, ontology, final_terms)
    
    print(results)
    
#############################

if __name__ == "__main__":
    main()
