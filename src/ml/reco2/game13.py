import pandas as pd
import numpy as np
import re
from gensim.models import Word2Vec
from pymorphy2 import MorphAnalyzer


patterns = "[A-Za-z!#$%&'()*+,./:;<=>?@–[\]^_`{|}~—\"\-«»…]+"
morph = MorphAnalyzer()

print("Загрузка датасета и моделей...")
data = pd.read_pickle("./static/dataset.pkl")
model = Word2Vec.load("./static/word2vec.model")
print("Датасет и модели загружены!")


def T9(pref):
    pref = pref.lower().strip()
    data['filter'] = data.name.apply(lambda x: pref == x.strip().lower()[:len(pref)])
    return list(data[data['filter']].name)


def get_top(lemm, data):
    data['sim'] = data.lemmatize_name.apply(
        lambda x: model.wv.n_similarity(lemm, x))
    data = data.sort_values('sim', ascending=False)
    data['top'] = range(1, data.shape[0] + 1)
    return data


def get_points(book):
    p = data[data['name'] == book]['top'].to_numpy()
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


# def getAns2(json):
#     s = json["text"]
#     if s.lower() == 'ответ':
#         re('Правильный ответ -', book)
#         re
#     points = get_points(s)


def getAns3(s):
    if len(s.split()) < 5:
        kniga = game2(s, data, 'lemmatize_name')
    else:
        kniga = game2(s, data, 'lemmatize')
    return f"{kniga[0]} - {kniga[1]}"
