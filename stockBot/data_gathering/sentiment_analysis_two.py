import os
import numpy as np
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import SGDClassifier
import pandas as pd

datafile="final_clean_data_set.csv"
corpus_data=pd.read_csv(datafile)
corpus=corpus_data['articleHTML'].values.tolist()
labels=corpus_data['labels'].values.tolist()
for i in labels:
    labels[i]=int(labels[i])

count_vect = CountVectorizer()

train_set=corpus[0:1000]
train_labels=labels[0:1000]
test_set=corpus[1001:1549]
test_labels=labels[1001:1549]

X_train_counts = count_vect.fit_transform(train_set) ###
print X_train_counts.shape

tfidf_transformer = TfidfTransformer()
X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
print X_train_tfidf.shape

clf = MultinomialNB().fit(X_train_tfidf, train_labels) ####
clf2=SGDClassifier(loss='hinge', penalty='l2',alpha=1e-3, random_state=42,max_iter=5, tol=None).fit(X_train_tfidf, train_labels)
X_new_counts = count_vect.transform(test_set) ####
X_new_tfidf = tfidf_transformer.transform(X_new_counts)

predicted = clf.predict(X_new_tfidf)
predicted2=clf2.predict(X_new_tfidf)
print "first model: "
print np.mean(predicted == test_labels)
print "second model: "
print np.mean(predicted2 == test_labels)

from sklearn import metrics
print(metrics.classification_report(test_labels, predicted, target_names=["bad","neutral","good"]))
print(metrics.classification_report(test_labels, predicted2, target_names=["bad","neutral","good"]))
#print(metrics.classification_report(test_labels, predicted2, target_names=str(test_labels)))
