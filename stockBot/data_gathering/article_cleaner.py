#this file will take the add_articles.csv files and clean the articles in the articleHTML columns
#it will then return the clean html as text and the categorizations (bullish, bearish, neutral) which will be the
#two columns (in a csv file) for the final input into the machine learning/sentiment analysis functions
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
import string

import os
import re
import pandas as pd
#from django_pandas.io import read_frame

datafolder='./articles_unclean/'
filepaths=os.listdir(datafolder)

stop    = set(stopwords.words('english'))
exclude = set(string.punctuation)
lemma   = WordNetLemmatizer()

mps_remover=re.compile(r'^mps*')
var_remover=re.compile(r'var')
show_chapter_remover=re.compile(r'^show chapter')

def clean_article(article_string):
        try:
            p_free  = "".join(ch for ch in article_string if ch not in exclude)           #remove punctuation, note that there is no space between the quotes
        except:
            print "possible empty article"
            print article_string
            return " "
        stop_word_free  =" ".join([i for i in p_free.lower().split() if i not in stop])  #remove stop words
        lemm=""
#        for word in stop_word_free.split():
#            try:
#                lemm=lemm+" "+word.decode('utf-8')
#            except:
#                print "word crash for: ", word
        lemm    = " ".join(lemma.lemmatize(word.decode('utf-8')) for word in stop_word_free.split())    #lemmatize words
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

def label_price_move(daily_change):
    if daily_change>0.0029:    # old value:0.0029
        return 1#"bull"
    if daily_change<-0.00662:  #old value -0.00462
        return -1#"bear"
    else:
        return 0#"neutral"

stock_ticker='UNH'

stock_array=[
        {'name':'facebook','symbol':'FB'},
        {'name':'alibaba', 'symbol':'BABA'},
        {'name':'amazon', 'symbol':'AMZN'},
        {'name':'microsoft', 'symbol':'MSFT'},
        {'name':'bank of america', 'symbol':'BAC'},
        {'name':'google', 'symbol':'GOOG'},
        {'name':'visa', 'symbol':'V'},
        {'name':'altaba', 'symbol':'AABA'},
        {'name':'charter communications', 'symbol':'CHTR'},
        {'name':'citigroup', 'symbol':'C'},
        {'name':'salesforce', 'symbol':'CRM'},
        {'name':'netflix', 'symbol':'NFLX'},
        {'name':'allergan', 'symbol':'AGN'},
        {'name':'time warner', 'symbol':'TWX'},
        {'name':'expedia', 'symbol':'EXPE'},
        {'name':'mastercard', 'symbol':'MA'},
        {'name':'paypal', 'symbol':'PYPL'},
        {'name':'broadcom', 'symbol':'AVGO'},
        {'name':'monsanto', 'symbol':'MON'},
        {'name':'delta airlines', 'symbol':'DAL'},
        {'name':'jp morgan', 'symbol':'JPM'},
        {'name':'t-mobile', 'symbol':'TMUS'},
        {'name':'adobe', 'symbol':'ADBE'},
        {'name':'activision blizzard', 'symbol':'ATVI'},
        {'name':'dxc technology', 'symbol':'DXC'},
        {'name':'constellation brands', 'symbol':'STZ'},
        {'name':'priceline', 'symbol':'PCLN'},
        {'name':'mgm resorts', 'symbol':'MGM'},
        {'name':'nvidia', 'symbol':'NVDA'},
        {'name':'shire', 'symbol':'SHPG'},
        {'name':'autodesk', 'symbol':'ADSK'},
        {'name':'electronic arts', 'symbol':'EA'},
        {'name':'wells fargo', 'symbol':'WFC'},
        {'name':'alexion', 'symbol':'ALXN'},
        {'name':'dell', 'symbol':'DVMT'},
        {'name':'micron', 'symbol':'MU'},
        #{'name':'servicenow', 'symbol':'NOW'}, No articles
        {'name':'zayo', 'symbol':'ZAYO'},
        {'name':'aetna', 'symbol':'AET'},
        {'name':'ally financial', 'symbol':'ALLY'},
        {'name':'anthem', 'symbol':'ANTM'},
        {'name':'celgene', 'symbol':'CELG'},
        {'name':'clovis', 'symbol':'CLVS'},
        {'name':'incyte', 'symbol':'INCY'},
        {'name':'unitedhealth', 'symbol':'UNH'},
        {'name':'parsley energy', 'symbol':'PE'}
        ]

columns=["articleHTML","labels"]
final_data_frame=pd.DataFrame(columns=columns)

for stock in stock_array:
    file_name=datafolder+stock['symbol']+'_articles_and_prices.csv'
    unclean_data=pd.read_csv(file_name)
    print  "CLEANING: ",stock
    print unclean_data['articleHTML'].count()
    unclean_data['articleHTML']=unclean_data['articleHTML'].apply(clean_article)
    unclean_data['labels']=unclean_data['daily_change'].apply(label_price_move)
    #print unclean_data.head()
    data_to_append=pd.DataFrame(columns=columns)
    data_to_append=unclean_data[['articleHTML','labels']]
    print data_to_append.head()
    final_data_frame=pd.concat([final_data_frame,data_to_append])
    print final_data_frame.head()

#new_file_name="final_clean_data_set_three_category.csv"
new_file_name="final_clean_data_set_three_category.csv"
#final_data_frame.reset_index(inplace=True)
#final_data_frame.drop(index=1474) #dropping rows to get exactly 1550 rows
#final_data_frame.reset_index(inplace=True)
#print len(final_data_frame)
final_data_frame.to_csv(new_file_name,encoding='utf-8')
