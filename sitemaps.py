"""Sitemaps"""


def sitemaps():
    """
    Obtains sitemaps for news sources

    Returns:
        [cnn_dict, nyt_dict, bi_dict]: list of dictionaries of links of sitemaps


    """
    mday = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    # CNN
    cnn_dict = {
        i: [
            f"https://www.cnn.com/article/sitemap-{i}-{j}.html"
            for j in range(1, 13)
        ]
        for i in range(2014, 2025)
    }

    # New York Times
    nyt_dict = {
        i: {
            j: [
                f"https://www.nytimes.com/sitemap/{i}/"
                f"{str(j).zfill(2)}/{str(k).zfill(2)}/"
                for k in range(1, mday[j - 1] + 1)
            ]
            for j in range(1, 13)
        }
        for i in range(2014, 2025)
    }

    # Business Insider
    bi_dict = {
        i: [
            f"https://www.businessinsider.com/sitemap/html/"
            f"{i}-{str(j).zfill(2)}.html"
            for j in range(1, 13)
        ]
        for i in range(2014, 2025)
    }

    # Fox
    fox_dict = ["https://www.foxnews.com/sitemap.xml?type=articles"] + [
        f"https://www.foxnews.com/sitemap.xml?type=articles&page={i}"
        for i in range(2, 161)
    ]

    return [cnn_dict, nyt_dict, bi_dict, fox_dict]
