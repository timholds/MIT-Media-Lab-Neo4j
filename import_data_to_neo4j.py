from neo4j.v1 import GraphDatabase

#driver = GraphDatabase.driver("bolt://localhost:7687")
uri = "bolt://localhost:7687"
driver = GraphDatabase.driver(uri, auth=("neo4j", "password"))

def delete_everything(driver):
    with driver.session() as session:
        return session.run(
            "MATCH (b) DETACH DELETE b")


# TODO add a variable for the root directory of this project so that the data source isn't hard coded
def import_groups_people(driver):
    with driver.session() as session:
        return session.run(
            "LOAD CSV WITH HEADERS FROM 'file:///group_person.csv' AS line "
            "MERGE (g:Group {name: line.group_name}) "
            "MERGE (person:Person {name: line.person}) "
            "MERGE (person)-[:WORKS_FOR]->(g)")


def import_groups_projects(driver):
    with driver.session() as session:
        return session.run(
            "LOAD CSV WITH HEADERS FROM 'file:///group_proj.csv' AS line "
            "MERGE (g:Group {name: line.group_name}) "
            "MERGE (proj:Project {title: line.project_title}) "
            "MERGE (g)-[:HAS_PROJ]->(proj)")


def import_projects_people(driver):
    with driver.session() as session:
        return session.run(
            "LOAD CSV WITH HEADERS FROM 'file:///proj_person.csv' AS line "
            "MERGE (proj:Project {title: line.project_title}) "
            "MERGE (person:Person {name: line.person, position: line.position}) "
            "MERGE (person)-[:WORKS_ON]->(proj)")


delete_everything(driver)
import_groups_people(driver)
import_groups_projects(driver)
import_projects_people(driver)
