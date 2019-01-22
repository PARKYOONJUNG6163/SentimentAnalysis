
# coding: utf-8

# In[52]:


import re
import nltk
from nltk.corpus import stopwords
from nltk.corpus import sentiwordnet as swn
from nltk.tokenize import sent_tokenize
from nltk.tokenize import RegexpTokenizer
import pymysql


# In[53]:


stop_words = set(stopwords.words('english')) # 정지단어집합 만들기


# In[57]:


def get_score(sentense_list) :   
    for sentence in sentense_list :
        filtered_words = []
        sentence = sentence.lower() # 소문자로
        retokenize = RegexpTokenizer("[\w]+") 
        split_sentence = retokenize.tokenize(sentence) # 토큰 단위로 자르기
        filtered_sentence = [w for w in split_sentence if not w in stop_words] # 정지단어 필터링  
        wnl = nltk.WordNetLemmatizer() # 원형 복원
        
        for f in filtered_sentence :
            filtered_words.append(wnl.lemmatize(str(f))) # 원형 복원   
        pos_tagged = nltk.pos_tag(filtered_words)
        
        positive_score = 0.0
        negative_score = 0.0
        synonym_avg = []
        
        for pos_word in pos_tagged :
            if pos_word[1].startswith('N'): # 명사
                newtag = 'n'
            elif pos_word[1].startswith('J'): #형용사
                newtag = 'a'
            elif pos_word[1].startswith('V'): # 동사
                newtag = 'v'
            elif pos_word[1].startswith('R'):
                newtag = 'r'
            else:
                newtag = ''
            if newtag != '' : # pos가 존재하면
                synsets = list(swn.senti_synsets(pos_word[0],newtag))
                if (len(synsets) > 0):
                    positive_score += sum([s.pos_score() for s in synsets])/len(synsets)
                    negative_score += sum([s.neg_score() for s in synsets])/len(synsets)
                    
        if (len(pos_tagged) > 0):            
            positive_score/=len(pos_tagged)
            negative_score/=len(pos_tagged)
  
            if positive_score > negative_score :
                print("positive")
            elif  positive_score < negative_score :
                print("negative")
            else :
                print("objective")
        else :
            print("objective")


# In[58]:


def get_body_sent() :
    conn = pymysql.connect(host = "", user = "root", password = "", charset = "utf8")
    curs = conn.cursor()
    curs.execute("use ;")
    query = """select * from ; """
    curs.execute(query)
    all_rows = curs.fetchall()
    body_list = []
    
    for i in all_rows:
        temp = re.sub('<.+?>', '', i[7], 0).strip() # 태그 제거
        temp = re.sub(r'\\x..', '', temp) #\xa0 같은 거 제거
        body_list.append(temp)
    
    for body in body_list :
        body = re.sub(r'\\x..', '', body)
        sentence_list = sent_tokenize(body)
        print(sentence_list)
        get_score(sentence_list)


# In[59]:


get_body_sent()

