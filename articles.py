"""Module used to scrape html data"""

import itertools
import requests
from bs4 import BeautifulSoup  # Imports bs4
import pandas as pd
import sitemaps

mday = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


def make_list(article_dict, titles, dates):
    """
    Returns consolidated article dictionary

    Args:
        article_dict:
        titles:
        links:
        dates:

    """
    # list of all unique dates

    date_set = list(set(dates))
    date_set.sort()
    # for each unique date, creates a list of tuples with the title & link
    # for every article that has that date then adds that to dictionary
    for _, date in enumerate(date_set):
        article_dict[date] = [
            titles[j] for j in range(len(dates)) if dates[j] == date
        ]
    return article_dict


def cnn(cnn_dict, start_year, end_year, start_month, end_month):
    """
    Returns a list of all the articles in a given time frame

    Args:
        start_year: int representing the starting year
        end_year: int representing the ending year
        start_month: int representing the starting month
        end_month: int representing the starting month

    Returns:
     cnn_articles: list of cnn articles
    """

    titles = []  # all article titles
    dates = []  # dates for those articles

    for year in range(start_year, end_year + 1):
        for month in range(start_month - 1, end_month):
            pulled_data = requests.get(cnn_dict[year][month], timeout=5000)
            lis = BeautifulSoup(pulled_data.text, "html.parser").find_all("li")
            # All links in lis have a date span & a sitemap-link span

            for i in lis:
                for j in i.descendants:  # gets all spans in the lis
                    data = str(j)  # current span as string

                    # gets date from date span
                    if 'class="date"' in data:
                        dates.append(
                            data[data.index("20") : data.index("20") + 10]
                        )

                    # gets link & title from sitemap-link span
                    if "sitemap-link" in data:
                        titles.append(
                            data[
                                36
                                + data[36:].index('"')
                                + 2 : 36
                                + data[36:].index("<")
                            ]
                        )

                    # the date from date structure is when it was updated
                    # most recently, not always when it was posted,
                    # so in the cases where the link has the date it was
                    # posted we refer to the link's date over the one
                    # from the date span
                    if ("sitemap-link" in data) & ("com/20" in data):
                        dates[-1] = data[
                            data.index("com/20") + 4 : data.index("com/20") + 14
                        ].replace("/", "-")

    return make_list({}, titles, dates)


def nyt(nyt_dict, start_year, end_year, start_month, end_month):
    """
    Returns a list of all the articles in a given time frame

    Args:
        start_year: int representing the starting year
        end_year: int representing the ending year
        start_month: int representing the starting month
        end_month: int representing the starting month

    Returns:
        nyt_articles: list of nyt articles
    """
    titles = []  # all article titles
    dates = []  # dates for those articles

    for year in range(start_year, end_year + 1):
        for month in range(start_month, end_month + 1):
            for day in range(mday[month - 1]):
                pulled_data = requests.get(
                    nyt_dict[year][month][day], timeout=5000
                )
                lis = BeautifulSoup(pulled_data.text, "html.parser").find_all(
                    "li"
                )
                # All links are in lis that have <a> with an href (link) & title
                for i in lis:
                    content = str(i.contents)

                    if (
                        f"https://www.nytimes.com/{year}/"
                        f"{str(month).zfill(2)}/{str(day+1).zfill(2)}"
                        in content
                    ):
                        titles.append(
                            content[
                                content.index('">') + 2 : content.index("</a>")
                            ]
                        )
                        dates.append(
                            f"{year}-{str(month).zfill(2)}"
                            f"-{str(day+1).zfill(2)}"
                        )
                    elif "https://www.nytimes.com/article/" in content:
                        titles.append(
                            content[
                                content.index('">') + 2 : content.index("</a>")
                            ]
                        )
                        dates.append(
                            f"{year}-{str(month).zfill(2)}"
                            f"-{str(day+1).zfill(2)}"
                        )
                    elif "https://www.nytimes.com/20" in content:
                        titles.append(
                            content[
                                content.index('">') + 2 : content.index("</a>")
                            ]
                        )
                        dates.append(
                            str(
                                content[
                                    content.index(
                                        "https://www.nytimes.com/20"
                                    ) : content.index('l">')
                                    + 1
                                ][24:34]
                            ).replace("/", "-")
                        )

    return make_list({}, titles, dates)


def b_i(bi_dict, start_year, end_year, start_month, end_month):
    """
    Returns a list of all the articles in a given time frame

    Args:
        start_year: int representing the starting year
        end_year: int representing the ending year
        start_month: int representing the starting month
        end_month: int representing the starting month

    Returns:
        bi_articles: list of bi articles
    """
    titles = []  # all article titles
    dates = []  # dates for those articles

    for year in range(start_year, end_year + 1):
        for month in range(start_month - 1, end_month):
            pulled_data = requests.get(bi_dict[year][month], timeout=5000)
            paragraphs = BeautifulSoup(
                pulled_data.text, "html.parser"
            ).find_all("p")
            # All links are in lis that have a date span
            # & a sitemap-link span

            for paragraph in paragraphs:
                content = str(paragraph.contents)
                if "https://www.businessinsider.com/" in content:
                    titles.append(
                        content[content.index(">") + 1 : content.index("</a>")]
                    )
                    if "<br>" in content:
                        dates.append(
                            content[
                                content.index("<br>") + 17 : content.rfind("T")
                            ]
                        )
                    elif "<br/>" in content:
                        dates.append(
                            content[
                                content.index("<br/>") + 18 : content.rfind("T")
                            ]
                        )

    return make_list({}, titles, dates)


def et(et_dict, start_year, end_year, start_month, end_month):
    """
    Returns a list of all the articles in a given time frame

    Args:
        start_year: int representing the starting year
        end_year: int representing the ending year
        start_month: int representing the starting month
        end_month: int representing the starting month

    Returns:
        et_articles: list of et articles
    """
    titles = []  # all article titles
    dates = []  # dates for those articles

    for year in range(start_year, end_year + 1):
        for month in range(start_month - 1, end_month):

            pulled_data = requests.get(et_dict[year][month], timeout=5000)
            urls = BeautifulSoup(pulled_data.text, "xml").find_all("url")

            for url in urls:
                for i in url.descendants:
                    data = str(i)
                    if "<loc>" in data:
                        titles.append(
                            data[data[:-6].rfind("/") + 1 : -6].replace(
                                "-", " "
                            )
                        )
                    if "<lastmod>" in data:
                        dates.append(data[9:-25])

    return make_list({}, titles, dates)


def articles(start_year, end_year, start_month, end_month):
    """
    Scrapes article names from various new sites

    Assumptions:
        1. Format of the sitemaps does not change over time

    Args:
        start_year: int representing the starting year
        end_year: int representing the ending year
        start_month: int representing the starting month
        end_month: int representing the starting month

    Returns:
        [
        cnn_articles,
        nyt_articles,
        bi_articles,
        nyp_articles,
        dm_articles,
        fox_articles,
    ]: list of articles
    """

    [cnn_dict, nyt_dict, bi_dict, et_dict] = sitemaps.sitemaps()
    cnn_articles = cnn(cnn_dict, start_year, end_year, start_month, end_month)
    nyt_articles = nyt(nyt_dict, start_year, end_year, start_month, end_month)
    bi_articles = b_i(bi_dict, start_year, end_year, start_month, end_month)
    et_articles = et(et_dict, start_year, end_year, start_month, end_month)
    return [
        cnn_articles,
        nyt_articles,
        bi_articles,
        et_articles,
    ]


def get_data(start_year, end_year, start_month, end_month):
    """
    Scrapes article names from various new sites and puts
    them in a dataframe and provides an example dataframe
    to more easily visualize how the data is stored

    Assumptions:
        1. Format of the sitemaps does not change over time

    Args:
        start_year: int representing the starting year
        end_year: int representing the ending year
        start_month: int representing the starting month
        end_month: int representing the starting month

    Returns:
        [
        dataframe,
        example_dataframe
    ]: dataframe of all scraped data and dataframe to use
       show how data is stored
    """

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
                            for month in range(start_month, end_month + 1)
                        ]
                    )
                )
                for year in range(start_year, end_year + 1)
            ]
        )
    )

    news_data = {}
    example_data = {}

    [cnn_articles, nyt_articles, bi_articles, et_articles] = articles(
        start_year, end_year, start_month, end_month
    )

    for date in dates:
        news_data[date] = [
            cnn_articles[date],
            nyt_articles[date],
            bi_articles[date],
            et_articles[date],
        ]
    
    for i in range(4):
        example_data[dates[i]] = [
            "list",
            "list",
            "list",
            "list",
        ]

    dataframe = pd.DataFrame(news_data, index=["CNN", "NYT", "BI", "ET"])
    example_dataframe = pd.DataFrame(
        example_data, index=["CNN", "NYT", "BI", "ET"]
    )

    print(example_dataframe)

    return [dataframe, example_dataframe]
