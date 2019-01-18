
# coding: utf-8

# In[47]:


import re
import nltk
from nltk.corpus import stopwords
from nltk.corpus import sentiwordnet as swn
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
import pymysql


# In[48]:


stop_words = set(stopwords.words('english')) # 정지단어집합 만들기


# In[49]:


def get_score(sentense_list) :   
    positive_score = 0.0
    negative_score = 0.0
    filtered_words = []
    
    for sentence in sentense_list :
        print(sentence)
        sentence = sentence.lower()
        split_sentence = word_tokenize(sentence)
        filtered_sentence = [w for w in split_sentence if not w in stop_words] # 정지단어 필터링  
        wnl = nltk.WordNetLemmatizer()
        
        for f in filtered_sentence :
            filtered_words.append(wnl.lemmatize(str(f)))
        print(filtered_words)    
        pos_tagged = nltk.pos_tag(filtered_words)
        
        synonym_avg = []
        for pos_word in pos_tagged :
            if pos_word[1].startswith('N'): # 명사
                newtag = 'n'
            elif pos_word[1].startswith('J'): #형용사
                newtag = 'a'
            elif pos_word[1].startswith('V'): # 동사
                newtag = 'v'
            else:
                newtag = ''
            if newtag != '' : # pos가 존재하면
                synsets = list(swn.senti_synsets(pos_word[0]))
                score = 0.0
                if (len(synsets) > 0):
                    positive_score += sum([s.pos_score() for s in synsets])/len(synsets)
                    negative_score += sum([s.neg_score() for s in synsets])/len(synsets)
            positive_score/=len(pos_tagged)
            negative_score/=len(pos_tagged)
                    
    positive_score/=len(sentense_list)
    negative_score/=len(sentense_list)
    objective_score = 1 - (positive_score + negative_score)
    print(positive_score)
    print(negative_score)
    print(objective_score)

    if objective_score > positive_score or objective_score > negative_score :
        print("objective")
    else :
        if positive_score > negative_score :
            print("positive")
        else : 
            print("negative")


# In[50]:


# temp = ['I love you','This is a sample sentence, showing off the stop words filtration.','Hello World.', "It's good to see you.", 'Thanks for buying this book.']
# get_score(temp)


# In[36]:


def get_body_sent() :
    conn = pymysql.connect(host = "", user = "root", password = "", charset = "utf8")
    curs = conn.cursor()
    curs.execute("use  ;")
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


# In[52]:


get_body_sent()


# In[51]:



# f = open('C:/Users/User/Desktop/SentiWordNet_3.0.0_20130122.txt')

# positive_score = 0.0
# negative_score = 0.0
# total_score = 0.0 

# for line in f:
#     if line.startswith("#") :
#         continue
#     split_line = line.split("\t")
#     split_words = split_line[4].split(" ")
#     synonym_list = [w.split("#")[0] for w in split_words]
#     for ex in split_example :
#         if ex in synonym_list :
#             print(split_line[0]+" " +split_line[1]+" " +split_line[2]+" " +split_line[3]+" " +split_line[4]+" " +split_line[5])
#             positive_score += float(split_line[2])
#             negative_score += float(split_line[3])

