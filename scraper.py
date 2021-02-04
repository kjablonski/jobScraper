from dotenv import load_dotenv
import requests
import os
import pdb
import bs4
import time
import mysql.connector
from datetime import date, datetime
from selenium import webdriver

#Load env variables for sensitive resources
load_dotenv(verbose=True)
dbUser = os.getenv('dbUser')
db = os.environ.get('db')
dbPass = os.getenv('dbPass')
userEmail = os.getenv('userEmail') or ''
userRepo = os.getenv('userRepo') or ''

#Setup SQL connection and web brower
conn = mysql.connector.connect(user=dbUser,database=db,password=dbPass,auth_plugin='mysql_native_password')
cursor = conn.cursor()
baseurl = 'https://www.foreflight.com'
url = 'https://www.foreflight.com/about/careers/'
headerUserAgent = 'Python job board scraper bot; ' + userEmail + '; ' + userRepo
headers = {'User-Agent':headerUserAgent}
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')
options.add_argument('--user-agent='+headerUserAgent)
driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver", chrome_options=options)

#Go get the career page and allow time for content to dynamically load
driver.get(url)
time.sleep(2)
page = driver.page_source

soup = bs4.BeautifulSoup(page,'html.parser')

#Find all the divs that contain jobs and store in an array
divs = soup.find_all("div",class_="g1-flex4 g2-flex2 g3-flex4 inner-wrap-space")

#Loop through each array and grab the job title and location
for div in divs:
    jobTitle = div.find('h3').text
    jobLocation =  div.find('div',class_='subtext').text
    link = div.find('a').get('href')
    joblink =  url + link
    
    #Use requests to grab static data from the link in the div
    jobpage = requests.get(joblink)
    
    jobsoup = bs4.BeautifulSoup(jobpage.content,'html.parser')
    
    #The job description is probably the div with all the content find all returns a list
    #max(list,key=len) will return the longest string
    jdesc = max(jobsoup.find_all('div',class_='g1-flex4 g2-flex6 g3-flex12'),key=len).get_text()
    
    #Package up all the job data to get ready for some SQL
    jobData = {
                "URL":joblink,
                "jobTitle":jobTitle,
                "jobLocation":jobLocation,
                "jobPostingDate": datetime.now().date(),
                "lastUpdate":datetime.now().date(),
                "desc":jdesc,
                "isactive":1
              }
    #See if we've already found this job or if it is new          
    queryjob = "SELECT count(*) as row_count from jobListings where URL = %s and isactive = 1"
    cursor.execute(queryjob,(joblink,))
    #Create default SQL script to insert into job table
    add_job = ("INSERT INTO jobListings (URL,jobTitle,jobLocation,jobPostingDate,jobLastUpdated,jobDescription,isactive) Values (%(URL)s,%(jobTitle)s,%(jobLocation)s,%(jobPostingDate)s,%(lastUpdate)s,%(desc)s,%(isactive)s)")
    if cursor.fetchall()[0][0] == 1:
        #We found a match! Overwrite the SQL command to update the date and description
        add_job = "UPDATE jobListings set jobLastUpdated = %(jobPostingDate)s,jobDescription = %(desc)s WHERE URL = %(URL)s and isactive = 1"

    #Add the job data to the db
    cursor.execute(add_job,jobData)
    conn.commit()
    
    print(jobTitle + ' - ' + jobLocation)
    #Be nice to ForeFlight servers...
    time.sleep(7)
    
#Close SQL connections
cursor.close()
conn.close()
