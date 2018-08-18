# MIT Media Lab Visualized in Neo4j
This project scrapes all of the groups, projects and people from the MIT Media Lab and puts the data into a Neo4j Graph database.

## Future Work
Future version of this project could include adding a property to each of the group, project, and people nodes to indicate if that group/project/person is still active in the Media Lab.

Also, adding a GUI for querying could be cool.

Perhaps one could select checkboxes on the GUI that queries for a certain node label. For example, this means one could decide that they only want to see projects.

This could also involve adding a search box which queries for a specific person, project, or group, and all of the nodes which have a direct relationship to this group.

There could also be a parameter in the GUI for how many degrees of relationship one wants to visualize. For example, one could query for a project and want to see all people nodes within 2 relationships of that project.
