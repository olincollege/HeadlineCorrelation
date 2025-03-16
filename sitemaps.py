def sitemaps():
    '''
    Docstring
    '''

    months = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
    ]
    mday = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    # CNN
    cnn_dict = dict(
        [
            (
                i,
                [
                    f"https://www.cnn.com/article/sitemap-{i}-{j}.html"
                    for j in range(1, 13)
                ],
            )
            for i in range(2014, 2025)
        ]
    )


    # New York Times
    nyt_dict = dict(
        [
            (
                i,
                dict(
                    [
                        (
                            j,
                            [
                                f"https://www.nytimes.com/sitemap/{i}/{str(j).zfill(2)}/{str(k).zfill(2)}/"
                                for k in range(1, mday[j - 1]+1)
                            ],
                        )
                        for j in range(1, 13)
                    ]
                ),
            )
            for i in range(2014, 2025)
        ]
    )


    # Business Insider
    bi_dict = dict(
        [
            (
                i,
                [
                    f"https://www.businessinsider.com/sitemap/html/{i}-{str(j).zfill(2)}.html"
                    for j in range(1, 13)
                ],
            )
            for i in range(2014, 2025)
        ]
    )


    # New York Post
    nyp_dict = dict(
        [
            (
                i,
                dict(
                    [
                        (
                            j,
                            [
                                f"https://nypost.com/{i}/{str(j).zfill(2)}/{str(k).zfill(2)}/"
                                for k in range(1, mday[j - 1]+1)
                            ],
                        )
                        for j in range(1, 13)
                    ]
                ),
            )
            for i in range(2014, 2025)
        ]
    )


    # Daily Mail
    dm_dict = dict(
        [
            (
                i,
                dict(
                    [
                        (
                            j,
                            [
                                f"https://www.dailymail.co.uk/home/sitemaparchive/day_{i}{str(j).zfill(2)}{str(k).zfill(2)}.html"
                                for k in range(1, mday[j - 1]+1)
                            ],
                        )
                        for j in range(1, 13)
                    ]
                ),
            )
            for i in range(2014, 2025)
        ]
    )


    # Fox
    fox_links = ["https://www.foxnews.com/sitemap.xml?type=articles"] + [
        f"https://www.foxnews.com/sitemap.xml?type=articles&page={i}"
        for i in range(2, 161)
    ]

    return[cnn_dict, nyt_dict, bi_dict, nyp_dict, dm_dict, fox_links]
