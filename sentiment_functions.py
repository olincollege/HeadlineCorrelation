"""Imports modules"""

import itertools
import numpy as np
import matplotlib.pyplot as plt
from nltk.sentiment.vader import SentimentIntensityAnalyzer


def word_sentiment(years, months, word, data):
    """
    Determines scores for the negativity, neutrality, positivity
    and compound sentiment for the data

    Args:
        years: list of ints representing the starting and ending year
        months: list of ints representing the starting and ending month
        word: string of the specific word to be tested for
        data: pandas dataframe containing the data to test

    Returns:
        values: dict of dict of all sentiment values
        title_count: dict of titles
    """

    mday = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    news_names = ["CNN", "NYT", "BI", "ET"]

    values = {}

    for news in news_names:
        values[news] = {"neg": 0.0, "neu": 0.0, "pos": 0.0, "compound": 0.0}

    title_count = {}
    dates = list(
        itertools.chain.from_iterable(
            [
                list(
                    itertools.chain.from_iterable(
                        [
                            [
                                f"{year}-{str(month).zfill(2)}"
                                f"-{str(day+1).zfill(2)}"
                                for day in range(mday[month - 1])
                            ]
                            for month in range(months[0], months[1] + 1)
                        ]
                    )
                )
                for year in range(years[0], years[1] + 1)
            ]
        )
    )

    for news in news_names:

        final_titles = []
        for date in dates:
            for i in data[date].loc[news]:
                if word.lower() in i.lower():
                    final_titles.append(i)
        final_titles.append(final_titles)
        title_count[news] = len(final_titles)

        for title in final_titles:
            for sentiment in values[news]:
                values[news][sentiment] = (
                    values[news][sentiment]
                    + SentimentIntensityAnalyzer().polarity_scores(str(title))[
                        sentiment
                    ]
                )

        for sentiment in values[news]:
            values[news][sentiment] = (
                values[news][sentiment] / title_count[news]
            )

    return [values, title_count]


def plot_sentiment_comparison(issue_values, news_blue, news_red, title):
    """
    Plots the sentiment comparison using matplotlib

    Args:
        issue_values: dict of all sentiment values
        news_blue: string representing the first source
        news_red: string representing the second source
        title: title of graph
    """

    colors = ["blue", "black", "red"]
    x = np.array([f"{news_blue} pos", "", f"{news_red} pos"])
    y = np.array(
        [
            issue_values[news_blue]["compound"],
            0,
            issue_values[news_red]["compound"],
        ]
    )

    plt.bar(x, y, color=colors)
    plt.ylim(bottom=-0.5, top=0.5)
    plt.title(title)
    plt.axhline()
    plt.show()


def yearly_sentiment(start_year, end_year, word, data):
    """
    Determines the sentiment by year

    Args:
        start_year: int representing starting year
        end_year: int representing ending year
        word: string representing the word to test for
        data: pandas dataframe to test for

    Returns:
        yearly_values: dict of dict of sentiment values
    """

    yearly_values = {}

    for year in range(start_year, end_year + 1):
        sentiment_data = word_sentiment([year, year], [1, 12], word, data)
        yearly_values[year] = sentiment_data

    return yearly_values


def yearly_graph(start_year, end_year, word, yearly_values):
    """
    Plots the sentiment comparison using matplotlib

    Args:
        start_year: int representing starting year
        end_year: int representing ending year
        word: string representing the word to test for
        yearly_values: dict of dict of sentiment values
    """
    x = range(start_year, end_year + 1)
    cnn_y = []
    et_y = []
    nyt_y = []
    bi_y = []

    for year in range(start_year, end_year + 1):
        cnn_y.append(yearly_values[year][0]["CNN"]["compound"])
        et_y.append(yearly_values[year][0]["ET"]["compound"])
        nyt_y.append(yearly_values[year][0]["NYT"]["compound"])
        bi_y.append(yearly_values[year][0]["BI"]["compound"])

    plt.plot(x, cnn_y, "b", x, et_y, "r", x, nyt_y, "g", x, bi_y, "m")
    plt.title(f"{word} over time")
    plt.legend(
        [
            "CNN compound sentiment",
            "ET compound sentiment",
            "NYT compound sentiment",
            "BI compound sentiment",
        ]
    )
    plt.show()
