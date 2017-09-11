import psycopg2

DBNAME = "news"
db = psycopg2.connect(database=DBNAME)
c = db.cursor()
c.execute("create view shortLog as select substring(path,10) as slugPath, count(path) as num from log where path like '/article/%' group by path order by num desc")
c.execute("select articles.title, shortLog.num from articles join shortLog on articles.slug = shortLog.slugPath limit 3")
rows = c.fetchall()
print("\nMost famous articles are:-\n")
for row in rows:
    print(row[0]+" -- "+str(row[1])+" views")
print("\n")
db.close()
