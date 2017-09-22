Log Analysis
This is a log analysis python program that displays the - three most popular three articles of all time, who are the most popular article authors of all time, and the dates
on which more than 1% of requests lead to errors.

Software and other requirements:-
-Python 3, PostgreSQL, the psycopg2 library for python.
-Virtualbox with vagrant to run the database virtually on a linux machine
	- Virtual Box can be downloaded here - https://www.virtualbox.org/wiki/Downloads
	- Vagrant can be downloaded here - https://www.vagrantup.com/downloads.html
		-Windows users- grant network permissions to Vagrant or make firewall exception.
	-Download the VM configuration by going to https://github.com/udacity/fullstack-nanodegree-vm and forking and cloaning the repository
		-Change to this directory in your terminal(Git Bash for Windows) and run the following commands:-
			-vagrant up - this will download the linux OS and install it.
			-vagrant ssh- to get the virtual terminal for linux
	-Download the newsdata.sql file and put this in the vagrant directory from this link
		-https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip
	-Run the following command to setup the database :- psql -d news -f newsdata.sql
	-Following queries needs to be run before running the newsPaper.py file to create all the views required:-
		-create view shortLogs as select substring(path,10) as slugPath, count(path) as num from log where path like '/article/%' group by path order by num desc
		-create view authorArticles as select articles.author, shortLogs.slugPath, shortLogs.num from articles join shortLogs on articles.slug = shortLogs.slugPath
		-create view totalCount as select date(time) as date , count(*) from log group by date
		-create view errorCount as select date(time) as date, count(status) from log where status != '200 OK' group by date
How to run this program?
-After completing all the above instructions run the following command in your directory where you have saved the newsPaper.py file
	-python newsPaper.py