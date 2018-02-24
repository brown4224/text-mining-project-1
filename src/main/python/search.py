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



def rank_postings(query):
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
    # print(ranking)



    # return [pos[0] for pos in ranking if pos[1] > 0]
    return [pos[0] for pos in ranking]  #  Get a higher score for returning more!!!




def search_query(query):
    # tokens = tokenize(str(query['query']))
    tokens = tokenize_search(str(query['query']))
    indexed_tokens = remove_not_indexed_toknes(tokens)
    if query['query number'] == 22:
        print(">>>>>>>>>>>>>  Query: ", indexed_tokens)
    if len(indexed_tokens) == 0:
        return []
    elif len(indexed_tokens) == 1:
        return inverted_index[indexed_tokens[0]]
    else:
        return rank_postings(indexed_tokens)

def remove_hyphen(tokens, char):
    str = []
    for token in tokens:
        str.extend(token.split(char))
    return str



#     return str
def stemming(tokens):
    # https://stackoverflow.com/questions/10369393/need-a-python-module-for-stemming-of-text-documents
    # stop_words = set(stopwords.words('english'))  #https://www.geeksforgeeks.org/removing-stop-words-nltk-python/
    str = []
    for token in tokens:
        # if token not in stop_words:
        str.append(PorterStemmer().stem(token))

    return str



def stemming_snowball(tokens):
    stemmer = SnowballStemmer("english",  ignore_stopwords=True)    # http://www.nltk.org/howto/stem.html
    stop_words = set(stopwords.words('english'))  #https://www.geeksforgeeks.org/removing-stop-words-nltk-python/

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


        # if len(word) > 0:
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
                # val2 = "%s %s" %(second, first)
                str.append(val)
                # str.append(val2)
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
        ("investigations" ,  "effects"),
        ("liquid", "water"),
        ("wave resistance" , "wave system"),
        ("velocities" , "pressure"),
        ("distribution" , "transportation"),
        ("speed", "velocity"),
        ("fast", "hypersonic"),
        ("velocious", "hypersonic"),
        ("variation", "differences"),
        ("variation", "different"),
        ("discover", "test"),
        ("discover", "observe"),
        ("discover", "recognize"),
        ("discover", "realize"),
        ("gas", "air"),
        ("demonstrate", "discover"),
        ("discover", "application"),
        ("turbulent", "violent"),
        ("turbulent", "unstable"),
        ("degrees", "temperature"),
        ("super sonic", "high speed"),
        ("information", "paper"),
        ("information", "analysis"),
        ("centrifugal", "various"),
        ("circle", "various"),
        ("small", "various"),
        ("newtonian", "normal"),
        ("boat-tail", "projectile"),
        ("boat-tail", "weapon"),
        ("boat-tail", "missile"),
        ("paper", "example"),
        ("gases", "chemical"),
        ("gases", "molecules"),
        ("acoustic", "sound"),
        ("acoustic", "subsonic"),
        ("acoustic", "sonic"),
        # ("acoustic", "shock"),
        ("propagation", "linearized"),
        ("propagation", "absorption"),
        ("papers", "experimental"),
        ("papers", "prove"),
        ("prove", "results"),
        ("reacting gases", "dissociating gas"),
        ("reacting", "conducting"),
        ("acoustic", "noise"),
        ("paper", "predictions"),
        ("paper", "theory"),
        ("around", "yawed"),
        ("flow", "supersonic"),
        ("flow", "speed"),
        ("distance", "range"),
        ("linear function", "coefficients"),
        ("reynolds numbers", "flow"),
        # ("flow", "pressure"),
        # ("conditions", "coefficients"),
        # ("wave", "radiation"),
        # ("acoustic", "aerodynamic"),
        # ("prove", "ideal"),
        # ("acoustic", "harmonic"),
        # ("acoustic", "vibration"),
        # ("wave", "frequency"),
        #
        # ("various", "semi"),
        # ("hypersonic", "force"),
        # ("incidence", "degree"),
        # ("incidence", "occurrence"),



        # ("supersonic", "high speed"),
        # ("thermal", "heat"),
        # ("friction", "resistance"),
        # # ("kinetic", "particle")

        # ("friction", "motion"),
        # ("temperature", "pressure"),
        # ("approximations", "similarity"),
        # ("air", "temperature"),
        # ("kinetic", "energy"),
        # ("theoretical", "theory"),
        # ("temperature", "thermal"),
        # ("temperature", "heat")

    ]

    # word_map = {}
    for tup in word_list:
        w1 = PorterStemmer().stem(tup[0])
        w2 = PorterStemmer().stem(tup[1])
        # Forward mapping
        word_map[w1] = w2
        #  Reverse mapping
        word_map[w2] = w1



def synonyms(tokens):
    syn = []
    for token in tokens:
        if token in word_map:
            syn.append(word_map[token])
            # print (word_list[token])

    tokens.extend(syn)
    return tokens

    # syn = []
    # word_list = {
    #     "investigations" : "effects",
    #      "effects" : "investigations",
    #     "investigation": "effect",
    #     "effect": "investigation",
    #     "liquid": "water",
    #     "water" : "liquid",
    #     "wave resistance" : "wave system",
    #     "velocities" : "pressure",
    #     "pressure" : "velocities",
    #     "distribution" : "transportation",
    #      "transportation" : "distribution"
    #
    # }
    #
    # for token in tokens:
    #     if token in word_list:
    #         syn.append(word_list[token])
    #         # print (word_list[token])
    #
    # if len(syn) > 1:
    #     tokens.extend(syn)
    # return tokens

    #  From https://www.geeksforgeeks.org/get-synonymsantonyms-nltk-wordnet-python/
    # from nltk.corpus import wordnet
    # nltk.corpus.wordnet

    # synonyms = []
    # for token in tokens:
    #     for syn in wordnet.synsets(token):
    #         for l in syn.lemmas():
    #             synonyms.append(l.name())
    #
    # tokens.extend(list(set(synonyms)))
    # # for v in val:
    # #     tokens.append(v)
    # return tokens


def tokenize_search(text):
    tokens = []


    tokens = text.split(" ")
    tokens = remove_hyphen(tokens, "-")
    tokens = remove_hyphen(tokens, ",")
    tokens = remove_hyphen(tokens, "=")
    tokens = stopWords(tokens)
    # tokens = synonyms(tokens)
    tokens = specialChar(tokens)
    tokens = wordPairs(tokens)
    tokens = mapNumbers(tokens)
    tokens = stemming(tokens)
#
    return tokens

def tokenize(text):
    tokens = []
    tokens = text.split(" ")
    tokens = remove_hyphen(tokens, "-")
    tokens = remove_hyphen(tokens, ",")
    tokens = remove_hyphen(tokens, "=")
    tokens = stopWords(tokens)
    # tokens = synonyms(tokens)
    tokens = specialChar(tokens)
    tokens = wordPairs(tokens)
    tokens = mapNumbers(tokens)
    tokens = stemming(tokens)
    tokens = synonyms(tokens)


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

# https://www.geeksforgeeks.org/python-get-unique-values-list/
def add_to_index(document):
    doc_id = document['id']
    tokens = []
    tokens = tokenize(document['title'])
    body = tokenize(document['body'])
    # author = tokenize(document['author'])

    tokens.extend(body)
    # tokens.extend(author)

    # Metadata
    global max_doc
    max_doc += 1


    for token in tokens:
        add_token_to_index(token, doc_id)



def create_index():
    for document in read_documents():

        add_to_index(document)
    print ("Created index with size {}".format(len(inverted_index)))
    # print_inverted_index()

creat_synonyms_list()
create_index()

if __name__ == '__main__':
    all_queries = [query for query in read_queries() if query['query number'] != 0]
    for query in all_queries:
        documents = search_query(query)
        print ("Query:{} and Results:{}".format(query, documents))