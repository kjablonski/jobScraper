from dotenv import load_dotenv
import requests
import os
import pdb
import bs4
import mysql.connector
from datetime import date, datetime

load_dotenv(verbose=True)
dbUser = os.getenv('dbUser')
db = os.environ.get('db')
dbPass = os.getenv('dbPass')

conn = mysql.connector.connect(user=dbUser,database=db,password=dbPass,auth_plugin='mysql_native_password')
cursor = conn.cursor()
baseurl = 'https://www.foreflight.com'
url = 'https://www.foreflight.com/about/careers/'
page = requests.get(url)

soup = bs4.BeautifulSoup(page.content,'html.parser')
divs = soup.find_all("div",class_="g1-flex4 g2-flex2 g3-flex4 inner-wrap-space")

for div in divs:
    jobTitle = div.find('h3').text
    jobLocation =  div.find('div',class_='subtext').text
    link = div.find('a').get('href')
    joblink =  baseurl + link
    #print joblink
    jobpage = requests.get(joblink)
    jobsoup = bs4.BeautifulSoup(jobpage.content,'html.parser')
    jdesc = max(jobsoup.find_all('div',class_='g1-flex4 g2-flex6 g3-flex12'),key=len).get_text()
    #jdescText = bs4.BeautifulSoup(jdesc,'html.parser').prettify()
    jobData = {
                "URL":link,
                "jobTitle":jobTitle,
                "jobLocation":jobLocation,
                "lastUpdate":datetime.now().date(),
                "desc":jdesc,
                "isactive":1
              }
    queryjob = "SELECT count(*) as row_count from jobListings where URL = %s and isactive = 1"
    cursor.execute(queryjob,(link,))
    add_job = ("INSERT INTO jobListings (URL,jobTitle,jobLocation,jobLastUpdated,jobDescription,isactive) Values (%(URL)s,%(jobTitle)s,%(jobLocation)s,%(lastUpdate)s,%(desc)s,%(isactive)s)")
    if cursor.fetchall()[0][0] == 1:
        add_job = "UPDATE jobListings set jobLastUpdated = %s WHERE URL = %s and isactive = 1"
        jobData = (datetime.now().date(),link)
    #pdb.set_trace()
    cursor.execute(add_job,jobData)
    conn.commit()
    print(jobTitle + ' - ' + jobLocation)
    #print jdesc
    
cursor.close()
conn.close()
    
    
