import pandas as pd
import numpy as np
from random import choice
import re
from gensim.models import Word2Vec
from pymorphy2 import MorphAnalyzer


patterns = "[A-Za-z!#$%&'()*+,./:;<=>?@–[\]^_`{|}~—\"\-«»…]+"
morph = MorphAnalyzer()

print("Загрузка датасета и моделей...")
data = pd.read_pickle("./static/dataset.pkl")
model = Word2Vec.load("./static/word2vec.model")
book = None
top = None
print("Датасет и модели загружены!")


def T9(pref):
    pref = re.sub(patterns, '', pref).strip().lower()
    if pref == '': return None
    data['filter'] = data.name.apply(lambda x: pref == re.sub(patterns, '', x).strip().lower()[:len(pref)])
    return list(data[data['filter']].name)

def choi():
    global book, top
    book = choice(data['name'].tolist())
    lemm = data[data['name'] == book].lemmatize_name.to_numpy()[0].tolist()
    top = get_top(lemm, data)
    return book


def get_top(lemm, df):
    df['sim'] = df.lemmatize_name.apply(
        lambda x: model.wv.n_similarity(lemm, x))
    df = df.sort_values('sim', ascending=False)
    df['top'] = range(1, df.shape[0] + 1)
    return df


def get_points(book):
    p = top[top['name'] == book]['top'].to_numpy()
    if p.size == 0:
        return None
    return p[0]


def lemmatize(text):
    text = re.sub(patterns, ' ', text).strip()
    tokens = np.array([])
    for token in text.split():
        if token:
            token = morph.normal_forms(token)[0]
            tokens = np.append(tokens, token)
    return tokens


def game2(text, data, stolb):
    lemm = lemmatize(text)
    data['sim'] = data[stolb].apply(
        lambda x: model.wv.n_similarity(lemm, x[:30]))
    data = data.sort_values('sim', ascending=False)
    return data[['name', 'author', 'description']].head(1).to_numpy()[0]


def getAns2(json):
    s = json["text"]
    if s.lower() == 'ответ':
        return [book, 1, 1]
    points = get_points(s)
    if points == None:
        return ['Мы не знаем такой книги', -1, -1]
    else:
        return [s, int(points), 1 - (int(points) / int(top.shape[0]))]


def getAns3(s):
    if len(s.split()) < 5:
        kniga = game2(s, data, 'lemmatize_name')
    else:
        kniga = game2(s, data, 'lemmatize')
    return (f"{kniga[0]} - {kniga[1]}", kniga[2])
    # return f"Аниме екгшмге - Аниме шиемвшРофл ХАХАХАХАХАХХААХАХА"
