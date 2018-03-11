import os
import numpy as np
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import confusion_matrix
from sklearn.svm import LinearSVC
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import StratifiedKFold

import pandas as pd

datafile="final_clean_data_set.csv"
corpus_data=pd.read_csv(datafile)
#from
#https://appliedmachinelearning.wordpress.com/2017/02/12/sentiment-analysis-using-tf-idf-weighting-pythonscikit-learn/
#movie review corpus with 2000 files
#I have 1550 files gatehered with my cnbc spider

kf = StratifiedKFold(n_splits=10)

totalsvm = 0           # Accuracy measure on 2000 files
totalNB = 0
totalMatSvm = np.zeros((2,2));  # Confusion matrix on 2000 files
totalMatNB = np.zeros((2,2));

corpus=corpus_data['articleHTML'].values.tolist()
labels=corpus_data['labels'].values.tolist()
for i in labels:
    labels[i]=int(labels[i])
    #print type(labels[i])

print type(labels)

for train_index, test_index in kf.split(corpus,labels):
    X_train = [corpus[i] for i in train_index]
    X_test = [corpus[i] for i in test_index]
    print len(train_index)
    print len(test_index)
    #y_train, y_test = labels[train_index], labels[test_index]
    y_train=[]
    y_test=[]
    for ix in test_index:
        if ix==len(test_index):
            break
        y_test.append(labels[test_index[ix]])
    for ix in train_index:
        if ix==len(train_index):
            break
        y_train.append(labels[train_index[ix]])

    vectorizer = TfidfVectorizer(min_df=5, max_df = 0.8, sublinear_tf=True, use_idf=True,stop_words='english')
    train_corpus_tf_idf = vectorizer.fit_transform(X_train)
    test_corpus_tf_idf = vectorizer.transform(X_test)
    model1 = LinearSVC()
    model2 = MultinomialNB()
    model1.fit(train_corpus_tf_idf,y_train)
    model2.fit(train_corpus_tf_idf,y_train)
    result1 = model1.predict(test_corpus_tf_idf)
    result2 = model2.predict(test_corpus_tf_idf)
    totalMatSvm = totalMatSvm + confusion_matrix(y_test, result1)
    totalMatNB = totalMatNB + confusion_matrix(y_test, result2)
    totalsvm = totalsvm+sum(y_test==result1)
    totalNB = totalNB+sum(y_test==result2)

print totalMatSvm, totalsvm/1550.0, totalMatNB, totalNB/1550.0
