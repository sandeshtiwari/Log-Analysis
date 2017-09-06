import psycopg2

DBNAME = "news"
db = psycopg2.connect(database=DBNAME)
c = db.cursor()
#c.execute("select authors.id, authors.name, articles.slug from authors join articles on authors.id= articles.author")
c.execute("select path, count(path) as num from log where path like '/article/%' group by path order by num desc limit 3")
#c.execute("select slug from articles")
print("\nMost popular articles of all time are ...\n")
rows = c.fetchall()
for row in rows:
    #if row[0:12] == "/article/":
        c.execute("select title from articles where slug='"+row[0][9:]+"'")
        print(c.fetchall()[0][0] +" -- "+ str(row[1])+" views.")
        

#popular author
#c.execute("select path, count(path) as num from log where path like '/article/%' group by path order by num desc ")
authors ={}
c.execute("select path,count(path) as num from log where path like '/article/%' group by path order by num desc")
rows = c.fetchall()
for row in rows:
        query = "select authors.name,articles.title from authors join articles on authors.id = articles.author where articles.slug='"+row[0][9:]+"'"
        c.execute(query)
        datas = c.fetchall()
        if datas!= []:
                authors[datas[0][0]] = row[1]
        #c.execute("select title, count(title) from articles where  ")
        #c.execute("select sum(count(path)) from log where  ")
for key, value in authors.items():
        for keyin, valuein in authors.items():
                if keyin == key:
                        authors[key] = value+ valuein
print(authors)
db.close()
