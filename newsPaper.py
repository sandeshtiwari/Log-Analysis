#!/usr/bin/python3

import psycopg2
DBNAME = "news"


def database_work(query):
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute(query)
    result = c.fetchall()
    db.close()
    return result


def get_top_articles():
    query = ("""
    select articles.title, shortLogs.num
    from articles join shortLogs on articles.slug = shortLogs.slugPath
    limit 3
    """)
    result = database_work(query)
    print("\nMost famous articles are:-\n")
    for article, views in result:
        print("{} -- {} views".format(article, views))
    print("\n")


def get_top_authors():
    query = ("""
    select authors.name, sum(authorArticles.num) as
        n from authors join authorArticles
        on authors.id = authorArticles.author
    group by authors.name order by n desc
    """)
    result = database_work(query)
    print("Most famous authors:-\n")
    for author, views in result:
        print("{} -- {} views".format(author, views))
    print("\n")


def get_error_per():
    query = ("""
    select totalCount.date,
        100.0 * errorCount.count / totalCount.count as errorPer
    from totalCount join errorCount
    on errorCount.date = totalCount.date
    where 100.0 * errorCount.count / totalCount.count > 1.0
    order by totalCount.date
    """)
    result = database_work(query)
    print("Dates with more than 1% errors:-\n")
    for date, errorPer in result:
        print(str(date) + " -- " + str(round(errorPer, 2)) + "%")
    print("\n")


if __name__ == "__main__":
    get_top_articles()
    get_top_authors()
    get_error_per()
