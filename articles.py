import requests
import re 
import itertools
from bs4 import BeautifulSoup # Imports bs4
import sitemaps

def articles(which,start_year,end_year,start_month,end_month):
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

    cnn_articles = {}    # Input: 20xx-xx-xx     Output: [(title 1, link 1), (title 2, link 2), ...]

    titles = [] # all article titles
    links = [] # all article links
    dates = [] # dates for those articles

    if which[0]:
        for year in range(start_year,end_year+1):
            for month in range(start_month-1,end_month):

                r = requests.get(cnn_dict[year][month])
                soup = BeautifulSoup(r.text, "html.parser")
                lis = soup.find_all("li") # All links are in lis that have a date span & a sitemap-link span

                for i in lis:
                    for j in i.descendants: # gets all spans in the lis
                        data = str(j) # current span as string

                        # gets date from date span 
                        if ("class=\"date\"" in data):
                            
                            dates.append(data[data.index("20"):data.index("20")+10])

                        # gets link & title from sitemap-link span
                        if "sitemap-link" in data:

                            titles.append(data[36 + data[36:].index('"') + 2 : 36 + data[36:].index("<")])
                            links.append(data[36 : 36 + data[36:].index('"')])

                            # the date from date structure is when it was updated most recently, not always when it was posted,
                            # so in the cases where the link has the date it was posted we refer to the link's date over the one 
                            # from the date span
                            if "com/20" in data:
                                dates[-1] = data[data.index("com/20")+4:data.index("com/20")+14].replace('/','-')
                
        # list of all unique dates
        date_set = list(set(dates))

        # for each unique date, creates a list of tuples with the title & link for every article that has that date then adds that to dictionary
        for i in range(len(date_set)):
            cnn_articles[date_set[i]] = [(titles[j],links[j]) for j in range(len(dates)) if dates[j] == date_set[i]]





    # ---------------- NYT --------------- #

    nyt_articles = {}    # Input: 20xx-xx-xx     Output: [(title 1, link 1), (title 2, link 2), ...]

    titles = [] # all article titles
    links = [] # all article links
    dates = [] # dates for those articles

    if which[1]:
        for year in range(start_year,end_year+1):
            for month in range(start_month,end_month+1):
                for day in range(mday[month-1]):

                    r = requests.get(nyt_dict[year][month][day])
                    soup = BeautifulSoup(r.text, "html.parser")
                    lis = soup.find_all("li") # All links are in lis that have 1 <a> with an href (link) & title

                    for li in lis:
                        a = str(li.contents)

                        if f"https://www.nytimes.com/{year}/{str(month).zfill(2)}/{str(day+1).zfill(2)}" in a:
                            titles.append(a[a.index("\">")+2:a.index("</a>")])
                            links.append(a[a.index(f"https://www.nytimes.com/{year}/{str(month).zfill(2)}/{str(day+1).zfill(2)}"):a.index("l\">")+1])
                            dates.append(f"{year}-{str(month).zfill(2)}-{str(day+1).zfill(2)}")
                        elif "https://www.nytimes.com/article/" in a:
                            titles.append(a[a.index("\">")+2:a.index("</a>")])
                            links.append(a[a.index("https://www.nytimes.com/article"):a.index("l\">")+1])
                            dates.append(f"{year}-{str(month).zfill(2)}-{str(day+1).zfill(2)}")
                        elif f"https://www.nytimes.com/20" in a:
                            temp_link = a[a.index(f"https://www.nytimes.com/20"):a.index("l\">")+1]
                            titles.append(a[a.index("\">")+2:a.index("</a>")])
                            links.append(temp_link)
                            dates.append(str(temp_link[24:34]).replace('/','-'))

        # list of all unique dates
        date_set = list(set(dates))
        date_set.sort()

        # for each unique date, creates a list of tuples with the title & link for every article that has that date then adds that to dictionary
        # Enumerate didn't works because of the large size :P
        for i in range(len(date_set)):
            nyt_articles[date_set[i]] = [(titles[j],links[j]) for j in range(len(dates)) if dates[j] == date_set[i]]





    # ---------------- BI --------------- #
    bi_articles = {}     # Input: 20xx-xx-xx     Output: [(title 1, link 1), (title 2, link 2), ...]

    # ---------------- NYP --------------- #
    nyp_articles = {}    # Input: 20xx-xx-xx     Output: [(title 1, link 1), (title 2, link 2), ...]

    # ---------------- DM --------------- #
    dm_articles = {}     # Input: 20xx-xx-xx     Output: [(title 1, link 1), (title 2, link 2), ...]

    # ---------------- FOX --------------- #
    fox_articles = {}    # Input: 20xx-xx-xx     Output: [(title 1, link 1), (title 2, link 2), ...]

    return [cnn_articles, nyt_articles, bi_articles, nyp_articles, dm_articles, fox_articles]
