
# coding: utf-8

# In[2]:


import re
from nltk.corpus import stopwords

import pymysql


# In[16]:


def get_article_body() :
    conn = pymysql.connect(host = "", user = "root", password = "", charset = "utf8")
    curs = conn.cursor()
    curs.execute("use yahoo_news ;")
    query = """select * from galaxys; """
    curs.execute(query)
    all_rows = curs.fetchall()
    body_list = []
    for i in all_rows:
        temp = re.sub('<.+?>', '', i[7], 0).strip() # 태그 제거
        temp = re.sub(r'\\x..', '', temp) #\xa0 같은 거 제거
        body_list.append(temp)
    print(body_list)


# In[9]:


dict_list = []
words_list = []

f = open('SentiWordNet_3.0.0_20130122.txt')
for line in f:
    if line.startswith("#") :
        continue
    split_line = line.split("\t")
    words = split_line[4]
    synonym_list = [words.split("#")[0] for w in words] #동의어
    for w in words : # 단어들만 모아둔 사전 만들기
        words_list.append(w)
    dict_list.append([split_line[0],split_line[1],split_line[2],split_line[3],synonym_list,split_line[5]]) # 모든 정보 포함하는 사전 만들기

