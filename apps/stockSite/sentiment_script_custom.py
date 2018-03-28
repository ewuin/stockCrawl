#this file will take scraped articles html and clean them. it will then return the clean html as text to be saved to the database
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
import string
import re
import pandas as pd
import pickle

#sys.path.append(dirname(os.getcwd())+'\\'+'pickledModel_MNB.pkl')
#print sys.path


def clean_article(article_string):
    stop    = set(stopwords.words('english'))
    exclude = set(string.punctuation)
    lemma   = WordNetLemmatizer()

    p_free  = "".join(ch for ch in article_string if ch not in exclude)           #remove punctuation, note that there is no space between the quotes

    #decoded_string=str(p_free).decode("utf-8","ignore") #typecase articlestring to avoid decoding floats
    ascii_string=p_free.encode("ascii","replace")  #done to avoid error in lemmatizer, which failed to convert something to ascii
    stop_word_free  =" ".join([i for i in ascii_string.lower().split() if i not in stop])  #remove stop words
    lemm    = " ".join(lemma.lemmatize(word) for word in stop_word_free.split())    #lemmatize words
    print lemm
    return lemm

def sentiment_analysis(articleHTML):
    print "articleHTML  type: ",type(articleHTML)
    with open('C:\Users\Owner\Documents\pickledModel_MNB_three_cat.pkl','rb') as fin:  #only was able to open with explicit path
        vectorizer, model1 = pickle.load(fin)
    X_new=vectorizer.transform(articleHTML)
    result1=model1.predict(X_new)
    print result1
    if result1[0]==1:
        return "Bullish"
    if result1[0]==-1:
        return "Bearish"
    else:
        return "Neutral"
