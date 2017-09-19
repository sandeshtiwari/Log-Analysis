#!/usr/bin/python3
import psycopg2

DBNAME = "news"
db = psycopg2.connect(database=DBNAME)
c = db.cursor()
c.execute("""
    create view shortLogs as
    select substring(path,10) as slugPath,
        count(path) as num
    from log
    where path like '/article/%'
    group by path
    order by num desc
          """)
c.execute("""
    select articles.title, shortLogs.num
    from articles join shortLogs on articles.slug = shortLogs.slugPath
    limit 3
    """)
rows = c.fetchall()
print("\nMost famous articles are:-\n")
for row in rows:
    print(row[0]+" -- "+str(row[1])+" views")
print("\n")
print("Most famous authors:-\n")
c.execute("""
    create view authorArticles as
    select articles.author, shortLogs.slugPath, shortLogs.num
    from articles join shortLogs on articles.slug = shortLogs.slugPath
    """)
c.execute("""
    select authors.name, sum(authorArticles.num) as
        n from authors join authorArticles
        on authors.id = authorArticles.author
    group by authors.name order by n desc
    """)
rows = c.fetchall()
for row in rows:
    print(row[0] + " -- " + str(row[1])+" views")
print("\n")


c.execute("""
    create view totalCount as
    select date(time) as date , count(*)
    from log
    group by date
    """)
c.execute("""
    create view errorCount as
    select date(time) as date, count(status)
    from log where status != '200 OK'
    group by date
    """)
c.execute("""
    select totalCount.date,
        100.0 * errorCount.count / totalCount.count as errorPer
    from totalCount join errorCount
    on errorCount.date = totalCount.date
    where 100.0 * errorCount.count / totalCount.count > 1.0
    order by totalCount.date
    """)
rows = c.fetchall()
print("Dates with more than 1% errors:-\n")
for row in rows:
        print(str(row[0]) + " -- " + str(round(row[1],2)) + "%")
print("\n")
db.close()
