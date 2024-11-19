# -*- coding: utf-8 -*-
"""
Created on Thu Oct 31 17:46:38 2024

@author: abc
"""
import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from transformers import pipeline

# DistilBERT, trained on the Stanford Sentiment Treebank dataset
# which contains movie reviews labeled as either positive or negative

df=pd.read_csv('player_news_table.csv')

df['player_news']=df['player_news'].fillna("").astype(str).str.replace(r"SOURCE:.*", "",regex=True).str.strip()
print("here")
analyzer=pipeline("sentiment-analysis",model="distilbert-base-uncased-finetuned-sst-2-english",truncation=True)
sent_labels=[]
processed_indexes = []

for i in range(0,len(df),16):
    batch= df['player_news'][i:i+16]
    print("here 1")
    batch_texts=[str(text) for text in batch if isinstance(text,str) and text.strip()]
    if not batch_texts:
        continue
    print("here 2")
    batch_results=analyzer(batch_texts)
    for index,result in zip(batch.index,batch_results):
        label=1 if result['label']=='POSITIVE' else 0
        sent_labels.append(label)
        print("here 3")
        processed_indexes.append(index)

df.loc[processed_indexes,'label']=sent_labels
print("here 4")
df.to_csv('player_news_table_with_labels.csv',index=False)

print(df['label'].value_counts())

