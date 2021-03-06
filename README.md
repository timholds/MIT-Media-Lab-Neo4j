# MIT Media Lab Visualized in Neo4j
This project scrapes all of the groups, projects and people from the MIT Media Lab and puts the data into a Neo4j Graph database. <br />
**Keep scrolling for pretty pictures!**

## Prerequisites
Python 3.6,
Scrapy 1.5.1,
Neo4j-driver 1.6

See requirements.txt for more details

## Getting started
To create a local copy of this project:

* If necessary, download Neo4j and make an instance on your machine at the default bolt://localhost:7687
* Run `git clone https://github.com/timholds/MIT-Media-Lab-Neo4j` to make a copy of this repo
* Update the Neo4j credentials in `import_data_to_neo4j.py` to work with your instance
* If you wish to use the data in this repo, scraped August 2018, copy the files from the data folder to the $NEO4J_HOME/import directory**, then 
run import_data_to_neo4j.py to put the data into your neo4j instance. 

** You can find out where your NEO4J_HOME is for an instance by going into Neo4j desktop, clicking on an instance, clicking manage, clicking terminal, and typing `pwd`. 

If you wish to get an updated dataset, run each of the following functions: <br />
`scrapy crawl group_person -o group_person.csv` <br />
`scrapy crawl project_person -o proj_person.csv` <br />
`scrapy crawl group_projects -o group_proj.csv` and then run <br /> 
`import_data_to_neo4j.py`

## Useful Queries
All these examples use the Affective Computing Group, but you can replace this with any group you like. Please note that 
groups, people, and projects are all case sensitive.

To find a specific group: <br />
`Match (b:Group {name:"Affective Computing"}) return b` <br />
![Affective Computing](https://github.com/timholds/MIT-Media-Lab-Neo4j/blob/master/Screenshots/affective_computing.png)<br />

To find all the projects of a specific group: <br />
`Match (g:Group {name:"Affective Computing"})-[:HAS_PROJ]->(proj:Project) return g, proj` <br />
![Affective Computing](https://github.com/timholds/MIT-Media-Lab-Neo4j/blob/master/Screenshots/affective_computing_projects.png)<br />

To find all the people who work for a specific group: <br />
`Match (g:Group {name:"Affective Computing"})<-[:WORKS_FOR]-(person:Person) return g, person` <br />
![Affective Computing](https://github.com/timholds/MIT-Media-Lab-Neo4j/blob/master/Screenshots/affective_computing_people.png)<br />

To find all the people who work on a specific project, in this case the "QuantifyMe" project: <br />
`MATCH (per:Person)-[:WORKS_ON]->(proj:Project {title:"QuantifyMe"}) RETURN per, proj` <br />
![Affective Computing](https://github.com/timholds/MIT-Media-Lab-Neo4j/blob/master/Screenshots/quantify_me_proj.png)<br />


To find the total number of people: <br />
 `Match (p:Person) return count(p)` <br />
![Number People](https://github.com/timholds/MIT-Media-Lab-Neo4j/blob/master/Screenshots/number_people.png)<br />

Similarly, to find the total number of Projects and Groups: <br />
`Match (p:Project) return count(p)` <br />
![Number Projects](https://github.com/timholds/MIT-Media-Lab-Neo4j/blob/master/Screenshots/number_projects.png)<br />

`Match (g:Group) return count(g)`  <br />
![Number Groups](https://github.com/timholds/MIT-Media-Lab-Neo4j/blob/master/Screenshots/number_groups.png) <br />

## Tests
I imagine I should add some tests at some point to make sure 1) the scraping is still working and 2) putting things into the database is still working.

## Future Work
Future version of this project could include adding a property to each of the group, project, and people nodes to indicate if that group/project/person is still active in the Media Lab.

Also, adding a GUI for querying could be cool.

Perhaps one could select checkboxes on the GUI that queries for a certain node label. For example, this means one could decide that they only want to see projects.

This could also involve adding a search box which queries for a specific person, project, or group, and all of the nodes which have a direct relationship to this group.

There could also be a parameter in the GUI for how many degrees of relationship one wants to visualize. For example, one could query for a project and want to see all people nodes within 2 relationships of that project.
