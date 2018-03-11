import re
from bs4 import BeautifulSoup as bsObj
pat=re.compile('video|audio')
article_type = "class article-audio"
print re.search(pat,article_type)

y='<html>aa</html>'
y2=bsObj(y,"html.parser")
print y2

x=[1,2,3]
if isinstance(x,list):
    print type(x)
