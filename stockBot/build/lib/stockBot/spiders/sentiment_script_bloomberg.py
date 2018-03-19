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

    mps_remover=re.compile(r'^mps*')
    var_remover=re.compile(r'var')
    show_chapter_remover=re.compile(r'^show chapter')
    p_free  = "".join(ch for ch in article_string if ch not in exclude)           #remove punctuation, note that there is no space between the quotes

    #decoded_string=str(p_free).decode("utf-8","ignore") #typecase articlestring to avoid decoding floats
    ascii_string=p_free.encode("ascii","replace")  #done to avoid error in lemmatizer, which failed to convert something to ascii
    stop_word_free  =" ".join([i for i in ascii_string.lower().split() if i not in stop])  #remove stop words
    lemm    = " ".join(lemma.lemmatize(word) for word in stop_word_free.split())    #lemmatize words
    pre_final_words   = lemm.split()
    final_words=''   #alternatively final_words=[] if list of comma-separated words needed
    for word in pre_final_words:
        if not (re.match(mps_remover,word) or re.match(var_remover,word) or len(word)>14 ):  #for some reason only choosing the words that didnt match the regex removed the unwanted word better
            final_words=final_words+word+" "           # alternatively: final_words.append(word)

    #print final_words
    #print "------------- Next article  ---------"
    if re.match(show_chapter_remover,final_words):
        temp_words=final_words.split()
        del temp_words[0]
        del temp_words[0]
        print "removing show chapter"
        final_words=""
        for word in temp_words:
            final_words=final_words+word+" "
    return final_words

def sentiment_analysis(articleHTML):
    print "articleHTML  type: ",type(articleHTML)
    with open('C:\Users\Owner\Documents\pickledModel_MNB.pkl','rb') as fin:  #only was able to open with explicit path
        vectorizer, model1 = pickle.load(fin)
    X_new=vectorizer.transform(articleHTML)
    result1=model1.predict(X_new)
    print result1
    if result1[0]==1:
        return "Bullish"
    else:
        return "Neutral/Bearish"
