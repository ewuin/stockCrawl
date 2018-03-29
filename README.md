# stockCrawl

see screen-caps at: http://18.188.177.97/

This is a website developed with django. The main purpose is to allow users to crawl financial news websites for news about
an individual security. When a user submits a search, the views.py file calls scrapy spiders to search the external sites,
which also gather the contents of the news articles, and then perform sentiment analysis on each article, labeling each article as
bullish, bearish, or neutral. The server returns the information to the client which sees the results in a table.

The gathering of data for the sentiment analysis (multinomial naive-bayes machine learning algorithm) was done using spiders that
crawled for articles dating back to July 2017 for about 40 stocks. Daily price changes for these stocks were also compiled
for the same period. The maching learning algorithm then analyzed the relationship between the words in the articles and the change
in the security's value for that day. This result was pickled and serves as the trained set against which the user requested articles
are compared to in order to categorize those articles.

The scrapy spiders are found in the subdirectory "stockBot." This subdirectory also contains the folder data_gathering which has the files
I used to develop the machine learning model.

The website is in the conventional "apps" subdirectory.

Due to the fact that this site needs a scrapyd server alongside the django server, I am still in the process of deploying a live
public version on amazon aws.
You can however see screen captures of the site running from my local machine at the IP address: http://18.188.177.97/

The packages necessary to run are:
django,
django-autocomplete-light,
requests,
uuid,
scrapy,
scrapyd (for scrapyd_api),
python-scrapyd-api,

scrapy_djangoitem,
bs4,
scrapyd-client,
nltk,
(after installing nltk, enter python shell,
>>import nltk
>>nltk.download('stopwords')
>>nltk.download('wordnet')
),
pandas,
numpy,
selenium,
scipy(if errors, use << pip --no-cache-dir install scipy >> to avoid memory error),
scikit-learn,
