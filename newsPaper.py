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
    select title, count(*) as views
       from log join articles
       on log.path = concat('/article/', articles.slug)
       group by title
       order by views desc
       limit 3;
    """)
    result = database_work(query)
    print("\nMost famous articles are:-")
    for article, views in result:
        print("\t"+"{} -- {} views".format(article, views))


def get_top_authors():
    query = ("""
    select authors.name, sum(authorArticles.num) as
        n from authors join authorArticles
        on authors.id = authorArticles.author
    group by authors.name order by n desc
    """)
    result = database_work(query)
    print("Most famous authors:-")
    for author, views in result:
        print("\t"+"{} -- {} views".format(author, views))


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
    print("Dates with more than 1% errors:-")
    for date, errorPer in result:
        print("\t"+str(date) + " -- " + str(round(errorPer, 2)) + "%")
    


if __name__ == "__main__":
    get_top_articles()
    print("-"*50+"\n")
    get_top_authors()
    print("-"*50+"\n")
    get_error_per()
    print("\n")
