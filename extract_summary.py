"""
提取摘要的步骤为
1. 利用标点符号分句、对每一句话分词
2. 将分词后的矩阵用sklearn中的tfidf函数求解单词的tfidf矩阵
3. 求得的tfidf矩阵后，求解余弦相似阵
4. 求得的余弦相似阵，即可调用textrank算法，求解句子的得分向量
5. 得到得分向量，排序取前几名的句子作为文章的摘要。
"""

import numpy as np
import pandas as pd
import jieba
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.metrics.pairwise import cosine_similarity
from wordcloud import WordCloud, ImageColorGenerator
from matplotlib import pyplot as plt
import json

stopwords = [line for line in open('stopwords.txt')]


def get_sentences():
    parrern = r'。|！|？|……'
    sentences = []
    with open('人民网.json', 'r', encoding='utf-8') as f:
        doc = json.load(f)
        doc = doc['document']
    for s in re.split(parrern, doc):
        sentences.append(s.strip())
    return sentences


def tokenizel(sentences, stopwords):
    cut_words = []
    for line in sentences:
        seg_list = jieba.cut(line, cut_all=False)
        cut_words.append(" ".join([i for i in seg_list if i not in stopwords]))
    return cut_words


def tfidf_keyword(cut_words):
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(cut_words)
    transformer = TfidfTransformer()
    tfidf = transformer.fit_transform(X)
    return tfidf.toarray(), len(vectorizer.get_feature_names())


def sim_mat(tf_idf, sentences, leng):
    sim_mat = np.zeros([len(sentences), len(sentences)])
    for i in range(len(sentences)):
        for j in range(len(sentences)):
            if i != j:
                sim_mat[i][j] = cosine_similarity(tf_idf[i].reshape(1, leng), tf_idf[j].reshape(1, leng))[0, 0]
    return sim_mat


def text_rank(sim, max_iter, min_diff):  # 相似度矩阵，最大迭代次数，最小误差（判断结束条件）
    d = 0.85
    D = len(sim)
    sim_sum = [sum(i) for i in sim]
    vertex = [1.0] * D
    for _ in range(max_iter):
        m = []
        max_diff = 0
        for i in range(D):
            m.append(1 - d)
            for j in range(D):
                if j == i or sim_sum[j] == 0:
                    continue
                m[-1] += (d * sim[j][i] / sim_sum[j] * vertex[j])
            if abs(m[-1] - vertex[i]) > max_diff:
                max_diff = abs(m[-1] - vertex[i])
        vertex = m
        if max_diff <= min_diff:
            break
    top = list(enumerate(vertex))
    top = sorted(top, key=lambda x: x[1], reverse=True)
    return top


def select_top(top, sentences, num):
    out = []
    flag = 0
    for i, _ in top:
        out.append(sentences[i])
        flag += 1
        if flag >= num:
            break
    return out


def display(stopwords):
    with open('人民网.json', 'r', encoding='utf-8') as f:
        doc = json.load(f)
        doc = doc['document']
    wc = WordCloud(font_path='new.ttf', background_color='white',
                   width=1000, height=800,
                   stopwords=stopwords).generate(" ".join(jieba.cut(doc, cut_all=False)))
    wc.to_file('ss.png')
    plt.imshow(wc)
    plt.axis('off')
    plt.show()


sentences = get_sentences()
cut_words = tokenizel(sentences, stopwords)
vector_TF, leng = tfidf_keyword(cut_words)
sim = sim_mat(vector_TF, sentences, leng)
top = text_rank(sim, 200, 0.001)
print(select_top(top, sentences, 3))
display(stopwords)

