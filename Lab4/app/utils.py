import os
import re

import redis
from Levenshtein import distance
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from soundex import Soundex
import nltk

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')

soundex = Soundex()
DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_PORT = os.environ.get('DB_PORT', '6380')

index = redis.Redis(DB_HOST, port=DB_PORT, db=0, charset="utf-8", decode_responses=True)
data = redis.Redis(DB_HOST, port=DB_PORT, db=1, charset="utf-8", decode_responses=True)
soundex_index = redis.Redis(DB_HOST, port=DB_PORT, db=2, charset="utf-8", decode_responses=True)


# normilize text
def normalize(text):
    return re.sub("[^\w\s\*]|[0-9]+", "", text).lower()


# tokenize text using nltk lib
def tokenize(text):
    return word_tokenize(text)


def lemmatization(tokens):
    lemazer = WordNetLemmatizer()
    return [lemazer.lemmatize(token, pos='a') for token in tokens]


def remove_stop_word(tokens):
    stop_words = set(stopwords.words('english'))
    return list(filter(lambda x: x not in stop_words, tokens))


def preprocess(text):
    return remove_stop_word(lemmatization(tokenize(normalize(text))))


def search_wildcard(query):
    result = []
    for word in index.keys():
        # The .+ symbol is used in place of * symbol
        if re.search(rf"^{query.replace('*', '.*')}$", word):
            result.append(word)
    return result


def get_top_similar(query, limit=3):
    words = soundex_index.smembers(soundex.soundex(query))
    return sorted(words, key=lambda x: distance(query, x))[:limit]


def preprocess(text) -> list(list()):
    tokens = tokenize(normalize(text))
    spelling_corrections = []
    for token in tokens:
        if index.exists(token):
            # there is word in index, no need to correct
            spelling_corrections.append([token])
        elif '*' in token:
            # do wildcard query
            spelling_corrections.append(search_wildcard(token))
        else:
            spelling_corrections.append(get_top_similar(token))

    result = [remove_stop_word(lemmatization(words)) for words in spelling_corrections]
    return result


def search(query):
    query_words = preprocess(query)
    result = []
    for word_group in query_words:
        # OR operation for words in group
        if not word_group:
            continue
        group_result = set(index.smembers(word_group[0]))
        for word in word_group:
            group_result.union(set(index.smembers(word)))

        # AND operation for groups
        if result:
            result = result.intersection(group_result)
        else:
            result = group_result

    return [(data.get(x), x) for x in result]


def search_titles(query):
    return [(result[0].split('\n')[1], result[1]) for result in search(query)]


if __name__ == '__main__':
    print(search_titles("New Yerk moskaw MEM*ShIP"))
