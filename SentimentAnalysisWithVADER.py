
# coding: utf-8

# In[6]:


import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from nltk.tokenize import sent_tokenize
import pymysql
import re


# In[7]:


analyzer = SentimentIntensityAnalyzer()


# In[8]:


def get_sentiment_scores(sentence):
    scores = analyzer.polarity_scores(sentence)
    
    if scores['compound'] >= 0.05 :
        sentiment = 'positive'
    elif scores['compound'] <= -0.05 :
        sentiment = 'negative'
    else :
        sentiment = 'objective'
        
    result = [sentence,scores['pos'],scores['neg'],scores['neu'],scores['compound'],sentiment]    
    return result


# In[14]:


def get_articles(keyword) :
    conn = pymysql.connect(host = "147.43.122.131", user = "root", password = "1234", charset = "utf8")
    curs = conn.cursor()
    curs.execute("use yahoo_news ;")
    query = """select * from """ + keyword + """_articles ; """
    curs.execute(query)
    all_rows = curs.fetchall()
    body_list = []
    for i in all_rows:
        temp = re.sub('<.*?>', '', i[7]).strip() # 태그 제거
        temp = re.sub(r'\\x..', '', temp) #\xa0 같은 거 제거
        temp = re.sub('\"', '', temp) #\xa0 같은 거 제거
        body_list.append(temp)
   
    total_list = []
    for body in body_list :
        body = re.sub(r'\\x..', '', body)
        sentence_list = sent_tokenize(body)
        for sentence in sentence_list :
            sentence = re.sub(r'\\x..', '', sentence)
            print(sentence)
            total_list.append(get_sentiment_scores(sentence))
    
    return total_list


# In[10]:


def get_replies(keyword) :
    conn = pymysql.connect(host = "147.43.122.131", user = "root", password = "1234", charset = "utf8")
    curs = conn.cursor()
    curs.execute("use yahoo_news ;")
    query = """select * from """ + keyword + """_replies ; """
    curs.execute(query)
    all_rows = curs.fetchall()
    body_list = []
    
    for i in all_rows:
        temp = re.sub('<.+?>', '', i[4], 0).strip() # 태그 제거
        temp = re.sub(r'\\x..', '', temp) #\xa0 같은 거 제거
        body_list.append(temp)
        
    total_list = []
    for body in body_list :
        body = re.sub(r'\\x..', '', body)
        sentence_list = sent_tokenize(body)
        for sentence in sentence_list :
            total_list.append(get_sentiment_scores(sentence))
    
    return total_list


# In[11]:


def get_rereplies(keyword) :
    conn = pymysql.connect(host = "147.43.122.131", user = "root", password = "1234", charset = "utf8")
    curs = conn.cursor()
    curs.execute("use yahoo_news ;")
    query = """select * from """ + keyword + """_rereplies ; """
    curs.execute(query)
    all_rows = curs.fetchall()
    body_list = []
    
    for i in all_rows:
        temp = re.sub('<.+?>', '', i[5], 0).strip() # 태그 제거
        temp = re.sub(r'\\x..', '', temp) #\xa0 같은 거 제거
        body_list.append(temp)
        
    total_list = []
    for body in body_list :
        body = re.sub(r'\\x..', '', body)
        sentence_list = sent_tokenize(body)
        for sentence in sentence_list :
            total_list.append(get_sentiment_scores(sentence))
    
    return total_list


# In[12]:


def save_file(total_list,file_name) :
    total_df = pd.DataFrame(total_list)
    total_df.columns = ['sentence','positive', 'negative', 'neutral', 'compound', 'sentiment']
    total_df.to_csv(file_name + ".csv", encoding = "euc-kr", index = False)
    print("FINISH")


# In[16]:


keyword = input("keyword? ")
keyword_type = input("articles / replies / rereplies ? ")
if keyword_type == 'articles' :
    total_list = get_articles(keyword)
elif keyword_type == 'replies' :
    total_list = get_replies(keyword)
else :
    total_list = get_rereplies(keyword)
print(total_list)
is_saved = input("파일로 저장하시겠습니까? y/n ")
if is_saved == 'y' :
    file_name = input("file name? ")
    save_file(total_list,file_name)

