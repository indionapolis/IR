import os
import re
from time import sleep

import nltk
import redis
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from soundex import Soundex

soundex = Soundex()

DATA_DIR = 'data'

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')

DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_PORT = os.environ.get('DB_PORT', '6380')

index = redis.Redis(DB_HOST, port=DB_PORT, db=0)
data = redis.Redis(DB_HOST, port=DB_PORT, db=1)
soundex_index = redis.Redis(DB_HOST, port=DB_PORT, db=2)


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


def get_collection():
    counter = 0

    for i in range(22):
        with open('{}/reut2-{:03}.sgm'.format(DATA_DIR, i), 'rb') as f:
            text = f.read().decode(errors='replace')

            soup = BeautifulSoup(text, 'html.parser')

            for txt in soup.findAll('text'):
                if counter > 10000:
                    sleep(5)
                yield txt.text
                counter += 1


def make_index(raw_collection):
    for text_id, text in enumerate(raw_collection):
        text_id = str(text_id)
        data.set(text_id, text)
        words = preprocess(text)

        for word in words:
            index.sadd(word, text_id)
            soundex_index.sadd(soundex.soundex(word), word)


if __name__ == '__main__':
    index.flushdb()
    data.flushdb()

    collection = get_collection()
    print('start to create index')
    make_index(collection)
    # print(len(data.keys()))
    # print(index.smembers('also'))
    # print(data.get('5').decode('utf-8').split('\n'))
