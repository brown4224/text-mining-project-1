from readers import read_queries, read_documents

inverted_index = {}


def remove_not_indexed_toknes(tokens):
    return [token for token in tokens if token in inverted_index]




def merge_two_postings(first, second):
    first_index = 0
    second_index = 0
    merged_list = []

    while first_index < len(first) and second_index < len(second):
        if first[first_index] == second[second_index]:
            merged_list.append(first[first_index])
            first_index = first_index + 1
            second_index = second_index + 1
        elif first[first_index] < second[second_index]:
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


def merge_postings(indexed_tokens):
    first_list = inverted_index[indexed_tokens[0]]
    second_list = []
    for each in range(1, len(indexed_tokens)):
        second_list = inverted_index[indexed_tokens[each]]
        first_list = merge_two_postings(first_list, second_list)
    return first_list


def search_query(query):
    tokens = tokenize(str(query['query']))
    indexed_tokens = remove_not_indexed_toknes(tokens)
    if len(indexed_tokens) == 0:
        return []
    elif len(indexed_tokens) == 1:
        return inverted_index[indexed_tokens[0]]
    else:
        return merge_postings(indexed_tokens)

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
    # a = "text"
    # a.startswith()
    for token in tokens:
        if len(token) > 1:
            for char in special_char_list:
                if token.startswith(char):
                    token = token[1:]

                if len(token) > 1 and token.endswith(char):
                    token = token[:-1]
        str.append(token)

    return str

def tokenize(text):
    tokens = []
    tokens = text.split(" ")
    tokens = specialChar(tokens)
    tokens.extend(stemming(tokens))
    tokens = remove_hyphen(tokens)


    return tokens




def add_token_to_index(token, doc_id):
    if token in inverted_index:
        current_postings = inverted_index[token]
        current_postings.append(doc_id)
        inverted_index[token] = current_postings
    else:
        inverted_index[token] = [doc_id]

# https://www.geeksforgeeks.org/python-get-unique-values-list/
def add_to_index(document):
    tokens = []
    tokens = tokenize(document['title'])
    body = (tokenize(document['body']))

    for word in body:
        if word not in tokens:
            tokens.append(word)
    # tokens = merge_two_postings(title, body)
    for token in tokens:
        add_token_to_index(token, document['id'])


def create_index():
    for document in read_documents():
        add_to_index(document)
    print ("Created index with size {}".format(len(inverted_index)))


create_index()

if __name__ == '__main__':
    all_queries = [query for query in read_queries() if query['query number'] != 0]
    for query in all_queries:
        documents = search_query(query)
        print ("Query:{} and Results:{}".format(query, documents))



