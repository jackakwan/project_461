"""
Name: Elijah Klein
    Date of Last Edit: 4/20/2023

    Purpose: Back End for Search Function in web api
    Details: checkTitle searches the repo title via native re regex package
        checkRM searches the according readMe for the given name
"""
import re
import sys

import pymysql
import sqlalchemy
from google.cloud.sql.connector import Connector


def checkTitle(repo_name, name):
    if re.search(
        name.lower(), repo_name.lower()
    ):  # Check the Repo Name contains the name via re regex package
        return 1
    return 0


def checkReadMe(readme, name):
    if re.search(
        name.lower(), readme.lower()
    ):  # Check the README contains the name via re regex package
        return 1
    return 0


connector = Connector()


# function to return the database connection
def getconn() -> pymysql.connections.Connection:
    conn: pymysql.connections.Connection = connector.connect(
        "", "pymysql", user="", password="", db=""
    )
    return conn


def main():
    name = sys.argv[1]
    # create connection pool
    pool = sqlalchemy.create_engine(
        "mysql+pymysql://",
        creator=getconn,
    )
    foundNames = []
    # interact with Cloud SQL database using connection pool
    with pool.connect() as db_conn:
        # query database
        t = sqlalchemy.text("SELECT * FROM Packages")
        result = db_conn.execute(t)
        # Do something with the results
        for row in result:
            if checkTitle(row[0], name) or checkReadMe(row[9], name):
                foundNames.append(1)
            else:
                foundNames.append(0)
    return foundNames


main()
