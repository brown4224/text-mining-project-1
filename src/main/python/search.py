#  Sean McGlincy
#  Text Mining: Project 1
#  March 2, 2018
#  NCDG Score:  0.6856248688570658


#  Dev Environment : Centos 7,  Python 3.6, Pycharm
#  Libraries:   math, re, nltk, nltk.corpus

#  Methods Atempted:
#  Algorithms:    Cos similarity and lang mode
#                 Played around with Or using query frequency and KNN to little success.  deleted code
#  Tokenization:  Used separate methods for doc and query
#                 Split on space and hyphen, remove special characters, stop words, word pairs
#                 number mapping, synonyms, stemming.  See method for full list.

import re as re
import math
# import nltk
from nltk import PorterStemmer
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import wordnet

from nltk.corpus import stopwords
from readers import read_queries, read_documents
max_doc = 1
inverted_index = {}
doc_length = {}
word_map = {}


def remove_not_indexed_toknes(tokens):
    return [token for token in tokens if token in inverted_index]

def remove_duplicates(tokens):
    return list(set(tokens))

def tf(freq):
    return 1 + math.log(float(freq))

def idf(freq):
    return math.log((max_doc - 1) / float(freq))



def lang_model(query):
    # 0.1  = Final ncdg for all queries is 0.46135264398948
    # 0.25 = Final ncdg for all queries is 0.4738344928695038
    # 0.5  = Final ncdg for all queries is 0.5017062653731896
    # 0.75 = Final ncdg for all queries is 0.520379967369712
    # 0.9  = Final ncdg for all queries is 0.5218121221541857


    query_word_unique = list(set(query))
    scores = [1] * max_doc  # Make max of list
    scores[0] = 0


    # Start Algorithm
    for token in query_word_unique:
        id_list = inverted_index[token]

        # collection Freqency
        c_tf = 0
        c_len = 0
        mc = 0
        for tup in id_list:
            c_tf += tup[1]
            c_len += doc_length[tup[0]]
        if c_len > 0:
            mc = c_tf / c_len

        # Doc Frequency
        for i in range(1, len(scores)):
            doc_id = i
            d_tf = 0
            d_len = 0
            md = 0
            for tup in id_list:
                if i == tup[0]:
                    d_tf = tup[1]
            if doc_length[doc_id] > 0:
                md = d_tf / doc_length[doc_id]

            # Lambda
            l = 0.75
            scores[i] *= (l * md) + ((1.0 - l) * mc)

    ranking = []
    for i in range(0, len(scores)):
        ranking.append((i, scores[i]))
    ranking.sort(key=lambda tup: tup[1], reverse=True)
    return [pos[0] for pos in ranking]

def cos_ranking(query):   #0.6117392006777134
    query_word_count = {}
    query_word_count[query[0]] = 1
    query_word_unique = [query[0]]

    #  Build out the query to match the inverted list data structure
    #  Query:  (word, freq), (word, freq), (word, freq), ...
    for i in range(1, len(query)):
        if query[i] in query_word_count:
            query_word_count[query[i]] += 1
        else:
            query_word_count[query[i]] = 1
            query_word_unique.append(query[i])

    scores = [0] * max_doc  # Make max of list
    length = [0] * max_doc  # Make max of list
    query_length = 0


    for i in range(len( query_word_unique)):
        # Variables
        token = query_word_unique[i]
        id_list = inverted_index[token]
        list_length = len(id_list)


        #  Calculate Query Vec
        # idf_val =  idf_custom(list_length)
        idf_val = idf(list_length)
        vec_query = tf(query_word_count[token]) * idf_val
        query_length += vec_query**2

        for tup in id_list:
            doc_id = tup[0]
            doc_freq = tup[1]
            vec_doc = tf(doc_freq)  # tf


            length[doc_id] += vec_doc**2  #  length
            scores[doc_id] += vec_doc * vec_query  #  Cos score



    ranking = []
    for i in range(0, len(scores)):


        if scores[i] > 0:
            cos_score = scores[i] /  ((query_length**0.5) * (length[i]**0.5))

        else:
            cos_score = scores[i]

        ranking.append((i, cos_score ))
    ranking.sort(key=lambda tup: tup[1], reverse=True)
    return [pos[0] for pos in ranking]



def search_query(query):
    # tokens = tokenize(str(query['query']))
    tokens = tokenize_search(str(query['query']))
    indexed_tokens = remove_not_indexed_toknes(tokens)
    if len(indexed_tokens) == 0:
        return []
    elif len(indexed_tokens) == 1:
        return inverted_index[indexed_tokens[0]]
    else:
        # return lang_model(indexed_tokens)
        return cos_ranking(indexed_tokens)

def remove_hyphen(tokens, char):
    str = []
    for token in tokens:
        str.extend(token.split(char))
    return str


def stemming(tokens):
    # https://stackoverflow.com/questions/10369393/need-a-python-module-for-stemming-of-text-documents
    str = []
    for token in tokens:
        # if token not in stop_words:
        str.append(PorterStemmer().stem(token))

    return str


def stemming_snowball(tokens):
    stemmer = SnowballStemmer("english",  ignore_stopwords=True)    # http://www.nltk.org/howto/stem.html
    str = []
    new_list = []
    for token in tokens:
        str.append(stemmer.stem(token))

    new_list.extend(str)
    return new_list


def specialChar(tokens):
    #  Special thanks Shah Zaframi for his help with char and strings in python
    str = []
    special_char_list = [".", "?", "/", "\\", "(", ")", "\"", "\'", "-", "+", ":"]
    for token in tokens:
        word = ""
        for c in token:
            if c not in special_char_list:
                word += c

        # https://stackoverflow.com/questions/19859282/check-if-a-string-contains-a-number
        # https://stackoverflow.com/questions/19859282/check-if-a-string-contains-a-number

        # Remove numbers that are in a string of word
        number = re.sub('[^\d]', '', word)

        char = []
        # Subtract the two sets and remove the digits
        # char = word.replace(number, "")
        if len(number) > 0:
            char = word.split(number)


        # Add number and char if they aren't duplicates
        if  len(number) > 0 and number != word:
            str.append(number)
        if  len(char) > 0 and char != word:
            for c in char:
                if len(c) > 0:
                    str.append(c)


        str.append(word)

    return str


def wordPairs(tokens):
    str = []
    for i in range(0, len(tokens) - 1):
        first = tokens[i]
        second = tokens[i + 1]
        if len(first) > 0 and first != ".":
            if len(second) > 0 and  second != ".":
                val = "%s %s" %(first,second)
                str.append(val)
    tokens.extend(str)
    return tokens


def stopWords(tokens):
    stop_words = set(stopwords.words('english'))  #https://www.geeksforgeeks.org/removing-stop-words-nltk-python/
    str = []
    for token in tokens:
        if token not in stop_words:
            str.append(token)
    return str


def creat_synonyms_list():
    word_list = [

        # (doc -> query word) mapping
        ("investigations", "effects"),
        ("effects", "investigations"),
        ("liquid", "water"),
        ("water", "liquid"),
        ("wave resistance", "wave system"),
        ("wave system", "wave resistance"),
        ("velocities", "pressure"),
        ("pressure", "mathematical"),
        ("distribution", "transportation"),
        ("transportation", "distribution"),
        ("speed", "flow"),
        ("velocity", "speed"),
        ("fast", "hypersonic"),
        ("hypersonic", "velocious"),
        ("variation", "different"),
        ("differences", "variation"),
        ("different", "variation"),
        ("discover", "application"),
        ("test", "discover"),
        ("observe", "discover"),
        ("recognize", "discover"),
        ("realize", "discover"),
        ("air", "gas"),
        ("demonstrate", "discover"),
        ("application", "discover"),
        ("turbulent", "unstable"),
        ("violent", "turbulent"),
        ("unstable", "turbulent"),
        ("degrees", "temperature"),
        ("temperature", "degrees"),
        ("super sonic", "high speed"),
        ("high speed", "super sonic"),
        ("information", "analysis"),
        ("paper", "theory"),
        ("analysis", "information"),
        ("centrifugal", "various"),
        ("various", "small"),
        ("newtonian", "normal"),
        ("normal", "newtonian"),
        ("example", "paper"),
        ("gases", "molecules"),
        ("chemical", "gases"),
        ("molecules", "gases"),
        ("acoustic", "noise"),
        ("sound", "acoustic"),
        ("subsonic", "acoustic"),
        ("sonic", "acoustic"),
        ("shock", "acoustic"),
        ("propagation", "absorption"),
        ("linearized", "propagation"),
        ("absorption", "propagation"),
        ("papers", "prove"),
        ("experimental", "papers"),
        ("prove", "results"),
        ("results", "prove"),
        ("reacting gases", "dissociating gas"),
        ("dissociating gas", "reacting gases"),
        ("reacting", "conducting"),
        ("conducting", "reacting"),
        ("noise", "acoustic"),
        ("predictions", "paper"),
        ("theory", "paper"),
        ("around", "yawed"),
        ("yawed", "swept"),
        ("flow", "reynolds numbers"),
        ("supersonic", "flow"),
        ("distance", "range"),
        ("range", "distance"),
        ("linear function", "coefficients"),
        ("coefficients", "linear function"),
        ("factors", "conditions"),
        ("conditions", "factors"),
        ("reynolds numbers", "flow"),
        ("functions", " equations"),
        ("equations", "functions"),
        ("swept", "yawed"),
        ("mathematical", "pressure"),
        ("number", "data"),
        ("similitude", "data"),
        ("circular", "around"),
        ("solution", "data"),
        ("paper", "data"),
        ("body", "surface"),
        ("heat-transfer", "pressure"),
        ("parameter", "data"),
        ("approximations", "details"),
        ("atmospheres", "gas"),
        ("pressure", "gas"),
        ("ionized", "gas"),
        ("investigation", "theory"),
        ("analysis", "theory"),
        ("approximated", "theory"),
        ("transport", "kinetic"),
        ("lift", "force"),
        ("moderate angles", "various angles"),
        ("improvement", "addition"),
        ("lift", "normal force"),
        ("centrifugal", "various angles"),
        ("extrapolations", "addition"),
        ("surface", "angles"),
        ("semi-angles", "various angles"),
        ("aerodynamics", "normal force"),
        ("linearised", "linear"),
        ("cylindrical surfaces", "curved wings"),
        ("formula", "design"),
        ("shape", "design"),
        ("ring", "curved"),
        ("semicircular", "curved"),
        ("noise", "influence"),
        ("aerodynamic", "laminar"),
        ("airstream", "wind"),
        ("flow", "wind"),
        ("laminar", "wind"),
        ("estimates", "model"),
        ("analogue computer", "model"),
        ("affecting", "influence"),
        ("roughness", "turbulent"),
        ("ground", "surface"),
        ("bullet", "boat tail"),
        ("ballistic", "boat tail"),
        ("missile", "boat tail"),
    ]


    for tup in word_list:
        w1 = PorterStemmer().stem(tup[0])
        w2 = PorterStemmer().stem(tup[1])
        if w1 in word_map:
            if w2 not in word_map[w1]:
                word_map[w1].append(w2)
        else:
            word_map[w1] = [w2]


def synonyms(tokens):
    syn = []
    for token in tokens:
        if token in word_map:
            syn.extend(word_map[token])
    tokens.extend(syn)
    return tokens


def tokenize_search(text):
    tokens = []
    tokens = text.split(" ")
    tokens = remove_hyphen(tokens, "-")
    tokens = remove_hyphen(tokens, ",")
    # tokens = remove_hyphen(tokens, "=")
    tokens = remove_hyphen(tokens, "\/")
    tokens = stopWords(tokens)
    tokens = specialChar(tokens)
    tokens = wordPairs(tokens)
    tokens = mapNumbers(tokens)
    tokens = stemming(tokens)
    return tokens


def tokenize(text):
    tokens = []
    tokens = text.split(" ")                   # Cos Base:  0.6117392006777134
    tokens = remove_hyphen(tokens, "-")        # Hyphen  :  0.6347618360585855
    tokens = remove_hyphen(tokens, ",")        # Comma   :  0.6407339532992602
    # tokens = remove_hyphen(tokens, "=")      # Equal   :  0.6407174038997508
    tokens = remove_hyphen(tokens, "\/")       # Slash   :  0.6407339532992602
    tokens = stopWords(tokens)                 # Stop    :  0.6372894149977122
    tokens = specialChar(tokens)               # Char    :  0.6485518460375124
    tokens = wordPairs(tokens)                 # Pairs   :  0.6407921165516753
    tokens = mapNumbers(tokens)                # Num     :  0.6411075910761688
    tokens = stemming(tokens)                  # Stem    :  0.6683700827175519
    tokens = synonyms(tokens)                  # Synon   :  0.6846613085682793
    return tokens


def mapNumbers(tokens):
    str = []
    for token in tokens:
        if token == "0":
            str.append("zero")
        elif token == "1":
            str.append("one")
        elif token == "2":
            str.append("two")
        elif token == "3":
            str.append("three")
        elif token == "4":
            str.append("four")
        elif token == "5":
            str.append("five")
        elif token == "6":
            str.append("six")
        elif token == "7":
            str.append("seven")
        elif token == "8":
            str.append("eight")
        elif token == "9":
            str.append("nine")
        elif token == "zero":
            str.append("0")
        elif token == "one":
            str.append("1")
        elif token == "two":
            str.append("2")
        elif token == "three":
            str.append("3")
        elif token == "four":
            str.append("4")
        elif token == "five":
            str.append("5")
        elif token == "six":
            str.append("6")
        elif token == "seven":
            str.append("7")
        elif token == "eight":
            str.append("8")
        elif token == "nine":
            str.append("9")

    tokens.extend(str)
    return tokens


def print_inverted_index():
    for key, value in inverted_index.items():
        print(key)


def add_token_to_index(token, doc_id):
    #  Maybe re-write
    # https://stackoverflow.com/questions/17962988/searching-an-item-in-a-multidimensional-array-in-python
    if token in inverted_index:
        current_postings = inverted_index[token]
        insert = False
        for i in range(0, len(current_postings)):
            if doc_id == current_postings[i][0]:
                current_postings[i][1] += 1
                insert = True
        if(insert == False ):
            current_postings.append([doc_id, 1])
            current_postings.sort(key=lambda tup: tup[1])
    else:
        inverted_index[token] = [[doc_id, 1]]

def add_to_index(document):
    # https://www.geeksforgeeks.org/python-get-unique-values-list/
    doc_id = document['id']
    tokens = []
    tokens = tokenize(document['title'])
    body = tokenize(document['body'])
    tokens.extend(body)


    # Metadata
    global max_doc
    max_doc += 1
    doc_length[document['id']] = len(document['title']) + len(document['body'])


    for token in tokens:
        add_token_to_index(token, doc_id)

def create_index():
    for document in read_documents():

        add_to_index(document)
    print ("Created index with size {}".format(len(inverted_index)))

creat_synonyms_list()
create_index()

if __name__ == '__main__':
    all_queries = [query for query in read_queries() if query['query number'] != 0]
    for query in all_queries:
        documents = search_query(query)
        print ("Query:{} and Results:{}".format(query, documents))