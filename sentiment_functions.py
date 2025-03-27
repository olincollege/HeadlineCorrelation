import pandas as pd
import numpy as np
import itertools
import re
import matplotlib.pyplot as plt


# import nltk
# nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer


def most_common(start_year,end_year,start_month,end_month,word,data):
    '''
    
    '''

    mday = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    news_names = ['CNN','NYT','BI','ET']

    words = {}
    title_count = {}
    dates = list(itertools.chain.from_iterable([list(itertools.chain.from_iterable([[f"{year}-{str(month).zfill(2)}-{str(day+1).zfill(2)}" for day in range(mday[month-1])] for month in range(start_month,end_month+1)])) for year in range(start_year,end_year+1)]))

    final_titles = []

    for news in news_names:
        final_titles = []
        for date in dates:
            titles = data[date].loc[news]
            for i in titles:
                if word.lower() in i.lower():
                    final_titles.append(i)
        final_titles.append(final_titles)

        temp_words = {}
        for title in final_titles[:-1]:
            for word in title.split(" "):
                word = re.sub(r'[^\w\s]','',word)
                if word in temp_words:
                    temp_words[word] += 1
                else:
                    temp_words[word] = 1
        words[news] = {k: v for k, v in sorted(temp_words.items(), key=lambda item: item[1])}
        title_count[news] = len(final_titles)
    

    return [words, title_count]





def word_sentiment(start_year,end_year,start_month,end_month,word,data):
    '''
    
    '''

    mday = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    news_names = ['CNN','NYT','BI','ET']

    values = {}

    for news in news_names:
        values[news] = {'neg': 0.0, 'neu': 0.0, 'pos': 0.0, 'compound': 0.0}

    title_count = {}
    dates = list(itertools.chain.from_iterable([list(itertools.chain.from_iterable([[f"{year}-{str(month).zfill(2)}-{str(day+1).zfill(2)}" for day in range(mday[month-1])] for month in range(start_month,end_month+1)])) for year in range(start_year,end_year+1)]))
    
    sid = SentimentIntensityAnalyzer()

    final_titles = []

    for news in news_names:

        final_titles = []
        for date in dates:
            titles = data[date].loc[news]
            for i in titles:
                if word.lower() in i.lower():
                    final_titles.append(i)
        final_titles.append(final_titles)
        title_count[news] = len(final_titles)

        for title in final_titles:
            sentiment_scores = sid.polarity_scores(str(title))
            for sentiment in values[news]:
                values[news][sentiment] = values[news][sentiment] + sentiment_scores[sentiment]

        for sentiment in values[news]:
            values[news][sentiment] = values[news][sentiment] / title_count[news]

    return [values, title_count]


def plot_sentiment_comparison(issue_values,news_blue,news_red,title):
    '''
    
    '''

    colors = ['blue','black','red']
    x = np.array([f"{news_blue} pos","", f"{news_red} pos"])
    y = np.array([issue_values[news_blue]['compound'],0, issue_values[news_red]['compound']])

    plt.bar(x,y,color=colors)
    plt.ylim(bottom=-0.5,top=0.5)
    plt.title(title)
    plt.axhline()
    plt.show()


def yearly_sentiment(start_year,end_year,word,data):
    '''

    '''

    yearly_values = {}

    for year in range(start_year,end_year+1):
        sentiment_data = word_sentiment(year, year,1,12,word,data)
        yearly_values[year] = sentiment_data

    return yearly_values

def yearly_graph(start_year,end_year,word,yearly_values):
    '''

    '''
    x = range(start_year,end_year+1)
    CNN_y = []
    ET_y = []
    NYT_y = []
    BI_y = []

    for year in range(start_year,end_year+1):
        CNN_y.append(yearly_values[year][0]['CNN']['compound'])
        ET_y.append(yearly_values[year][0]['ET']['compound'])
        NYT_y.append(yearly_values[year][0]['NYT']['compound'])
        BI_y.append(yearly_values[year][0]['BI']['compound'])

    plt.plot(x,CNN_y,'b',x,ET_y,'r',x,NYT_y,'g',x,BI_y,'m')
    plt.title(f"{word} over time")
    plt.legend(['CNN compound sentiment','ET compound sentiment','NYT compound sentiment','BI compound sentiment'])
    plt.show()

    