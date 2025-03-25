import pandas as pd
import numpy as np
import itertools
import re

# import nltk
# nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer


def most_common(which,start_year,end_year,start_month,end_month,word,data):

    mday = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    news_names = []
    if which[0]: news_names.append('CNN')
    if which[1]: news_names.append('NYT')
    if which[2]: news_names.append('BI')
    if which[5]: news_names.append('FOX')

    data = pd.DataFrame(data)

    words = {}
    title_count = {}
    dates = list(itertools.chain.from_iterable([list(itertools.chain.from_iterable([[f"{year}-{str(month).zfill(2)}-{str(day+1).zfill(2)}" for day in range(mday[month-1])] for month in range(start_month,end_month+1)])) for year in range(start_year,end_year+1)]))

    final_titles = []

    for news in news_names:
        final_titles = []
        for date in dates:
            titles = data[date].loc[news]
            for i in titles:
                if word.lower() in i[0].lower():
                    final_titles.append(i[0])
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





def sentiment(which,start_year,end_year,start_month,end_month,word,data):

    mday = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    news_names = []
    if which[0]: news_names.append('CNN')
    if which[1]: news_names.append('NYT')
    if which[2]: news_names.append('BI')
    if which[5]: news_names.append('FOX')

    data = pd.DataFrame(data)

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
                if word.lower() in i[0].lower():
                    final_titles.append(i[0])
        final_titles.append(final_titles)
        title_count[news] = len(final_titles)

        for title in final_titles:
            sentiment_scores = sid.polarity_scores(str(title))
            for sentiment in values[news]:
                values[news][sentiment] = values[news][sentiment] + sentiment_scores[sentiment]

        for sentiment in values[news]:
            values[news][sentiment] = values[news][sentiment] / title_count[news]

    return [values, title_count]
    