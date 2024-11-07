# -*- coding: utf-8 -*-
"""
Created on Thu Oct 31 17:46:38 2024

@author: abc
"""
from nltk.sentiment import SentimentIntensityAnalyzer
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from transformers import BertForSequenceClassification, BertTokenizer,BertModel,AdamW
import torch
from torch.utils.data import DataLoader, TensorDataset, random_split
from textblob import TextBlob



from transformers import pipeline

from sklearn.model_selection import train_test_split
from torch.utils.data import TensorDataset, DataLoader, RandomSampler, SequentialSampler


# #function to collect the data
# def data_collector():
#
#     player_complete_data = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'newsItem__multiNewsItemContainer--1euVb')))
#
#
#     for player in player_complete_data:
#         player_name_data = player.find_elements(By.CLASS_NAME, 'newsItem__newsName--1jIcY')
#         news_date_data = player.find_elements(By.CLASS_NAME, 'newsItem__newsPostDate--2BGCT')
#         actual_news_data=player.find_elements(By.CLASS_NAME, 'newsItem__newsText--3mT94')
#
#         for i in player_name_data:
#             player_name.append(i.text)
#
#         for j in news_date_data:
#             player_news_date.append(j.text)
#
#         for k in actual_news_data:
#             player_news.append(k.text)
#
# url='https://tools.thehuddle.com/nfl-fantasy-football-player-news/'
#
# driver=webdriver.Chrome()
# driver.get(url)
#
# wait = WebDriverWait(driver, 10)  # 10 seconds timeout
#
# #to be used in function
# player_name=[]
# player_news=[]
# player_news_date=[]
#
# #executing data_collector() for first page
# data_collector()
#
#
# for i in range(0,13):
#     #moving to next page
#     wait = WebDriverWait(driver, 20)  # 10 seconds timeout
#     next_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'next')))
#     next_button.click()
#
#     #calling data_collector() for next page
#     data_collector()
#
# driver.quit()
#
# df = pd.DataFrame({
#     'player_name': player_name,
#     'player_news': player_news,
#     'player_news_date': player_news_date
# })
#
#
# df.to_csv('player_news_table.csv', index=False)
#

tokenizer= BertTokenizer.from_pretrained('bert-base-uncased', do_lower_case=True)
model =BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=2)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

df=pd.read_csv('player_news_table.csv')
texts=df['player_news'].tolist()

model.eval()

tokens=tokenizer(df['player_news'].tolist(),return_tensors='pt',padding=True,truncation=True)
tokens={key:value.to(device) for key,value in tokens.items()}

batch_size=16
labels=[]

with torch.no_grad():
    for i in range(0,len(df),batch_size):
        inputs={key:value[i:i+batch_size] for key,value in tokens.items()}
        outputs=model(**inputs)
        logits=outputs.logits
        batch_predictions=torch.argmax(logits,dim=1).cpu().numpy()
        labels.extend(batch_predictions)

df['label']=labels

df.to_csv('player_news_table.csv', index=False)



#
# def clasification(text):
#     polarity=TextBlob(text).sentiment.polarity
#     return 1 if polarity>0 else 0
#
# df['label']=df['player_news'].apply(clasification)
# print(df.head())


# tokenizer = BertTokenizer.from_pretrained('bert-base-uncased', do_lower_case=True)
# tokens= tokenizer(df['player_news'].tolist(),return_tensors='pt')
# model= BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=2)
# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# model.to(device)
# label=torch.sensor(df)
# predicted_labels = []
# batch_size = 1
#
# with torch.no_grad():
#     for i in range(0, len(df), batch_size):
#         batch_inputs = {key: value[i:i + batch_size] for key, value in inputs.items()}
#         outputs = classifier(**batch_inputs)
#         logits = outputs.logits
#         batch_predictions = torch.argmax(logits, dim=1).cpu().numpy()
#         predicted_labels.extend(batch_predictions)
#
# df['predicted_label'] = predicted_labels
#
# print(df[['player_name','player_news','predicted_label']].head())