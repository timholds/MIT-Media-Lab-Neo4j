# MIT Media Lab Visualized in Neo4j
This project scrapes all of the groups, projects and people from the MIT Media Lab and puts the data into a Neo4j Graph database.

## Prerequisites
Python 3.6
Scrapy 1.5.1
Ipython 6.5
Neo4j-driver 1.6

See requirements.txt for more details

## Getting started
To create a local copy of this projects:
0) If necessary, download neo4j make an instance on your machine at the default bolt://localhost:7687
1) Edit the neo4j.conf file to disable authentication by changing dbms.security.auth_enabled=true to dbms.security.auth_enabled=false
2) If you wish to use the data provided in this repo, scraped August 2018, run each of the functions in the import_data_to_neo4j.ipynb to put the data from the data folder into the database

If you wish to get an updated dataset, run each of the following functions:
scrapy crawl group_person -o group_person.csv
scrapy crawl project_person -o proj_person.csv
scrapy crawl group_projects -o group_proj.csv
and then fun the functions in import_data_to_neo4j.ipynb

## Tests
I imagine I should add some tests at some point to make sure 1) the scraping is still working and 2) putting things into the database is still working.

## Future Work
Future version of this project could include adding a property to each of the group, project, and people nodes to indicate if that group/project/person is still active in the Media Lab.

Also, adding a GUI for querying could be cool.

Perhaps one could select checkboxes on the GUI that queries for a certain node label. For example, this means one could decide that they only want to see projects.

This could also involve adding a search box which queries for a specific person, project, or group, and all of the nodes which have a direct relationship to this group.

There could also be a parameter in the GUI for how many degrees of relationship one wants to visualize. For example, one could query for a project and want to see all people nodes within 2 relationships of that project.
