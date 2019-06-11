import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json, re, jieba


def split_sentence_word(article, stopwords):
    pattern = ' |？|！|。|，'
    sentences = re.split(pattern, article)

    words_array = []
    for sentence in sentences:
        words = jieba.cut(sentence, cut_all=False)
        words_array.append(" ".join([word for word in words if word not in stopwords]))

    print(words_array)
    return words_array, sentences


def calcu_tfidf(words_array):
    vectorizer = CountVectorizer()
    tmp = vectorizer.fit_transform(words_array)
    transform = TfidfTransformer()
    tfidf = transform.fit_transform(tmp)

    return tfidf.toarray(), len(vectorizer.get_feature_names())


def sim_matrix(tfidf, sentences, length):
    sim_mat = np.zeros([len(sentences), len(sentences)])

    for i in range(len(sentences)):
        for j in range(len(sentences)):
            if i != j:
                sim_mat[i][j] = cosine_similarity(tfidf[i].reshape(1, length), tfidf[j].reshape(1, length))[0, 0]

    return sim_mat


def text_rank(sim_matrix, max_iter, min_diff):  # 相似度矩阵，最大迭代次数，最小误差（判断结束条件）
    d = 0.85
    D = len(sim_matrix)
    sim_sum = [sum(i) for i in sim_matrix]
    vertex = [1.0] * D
    for _ in range(max_iter):
        m = []
        max_diff = 0
        for i in range(D):
            m.append(1 - d)
            for j in range(D):
                if j == i or sim_sum[j] == 0:
                    continue
                m[-1] += (d * sim_matrix[j][i] / sim_sum[j] * vertex[j])
            if abs(m[-1] - vertex[i]) > max_diff:
                max_diff = abs(m[-1] - vertex[i])
        vertex = m
        if max_diff <= min_diff:
            break
    top = list(enumerate(vertex))
    top = sorted(top, key=lambda x: x[1], reverse=True)
    return top


if __name__ == "__main__":
    title_time_artcile = pd.read_csv("extract_data.csv")
    with open("stopwords.txt", 'r', encoding='utf-8') as f:
        stopwords = f.readlines()
    stopwords = [i.strip('') for i in stopwords]
    words, split_sentences = split_sentence_word(title_time_artcile.loc[0]['content'], stopwords)
    tfidf_array, leng = calcu_tfidf(words)
    print(tfidf_array,leng)
    sim_matrix = sim_matrix(tfidf_array, split_sentences, leng)
    top_n = text_rank(sim_matrix, 200, 0.01)
    for i in top_n[:5]:
        print(split_sentences[i[0]])

