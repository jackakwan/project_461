'''
Name: Jack Kwan
Date of last modification: 4/22/2023

Function: download.py serves as the backend functionality 
          to provide users the ability to download packages from the database
'''
import re
import sys
import urllib.request
import zipfile
import pymysql
import sqlalchemy
from google.cloud.sql.connector import Connector

class BadRequest(Exception):
    '''Define bad request exception'''
    
def download(repo_link):
    '''Functionality to download a repo as a zip'''
    if "github.com" in repo_link:
        match = re.match(r'https://github.com/([\w-]+)/([\w-]+)', repo_link)
        if not match:
            raise BadRequest('Invalid repository URL')
        owner = match.group(1)
        repo_name = match.group(2)
        zip_url = f"https://github.com/{owner}/{repo_name}/archive/refs/heads/main.zip"
        zip_filename = f"{repo_name}.zip"
        urllib.request.urlretrieve(zip_url, zip_filename)
        with zipfile.ZipFile(zip_filename, "r") as zip_ref:
            zip_ref.extractall(repo_name)
            return 1
    elif "npmjs.com" in repo_link:
        package_name = repo_link.split("/")[-1]
        zip_url = f"https://registry.npmjs.org/{package_name}/-/{package_name}-latest.tgz"
        zip_filename = f"{package_name}.tgz"
        urllib.request.urlretrieve(zip_url, zip_filename)
        with zipfile.ZipFile(zip_filename, "r") as zip_ref:
            zip_ref.extractall(package_name)
            return 1
    else:
        return 0        #Download failed

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
    