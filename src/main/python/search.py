import math
from readers import read_queries, read_documents

inverted_index = {}
max_doc_id = 0


def remove_not_indexed_toknes(tokens):
    return [token for token in tokens if token in inverted_index]

def remove_duplicates(tokens):
    return list(set(tokens))

def merge_two_postings(first, second):
    first_index = 0
    second_index = 0
    merged_list = []
    # print(first)

    while first_index < len(first) and second_index < len(second):
        if first[first_index][0] == second[second_index][0]:
            merged_list.append((first[first_index][0], first[first_index][1] + 1))
            first_index = first_index + 1
            second_index = second_index + 1
        elif first[first_index][0] < second[second_index][0]:
            merged_list.append(first[first_index])
            first_index = first_index + 1
        else:
            merged_list.append(second[second_index])
            second_index = second_index + 1

    # Append remainder
    if(first_index < len(first)):
        merged_list.extend(first[first_index:-1])
    if (second_index < len(second)):
        merged_list.extend(second[second_index:-1])

    return merged_list



def tf(freq):
    return 1 + math.log(float(freq))

def idf(freq):
    return math.log(float(len(inverted_index)) / float(freq))

# def cos_similarity(vec1, vec2):
#     return (vec1 @ vec2) / (vec1 * vec2)







def rank_postings(query):
    query_word_count = {}
    query_word_count[query[0]] = 1
    query_word_unique = [query[0]]

    for i in range(1, len(query)):
        if query[i] in query_word_count:
            query_word_count[query[i]] += 1
        else:
            query_word_count[query[i]] = 1
            query_word_unique.append(query[i])


    scores = [0] * 1401  # Make max of list

    for token in query_word_unique:
        vec_query = tf(query_word_count[token]) * idf(len(inverted_index[token]))
        id_list = inverted_index[token]
        list_length = len(id_list)
        for tup in id_list:
            doc_id = tup[0]
            doc_freq = tup[1]
            vec_doc = tf(doc_freq) * idf(list_length)              #  tf-idf

            # print("Doc ID: ", doc_id)
            # print("Vec Doc: ", vec_doc)
            # print("Vec Query: ", vec_query)


            scores[doc_id] += vec_doc * vec_query   #  Cos score

    ranking = []
    for i in range(0, len(scores)):
        ranking.append((i, scores[i]))
    ranking.sort(key=lambda tup: tup[1], reverse=True)



    return [pos[0] for pos in ranking if pos[1] > 0]






    # # todo try to normalize by doc length
    # # todo modularize the function
    #
    # # Make doc scores dic:  sum up scores
    # doc_scores = {}
    # for token in query_word_unique:
    #     id_list = inverted_index[token]
    #     for tup in id_list:
    #         doc = tf(tup[1]) * idf(len(id_list))              #  tf-idf
    #         vec = doc * query_scores[tup[0]]   #  Cos score
    #
    #         # vec = cos_similarity(doc, queery_scores[tup[0]])   #  Cos score
    #         if tup[0] not in doc_scores:
    #             doc_scores[tup[0]] = vec
    #         else:
    #             doc_scores[tup[0]] += vec
    # # Conver to array and calculate cos similarity
    # ranking = []
    # results = []
    # for key, value in doc_scores.iteritems():
    #     ranking.append((key, value))
    # ranking.sort(key=lambda tup: tup[1])
    # for tup in ranking:
    #     results.append(tup[0])
    # return results






# def rank_postings(query):
#     query_word_count = {}
#     query_word_count[query[0]] = 1
#     query_word_unique = [query[0]]
#
#     for i in range(1, len(query)):
#         if query[i] in query_word_count:
#             query_word_count[query[i]] += 1
#         else:
#             query_word_count[query[i]] = 1
#             query_word_unique.append(query[i])
#
#     # Makes array of query vec:  (word, score)
#     # token_scores = []
#     # for token in query_word_unique:
#     #     vec = tf(query_word_count[token]) * idf(len(inverted_index[token]))
#     #     token_scores.append((token, vec ))
#     query_scores = {}
#     for token in query_word_unique:
#         vec = tf(query_word_count[token]) * idf(len(inverted_index[token]))
#         query_scores[token] = vec
#     # todo try to normalize by doc length
#     # todo modularize the function
#
#     # Make doc scores dic:  sum up scores
#     doc_scores = {}
#     for token in query_word_unique:
#         id_list = inverted_index[token]
#         for tup in id_list:
#             doc = tf(tup[1]) * idf(len(id_list))              #  tf-idf
#             vec = doc * query_scores[tup[0]]   #  Cos score
#
#             # vec = cos_similarity(doc, queery_scores[tup[0]])   #  Cos score
#             if tup[0] not in doc_scores:
#                 doc_scores[tup[0]] = vec
#             else:
#                 doc_scores[tup[0]] += vec
#     # Conver to array and calculate cos similarity
#     ranking = []
#     results = []
#     for key, value in doc_scores.iteritems():
#         ranking.append((key, value))
#     ranking.sort(key=lambda tup: tup[1])
#     for tup in ranking:
#         results.append(tup[0])
#     return results

#
# def rank_postings(query):
#     query_word_count = {}
#     query_word_count[query[0]] = 1
#     query_word_unique = [query[0]]
#
#     for i in range(1, len(query)):
#         if query[i] in query_word_count:
#             query_word_count[query[i]] += 1
#         else:
#             query_word_count[query[i]] = 1
#             query_word_unique.append(query[i])
#
#     # Makes array of query vec:  (word, score)
#     query_scores = []
#     for token in query_word_unique:
#         vec = tf(query_word_count[token]) * idf(len(inverted_index[token]))
#         query_scores.append((token, vec ))
#     # query_scores = {}
#     # for token in query_word_unique:
#     #     vec = tf(query_word_count[token]) * idf(len(inverted_index[token]))
#     #     query_scores[token] = vec
#     # todo try to normalize by doc length
#     # todo modularize the function
#
#     doc_vec = {}
#     for i in range(0, len(query_word_unique)):
#         token = query_word_unique[i]
#         id_list = inverted_index[token]
#         for tup in id_list:
#             doc_id = tup[0]
#             token_freq = tup[1]
#             doc = tf(token_freq) * idf(len(id_list))              #  tf-idf
#             if doc_id not in doc_vec:
#                 doc_vec[doc_id] =
#
#
#
#
#     # Make doc scores dic:  sum up scores
#     doc_scores = {}
#     for token in query_word_unique:
#         id_list = inverted_index[token]
#         for tup in id_list:
#             doc = tf(tup[1]) * idf(len(id_list))              #  tf-idf
#             vec = cos_similarity(doc, query_scores[tup[0]])   #  Cos score
#             if tup[0] not in doc_scores:
#                 doc_scores[tup[0]] = vec
#             else:
#                 doc_scores[tup[0]] += vec
#     # Conver to array and calculate cos similarity
#     ranking = []
#     results = []
#     for key, value in doc_scores.iteritems():
#         ranking.append((key, value))
#     ranking.sort(key=lambda tup: tup[1])
#     for tup in ranking:
#         results.append(tup[0])
#     return results
#
#
#
#
#




    # scores = 0
    # for word in word_list:
    #     # Get list of DocID:  [[docID, freq], ...]
    #     doc_list = inverted_index
    #     score = 0.0
    #     for doc in doc_list:
    #         score += tf(doc[1]) * idf(len(doc_list))
    #     scores[word] = score
    # return scores



# def ranking(tokens):
#     word_list = remove_duplicates(tokens)
#     word_scores = score_words(word_list)
#
#
#
# def merge_postings(indexed_tokens):
#     query = inverted_index[indexed_tokens[0]]
#     no_dups
#
#     first_list_tup = list(zip(first_list, [1] * len(first_list)))
#
#     for each in range(1, len(indexed_tokens)):
#         second_list = inverted_index[indexed_tokens[each]]
#         second_list_tup = list(zip(second_list, [1] * len(second_list)))
#         first_list_tup = merge_two_postings(first_list_tup, second_list_tup)
#     sorted_list  = sorted(first_list_tup, key=lambda tup: tup[1], reverse=True)  # https://stackoverflow.com/questions/4183506/python-list-sort-in-descending-order
#     results = []
#     for word in sorted_list:
#         results.append(word[0])
#     # print(sorted_list)
#     return results


def search_query(query):
    tokens = tokenize(str(query['query']))
    indexed_tokens = remove_not_indexed_toknes(tokens)
    if len(indexed_tokens) == 0:
        return []
    elif len(indexed_tokens) == 1:
        return inverted_index[indexed_tokens[0]]
    else:
        return rank_postings(indexed_tokens)
        # return merge_postings(indexed_tokens)

def remove_hyphen(tokens):
    str = []
    for token in tokens:
        str.extend(token.split("-"))
    return str

def stemming(tokens):
    str = []
    stemming_list = ["s", "ies", "\'s", "s\'", "\'", "ed", "ing" ]
    for token in tokens:
        for stem in stemming_list:
            if token.endswith(stem):
                str.append(token[:-len(stem)])
    return str


def specialChar(tokens):
    str = []
    special_char_list = [".", "?", "/", "\\", "(", ")"]
    for token in tokens:
        if len(token) > 1:
            for char in special_char_list:
                if token.startswith(char):
                    token = token[1:]

                if len(token) > 1 and token.endswith(char):
                    token = token[:-1]
        str.append(token)

    return str


def stopWords(tokens):
    stop_words_list = ["a", "an", "the", "be", "been", "you", "are", "you're", "by", "to"]
    for word in stop_words_list:
        if word in tokens:
            tokens.remove(word)
    return tokens



def tokenize(text):
    tokens = []
    tokens = text.split(" ")
    tokens = stopWords(tokens)
    tokens = specialChar(tokens)
    tokens = remove_hyphen(tokens)
    tokens = mapNumbers(tokens)
    tokens.extend(stemming(tokens))


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
    # max_doc_id = max_doc_id + 1
    tokens = []
    tokens = tokenize(document['title'])
    body = tokenize(document['body'])
    # body.extend(tokenize(document['author']))

    tokens.extend(body)


    # for word in body:
    #     if word not in tokens:
    #         tokens.append(word)
    for token in tokens:
        add_token_to_index(token, document['id'])


def create_index():
    # global max_doc_id
    for document in read_documents():
        # global max_doc_id
        # max_doc_id += 1
        add_to_index(document)
    print ("Created index with size {}".format(len(inverted_index)))

# max_doc_id =0
create_index()

if __name__ == '__main__':
    all_queries = [query for query in read_queries() if query['query number'] != 0]
    for query in all_queries:
        documents = search_query(query)
        print ("Query:{} and Results:{}".format(query, documents))