import requests
import re 
import itertools
from bs4 import BeautifulSoup # Imports bs4
import sitemaps

def articles():
    '''
    ### Code to get data
    CNN:
    ```html
    <li>
        <span class="date">2024-01-31</span>
        <span class="sitemap-link">
            <a href="https://www.cnn.com/tech/live-news/meta-x-discord-tiktok-snap-chiefs-testimony-senate/index.html">
                Mark Zuckerberg apologizes to families over social media harms in contentious Senate hearing
            </a>
        </span>
    </li>
    ```

    NYT:
    ```html
    <li>
        <a href="https://www.nytimes.com/2023/12/31/business/dealbook/pga-tour-saudi-deal-deadline.html">
            PGA Tour and Saudi-Backed LIV Extend Deadline to Finalize Deal
        </a>
    </li>
    ```

    BI:
    ```html
    <p>
        <a href="https://www.businessinsider.com/feud-capote-vs-swans-ann-woodward-suicide-death-real-story-2024-1">
            The real story behind the suicide of American socialite Ann Woodward in &#39;Feud: Capote vs. The Swans&#39;
        </a>
        <br>2024-02-01T03:31:01.68Z
    </p>
    ```

    NYP:
    ```html
    <h3 class="story__headline headline headline--archive">
        <a href="https://nypost.com/2024/01/01/sports/og-anunoby-trending-toward-the-perfect-piece-for-knicks/" rel="" target="_self">
            Knicks&#039; big trade acquisition already looks like the &#039;perfect fit&#039; 												
        </a>
    </h3>
    ```

    DM:
    ```html
    <a href="/wires/ap/article-12917573/Christian-McCaffrey-miss-49ers-regular-season-finale-return-playoffs.html" title="">
        Christian McCaffrey will miss the 49ers regular-season finale but should return for playoffs
    </a>
    ```

    FOX:
    ```html
    <loc>
        https://www.foxnews.com/opinion/why-the-department-of-education-is-going-to-rip
    </loc>
    <lastmod>
        2025-03-12T05:00:54-04:00
    </lastmod>
    ```
    '''

    mday = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    
    [cnn_dict, nyt_dict, bi_dict, nyp_dict, dm_dict, fox_links] = sitemaps.sitemaps()

    # ---------------- CNN --------------- #
    cnn_articles = {} 

    titles = []
    links = []
    dates = []
    test_dates = []

    for year in range(2014,2024):
        for month in range(12):

            r = requests.get(cnn_dict[year][month])
            soup = BeautifulSoup(r.text, "html.parser")
            test = soup.find_all("li")

            for i in test:
                for j in i.descendants:
                    data = str(j)
                    if ("class=\"date\"" in data):
                        dates.append(data[data.index("20"):data.index("20")+10])
                        test_dates.append(data[data.index("20"):data.index("20")+10])
                    if "sitemap-link" in data:

                        titles.append(
                            data[
                                36
                                + data[36:].index('"')
                                + 2 : 36
                                + data[36:].index("<")
                            ]
                        )

                        links.append(data[36 : 36 + data[36:].index('"')])

                        if "com/20" in data:
                            dates[-1] = data[data.index("com/20")+4:data.index("com/20")+14].replace('/','-')
            
    date_set = set(dates)
    date_set = list(date_set)

    temp = [[(titles[j],links[j]) for j in range(len(dates)) if dates[j] == i] for i in date_set]
            
    for i in range(len(date_set)):
        cnn_articles[date_set[i]] = temp[i]

    for year in range(2014,2024):
        for month in range(1,13):
            for day in range(1, mday[month-1]+1):
                try:
                    print(cnn_articles[f"{year}-{str(month).zfill(2)}-{str(day).zfill(2)}"])
                except:
                    print(f"{year}-{str(month).zfill(2)}-{str(day).zfill(2)}" in date_set)
                    print(f"{year}-{str(month).zfill(2)}-{str(day).zfill(2)}" in test_dates)
                    print(f"{year}-{str(month).zfill(2)}-{str(day).zfill(2)}     BROKE")

    # ---------------- Next News --------------- #


    #print(cnn_articles)

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
