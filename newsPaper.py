import psycopg2

DBNAME = "news"
db = psycopg2.connect(database=DBNAME)
c = db.cursor()
c.execute("create view shortLog as select substring(path,10) as slugPath, count(path) as num from log where path like '/article/%' group by path order by num desc")
db.close()
