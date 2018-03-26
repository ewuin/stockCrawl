import os
import numpy as np
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import confusion_matrix
from sklearn.svm import LinearSVC
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import StratifiedKFold
from sklearn import metrics
import pickle
from sklearn.externals import joblib


import pandas as pd

datafile="final_clean_data_set_three_category.csv"
corpus_data=pd.read_csv(datafile)
#from
#https://appliedmachinelearning.wordpress.com/2017/02/12/sentiment-analysis-using-tf-idf-weighting-pythonscikit-learn/
#movie review corpus with 2000 files
#I have 1550 files gatehered with my cnbc spider

kf = StratifiedKFold(n_splits=10)

'''
use 2 x 2 matrix if two categories for labels (bull/bear)
use 3 x 3 matric if three categories (bull/bear/neutral)
'''

totalsvm = 0           # Accuracy measure on 2000 files
totalNB = 0
totalMatSvm = np.zeros((3,3));  # Confusion matrix on 2000 files
totalMatNB = np.zeros((3,3));

corpus=corpus_data['articleHTML'].values.tolist()
labels=corpus_data['labels'].values.tolist()
for i in labels:
    labels[i]=int(labels[i])
    #print type(labels[i])

print "# of labels: ",len(labels)

#y_test_arr=[]
#y_train_arr=[]
for train_index, test_index in kf.split(corpus,labels):
    #for itest in test_index:
    #    y_test_arr.append(test_index[itest])
    #for itrain in train_index:
#        y_train_arr.append(train_index[itrain])
    #print train_index
    #print test_index
    X_train = [corpus[i] for i in train_index]
    X_test = [corpus[i] for i in test_index]
    y_train=[labels[i] for i in train_index]
    y_test=[labels[i] for i in test_index]

    print "length train index: ",len(train_index)
    print "length test index: ",len(test_index)
    #y_train, y_test = labels[train_index], labels[test_index]
    '''
    print "len y_train: ",len(y_train)
    print "len X_Train: ",len(X_train)
    print "len y_test: ",len(y_test)
    print "len X_test: ",len(X_test)
    '''
    vectorizer = TfidfVectorizer(min_df=5, max_df = 0.8, sublinear_tf=True, use_idf=True,stop_words='english')
    train_corpus_tf_idf = vectorizer.fit_transform(X_train)
    test_corpus_tf_idf = vectorizer.transform(X_test)
    model1 = LinearSVC()
    model2 = MultinomialNB()
    model1.fit(train_corpus_tf_idf,y_train)
    model2.fit(train_corpus_tf_idf,y_train)
    result1 = model1.predict(test_corpus_tf_idf)
    result2 = model2.predict(test_corpus_tf_idf)
    #print result1

    totalMatSvm = totalMatSvm + confusion_matrix(y_test, result1)
    totalMatNB = totalMatNB + confusion_matrix(y_test, result2)
    totalsvm = totalsvm+sum(y_test==result1)
    totalNB = totalNB+sum(y_test==result2)

print "SVM:"
print totalMatSvm, totalsvm/1550.0
print "N Bayes:"
print totalMatNB, totalNB/1550.0

#model 1 is LinearSVC   model 2 is MultinomialNB

with open('pickledModel_SVC_three_cat.pkl','wb') as fout:        #the vectorizer must also be pickled for text analysis cases
    pickle.dump((vectorizer,model1),fout)

with open('pickledModel_MNB_three_cat.pkl','wb') as fout:
    pickle.dump((vectorizer,model2),fout)

#joblib.dump(model1,'linSVC_smaller_bull.pkl')
#joblib.dump(model2,'mnBayes_smaller_bull.pkl')
