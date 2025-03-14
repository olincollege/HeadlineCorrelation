import requests
import re 
import itertools
from bs4 import BeautifulSoup # Imports bs4
import wget # Imports wget
import sitemaps


def articles():

    # sitemaps()

    # r = requests.get(fox_links[0])
    # print('discovery' in r.text)


    # cnn_articles = {}
    # for year in range(2014,2025):
    #     for month in range(1,13):

    #         r = requests.get(cnn_dict[year][month])
    #         soup = BeautifulSoup(r.text, "html.parser")
    #         test = [i for i in soup.find_all("li")]

    #         titles = []
    #         links = []
    #         dates = []

    #         for i in test:
    #             for j in i.descendants:
    #                 if "sitemap-link" in str(j):
    #                     titles.append(
    #                         str(j)[
    #                             36
    #                             + str(j)[36:].index('"')
    #                             + 2 : 36
    #                             + str(j)[36:].index("<")
    #                         ]
    #                     )
    #                     links.append(str(j)[36 : 36 + str(j)[36:].index('"')])

    # print(titles)
    # print(links)
    # print(dates)

    # r = requests.get(nyt_dict[2024][1][0])
    # soup = BeautifulSoup(r.text, "html.parser")
    # # print(r.text)
    # test = [i for i in soup.find_all("li")]
    # titles = []
    # links = []
    # dates = []
    # for i in test:
    #     test = str(i.contents[0])
    #     if ("https:" in test) & (".html" in test) & ("2024/01/01" in test):
    #         links.append(test[test.index("https:") : test.index(".html")])
    #         titles.append(test[test.index(">") + 1 : test[4:].index("<") + 4])
    #         dates.append("2024-01-01")

    # print(titles)
    # print(links)
    # print(dates)

    return None
