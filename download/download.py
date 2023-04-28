'''
Name: Jack Kwan
Date of last modification: 4/22/2023

Function: download.py serves as the backend functionality 
          to provide users the ability to download packages from the database
'''
import re
import requests
import sys
import urllib.request
import zipfile
import pymysql
import sqlalchemy
from google.cloud.sql.connector import Connector

class BadRequest(Exception):
    '''Define bad request exception'''
    
def getGithubURLs(repo):
    '''Transform npm links to github links'''
    webUrl = urllib.request.urlopen(repo)
    if webUrl.getcode() == 200:
        html_cont = webUrl.read().decode("utf-8")
        r1 = r'<span id="repository-link">(.*?)<\/span>'
        try:
            reg_out = re.search(r1, html_cont)
            gitLink = "https://" + reg_out.group(1)
        except:
            raise Exception("Valid GitHub link not found.\n")
    else:
        raise Exception("npm url not able to connect.\n")
    return gitLink   
 
def download(repo_link):
    '''Functionality to download a repo as a zip'''
    if "github.com" in repo_link:
        match = re.match(r'https://github.com/([\w-]+)/([\w-]+)', repo_link)
        if not match:
            raise BadRequest('Invalid repository URL')
        owner = match.group(1)
        repo_name = match.group(2)
        zip_url = f"https://github.com/{owner}/{repo_name}/archive/refs/heads/main.zip"
        # Send a GET request to the URL and retrieve the response content
        response = requests.get(zip_url)
        zip_content = response.content
        if response.status_code == 404:
            print('master not main')
            zip_url = f"https://github.com/{owner}/{repo_name}/archive/refs/heads/master.zip"
            response = requests.get(zip_url)
            zip_content = response.content
        # Create a new file in binary write mode and write the zip content to it
        repo_name = repo_name.rstrip('/')
        with open(repo_name + ".zip", "wb") as f:
            f.write(zip_content)
            return 1
    elif "npmjs.com" in repo_link:
        repo_link = getGithubURLs(repo_link)
        match = re.match(r'https://github.com/([\w-]+)/([\w-]+)', repo_link)
        if not match:
            raise BadRequest('Invalid repository URL')
        owner = match.group(1)
        repo_name = match.group(2)
        zip_url = f"https://github.com/{owner}/{repo_name}/archive/refs/heads/main.zip"
        # Send a GET request to the URL and retrieve the response content
        response = requests.get(zip_url)
        zip_content = response.content
        if response.status_code == 404:
            print('master not main')
            zip_url = f"https://github.com/{owner}/{repo_name}/archive/refs/heads/master.zip"
            response = requests.get(zip_url)
            zip_content = response.content
        # Create a new file in binary write mode and write the zip content to it
        repo_name = repo_name.rstrip('/')
        with open(repo_name + ".zip", "wb") as f:
            f.write(zip_content)
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
    