
# coding: utf-8

# In[13]:


import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from nltk.tokenize import sent_tokenize
import pymysql
import re


# In[14]:


analyzer = SentimentIntensityAnalyzer()


# In[21]:


def get_sentiment_scores(body):
    scores = analyzer.polarity_scores(body)
    
    if scores['compound'] >= 0.05 :
        sentiment = 'positive'
    elif scores['compound'] <= -0.05 :
        sentiment = 'negative'
    else :
        sentiment = 'objective'
        
    result = [body,scores['pos'],scores['neg'],scores['neu'],scores['compound'],sentiment]    
    return result


# In[27]:


def get_articles(keyword) :
    conn = pymysql.connect(host = "", user = "root", password = "", charset = "utf8")
    curs = conn.cursor()
    curs.execute("use ;")
    query = """select * from """ + keyword + """_articles ; """
    curs.execute(query)
    all_rows = curs.fetchall()

    body_list = [i[7] for i in all_rows]
    total_list = [get_sentiment_scores(body) for body in body_list]
    return total_list


# In[28]:


def get_replies(keyword) :
    conn = pymysql.connect(host = "", user = "root", password = "", charset = "utf8")
    curs = conn.cursor()
    curs.execute("use ;")
    query = """select * from """ + keyword + """_replies ; """
    curs.execute(query)
    all_rows = curs.fetchall()
    
    body_list = [i[4] for i in all_rows]
    total_list = [get_sentiment_scores(body) for body in body_list]
    
    return total_list


# In[29]:


def get_rereplies(keyword) :
    conn = pymysql.connect(host = "", user = "root", password = "", charset = "utf8")
    curs = conn.cursor()
    curs.execute("use ;")
    query = """select * from """ + keyword + """_rereplies ; """
    curs.execute(query)
    all_rows = curs.fetchall()
    
    body_list = [i[5] for i in all_rows]
    total_list = [get_sentiment_scores(body) for body in body_list]
    
    return total_list


# In[30]:


def save_file(total_list,file_name) :
    total_df = pd.DataFrame(total_list)
    total_df.columns = ['body','positive', 'negative', 'neutral', 'compound', 'sentiment']
    total_df.to_csv(file_name + ".csv", encoding = "euc-kr", index = False)
    print("FINISH")


# In[31]:


keyword = input("keyword? ")
keyword_type = input("articles / replies / rereplies ? ")
if keyword_type == 'articles' :
    total_list = get_articles(keyword)
elif keyword_type == 'replies' :
    total_list = get_replies(keyword)
else :
    total_list = get_rereplies(keyword)

is_saved = input("파일로 저장하시겠습니까? y/n ")
if is_saved == 'y' :
    file_name = input("file name? ")
    save_file(total_list,file_name)

