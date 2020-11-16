import random as rd
import pandas as pd 
import numpy as np

from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from sklearn.model_selection import train_test_split as tts
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from gensim.models.word2vec import Word2Vec


class Word2VecClassification:

    def __init__(self, vector_size=10, window_size=3):
        self.vector_size = vector_size
        self.window_size = window_size
        self.tkr = RegexpTokenizer('[a-zA-Z]+')
        self.sw = stopwords.words('spanish')
        self.algorithm = RandomForestClassifier()
        self.model_w2v = None
        self.model_cls = None


    def buildWordVector(self, doc):
        vec_matrix = np.zeros(shape=(self.vector_size, len(doc)))

        for idw, word in enumerate(doc):
            if word not in self.sw:      
                try:
                    vec_matrix[:, idw] = self.model_w2v[word]
                except KeyError:
                    continue

        return np.mean(vec_matrix, axis=1)


    def get_feature_from_vec(self, tokenized_corpus):
        print('getting feature from vectores...')
        docs = []
        for doc in tokenized_corpus:
            doc =  [x for x in doc if x not in self.sw]
            vec = self.buildWordVector(doc)
            docs.append(vec)
        return docs


    def get_tokenized_corpus(self, corpus):
        return [self.tkr.tokenize(text.strip().lower()) for text in corpus]


    def fit_w2v(self, tokenized_corpus):
        print('fitting word2vec...')
        return Word2Vec(sentences=tokenized_corpus,
                            size=self.vector_size,
                            window=self.window_size,
                            min_count=2,
                            negative=20,
                            hs=0,
                            ns_exponent=.5,
                            cbow_mean=1,
                            iter=150,
                            sg=0,                            
                            )


    def fit(self, corpus, y_train):
        # train w2ec
        tokenized_corpus = self.get_tokenized_corpus(corpus)
        self.model_w2v = self.fit_w2v(tokenized_corpus)
        # train classification
        x_train = self.get_feature_from_vec(tokenized_corpus)
        self.model_cls = self.algorithm.fit(x_train, y_train)


    def predict(self, corpus):
        tokenized_corpus = self.get_tokenized_corpus(corpus)
        x = self.get_feature_from_vec(tokenized_corpus)
        return self.model_cls.predict(x)


if __name__ == '__main__':

    # data
    target = 'category'
    corpus = 'product_name'
    url = 'https://www.dropbox.com/s/1n6tcxqptjysvvf/supermercado.csv?dl=1'
    data = pd.read_csv(url, encoding='utf-8')
    train, test = tts(data, train_size = 0.85)

    # train
    model = Word2VecClassification(vector_size=10, window_size=3)
    model.fit(train[corpus], train[target])

    # predict
    predictions = model.predict(test[corpus])
    report = classification_report(test[target], predictions)
    print(report)
