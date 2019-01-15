
# coding: utf-8

# In[3]:


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


# In[17]:


body_list = []
get_article_body()

