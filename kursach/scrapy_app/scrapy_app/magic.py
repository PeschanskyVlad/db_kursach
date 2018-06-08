#!python
# -*- coding: utf-8 -*-

import sys

import numpy as np
import pickle
import sqlite3
import re

from Stemmer import Stemmer

# from sklearn.feature_extraction.text import CountVectorizer
# from sklearn.feature_extraction.text import HashingVectorizer
# from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import SGDClassifier
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score


def magic_load_dictionary():
    dbname = 'D:/Labs/Petrashenko/2semestr/kursach/kursach/kursach/data/rss-all.sqlite'
    data = {'text': [], 'tag': []}
    conn = sqlite3.connect(dbname)
    try:
        c = conn.cursor()
        for row in c.execute('SELECT * FROM data'):
            data['text'] += [row[1]]
            data['tag'] += [row[2]]
    finally:
        conn.close()
    return data


def magic_split_dictionary(data):
    # изи, прост размер масива
    sz = len(data['text'])
    # эт фигня делает просто масив из интов по порядкам например при 3196 выход будет таким:
    # [0    1    2 ... 3193 3194 3195]
    indices = np.arange(sz)

    # Эта фигня прост рандомно тусует тот масив, тип так:
    # [2273  470 2186 ...  306  249  179]
    np.random.shuffle(indices)

    # Все тексты по очереди(новой)
    X = [data['text'][i] for i in indices]
    # Все теги отдельно по очереди(новой)
    Y = [data['tag'][i] for i in indices]
    # Порядок текстов и тегов совподают (очевидно лол)
    return {
        'train': {'x': X, 'y': Y}
    }


class Magic(object):
    text_clf = 1

    def __init__(self):
        data = magic_load_dictionary()
        D = magic_split_dictionary(data)

        self.text_clf = Pipeline([
            ('tfidf', TfidfVectorizer()),
            ('clf', SGDClassifier(loss='hinge')),
        ])
        self.text_clf.fit(D['train']['x'], D['train']['y'])

    def behold_category_name(self,text):
        list = []
        list.append(text)
        predicted = self.text_clf.predict(list)
        return predicted[0]



