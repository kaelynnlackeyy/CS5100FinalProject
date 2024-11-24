# -*- coding: utf-8 -*-
"""
Created on Thu Oct 31 17:46:38 2024

@author: abc
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

#function to collect the data
def data_collector():
    
    player_complete_data = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'newsItem__multiNewsItemContainer--1euVb')))

    

    for player in player_complete_data:
        player_name_data = player.find_elements(By.CLASS_NAME, 'newsItem__newsName--1jIcY')
        news_date_data = player.find_elements(By.CLASS_NAME, 'newsItem__newsPostDate--2BGCT')
        actual_news_data=player.find_elements(By.CLASS_NAME, 'newsItem__newsText--3mT94')
    
        for i in player_name_data:
            player_name.append(i.text)
    
        for j in news_date_data:
            player_news_date.append(j.text)
    
        for k in actual_news_data:
            player_news.append(k.text)

url='https://tools.thehuddle.com/nfl-fantasy-football-player-news/'

driver=webdriver.Chrome()
driver.get(url)

wait = WebDriverWait(driver, 10)  # 10 seconds timeout

#to be used in function
player_name=[]
player_news=[]
player_news_date=[]

#executing data_collector() for first page 
data_collector()


for i in range(0,1871):
    #moving to next page 
    wait = WebDriverWait(driver, 10)  # 10 seconds timeout
    next_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'next')))
    next_button.click()

    #calling data_collector() for next page
    data_collector()
    
driver.quit()

df = pd.DataFrame({
    'player_name': player_name,
    'player_news': player_news,
    'player_news_date': player_news_date
})

df.head()

print(len(df))

df.to_csv('player_news_table.csv', index=False)
        
    