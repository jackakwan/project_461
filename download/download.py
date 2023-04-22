'''
Name: Jack Kwan
Date of last modification: 4/22/2023

Function: download.py serves as the backend functionality 
          to provide users the ability to download packages from the database
'''
import sys
import urllib.request
import zipfile
import pymysql
import sqlalchemy
from google.cloud.sql.connector import Connector

def download(repo_link):
    '''Functionality to download a repo as a zip'''
    split_url = repo_link.split("/")
    username = split_url[-2]
    repo = split_url[-1].split(".")[0]
    zip_url = f"https://github.com/{username}/{repo}/archive/refs/heads/main.zip"
    zip_filename = f"{repo}.zip"
    urllib.request.urlretrieve(zip_url, zip_filename)
    with zipfile.ZipFile(zip_filename, "r") as zip_ref:
        zip_ref.extractall(repo)
        return 1

connector = Connector()

# function to return the database connection
def getconn() -> pymysql.connections.Connection:
    conn: pymysql.connections.Connection = connector.connect(
        "", "pymysql", user="", password="", db=""
    )
    return conn

def main():
    '''Calling function for download'''
    package_name = sys.argv[1]
    # create connection pool
    pool = sqlalchemy.create_engine(
        "mysql+pymysql://",
        creator=getconn,
    )
    with pool.connect() as db_conn:
        t = sqlalchemy.text("SELECT * FROM Packages")
        result = db_conn.execute(t)
        for row in result:
            if row[0] == package_name:
                download(row[1])
            else:
                print(f'No package found with name {package_name}.')
                return 0

if __name__ == "__main__":
    main()
    