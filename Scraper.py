#Importing Necessary Modules!

from selenium import webdriver
from bs4 import BeautifulSoup
import threading
from tqdm import tqdm
import pandas as pd
from collections import Counter
import numpy as np
import re
import matplotlib.pyplot as plt
from nltk.sentiment.vader import SentimentIntensityAnalyzer


#Function TO Analyse Sentiments and Make Graph
def Sentiment_Analyser():
  try:
    sid = SentimentIntensityAnalyzer()
    print("Reading Reviews...")
    data = pd.read_csv('reviews.csv')
    Positive = dict()
    Negative = dict()
    for comment in tqdm(data.Comments):
        words = re.findall(r'\w+', comment)
        for word in words:
            if (sid.polarity_scores(word)['compound']) >= 0.2 and len(word) > 2:
              if word.lower() in Positive:
                Positive[word.lower()] += 1
              else:
                Positive[word.lower()] = 1
            if (sid.polarity_scores(word)['compound']) <= -0.2 and len(word) > 2:
                if word.lower() in Negative:
                    Negative[word.lower()] += 1
                else:
                    Negative[word.lower()] = 1

    pos_Dict = Counter(Positive)
    neg_Dict = Counter(Negative)
    high = pos_Dict.most_common(10)
    low = neg_Dict.most_common(10)
    # for i, j in zip(high, low):
    #   print(i[0], i[1], "    ", j[0], j[1])
    high = dict(high)
    low = dict(low)
    poskeys = list(high.keys())
    negKeys = list(low.keys())



    barWidth = 0.20

    posratings = list(high.values())
    negRatings = list(low.values())
    # Set position of bar on X axis
    r1 = np.arange(len(posratings))
    # print(r1)
    r2 = [x + barWidth for x in r1]
    # print(r2)
    # Make the plot
    plt.figure(figsize=(10,10))
    # plt.style.use('dark_background')
    plt.title('Reviews Summary', color='black')
    plt.bar(r1, posratings, color='white', width=barWidth, label='Positive', lw=2, edgecolor='green')
    plt.bar(r2, negRatings, color='white', width=barWidth, edgecolor='red', lw=2,label='Negative')

    plt.tick_params(color='black')
    plt.yticks(color='black')
    plt.xticks([r + barWidth for r in range(len(posratings))], zip(poskeys, negKeys), rotation=15, color='black', fontsize=10)

    plt.legend()
    plt.show()

  except:
    print("OOps! Something Went Wrong !! Try Again... ")




if __name__ == '__main__':
  #Everything in an infinite loop
  print("Welcome to Amazon Reviews Scraper 1.0\n\n")
  while(1):
    print("\n\n")
    print("What do you want to do?")
    print("1. Paste a new Link.")
    print("2. Show Last Graph.")
    decision = input("Select From Above(1/2) : ")
    if decision == '1':
      pass
    elif decision == '2':
      Sentiment_Analyser()
      continue
    else:
      print("Wrong Input. Please Select a Valid Input.")
      continue
    def Comments(link):
        title = soup.find_all('a', attrs={'data-hook': 'review-title'})
        comments = soup.find_all('div', attrs={'class': 'a-row a-spacing-small review-data'})
        for i, j in zip(title, comments):
            comment = i.find('span').text + " " + j.find('span').text
            AllComments.append(comment)

    def Ratings(link):
        ratings = soup.find_all('i', attrs={'data-hook': 'review-star-rating'})
        for i in ratings:
            rating = float(i.find('span', class_='a-icon-alt').text[0:3])
            AllRatings.append(rating)

    link = input("Paste The Link Here :> ")
    AllComments = []
    AllRatings = []

    #Link Validation
    if 'amazon' not in link:
        print('Wrong Input Link')

        continue
    if 'all_reviews' not in link:
        print('Wrong Input Link')
        
        continue
    #Handling Selenium Error Using 
    #try Except Block
    try:
      print('Starting Service....')
      options = webdriver.ChromeOptions()
      options.add_argument('headless')

      driver = webdriver.Chrome("chromedriver.exe", options=options)
      print('Please Wait, Fetching Reviews.......')
      driver.get(link)
      browser = driver.page_source
      soup = BeautifulSoup(browser, 'html.parser')
      threading.Thread(target=Comments, args=(link,)).start()
      threading.Thread(target=Ratings, args=(link,)).start()
  



      Addition = link.find('&reviewer')
    #loop to Extract Reviews From Web
      for i in tqdm(range(2, 7)):

          newlink = link[:Addition] + '&pageNumber=' + str(i) + link[Addition:]
          driver.get(newlink)
          browser = driver.page_source
          soup = BeautifulSoup(browser, 'html.parser')

        #Threading 
          threading.Thread(target=Comments, args=(link,)).start()
          threading.Thread(target=Ratings, args=(link,)).start()

    
      df = pd.DataFrame({'Ratings': AllRatings,
                   'Comments': AllComments
                   })
      df.to_csv('reviews.csv')
      print(len(AllComments), len(AllRatings))

      
    except:
      print(" Something went wrong( __Check your URL or Check your internet Connection and Try Again__ )")
      continue
    Sentiment_Analyser()
  
