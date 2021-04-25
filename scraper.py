from dotenv import load_dotenv
import requests
import os
import pdb
import bs4
import time
import mysql.connector
from datetime import date, datetime
from selenium import webdriver
import multiprocessing
import stateAbbr

def getJob(m_URL):
  #Load env variables for sensitive resources
  load_dotenv()
  dbUser = os.getenv('dbUser')
  db = os.environ.get('db')
  dbPass = os.getenv('dbPass')
  userEmail = os.getenv('userEmail') or ''
  userRepo = os.getenv('userRepo') or ''
  
  #Setup connections and create custom user-agent
  headerUserAgent = 'Python job board scraper bot; ' + userEmail + '; ' + userRepo
  customHeaders = {'User-Agent':headerUserAgent}
  conn = mysql.connector.connect(user=dbUser,database=db,password=dbPass,auth_plugin='mysql_native_password')
  cursor = conn.cursor()
  
  #Use requests to grab static data from the link in the div
  jobpage = requests.get(m_URL,headers = customHeaders)
  jobsoup = bs4.BeautifulSoup(jobpage.content,'html.parser')
  
  jobTitle = jobsoup.select("h2.beta")[0].text
  jobLocation = jobsoup.select("div.zeta")[0].text
  jobLocation = jobLocation.split(', ')[0] + ', ' + stateAbbr.name_to_abbr(jobLocation.split(', ')[1])
  jobDescription = jobsoup.find(id="career-detail").text
  #Package up all the job data to get ready for some SQL
  jobData = {
                "URL":m_URL,
                "jobTitle":jobTitle,
                "jobLocation":jobLocation,
                "jobPostingDate": datetime.now().date(),
                "lastUpdate":datetime.now().date(),
                "desc":jobDescription,
                "isactive":1
            }
  #See if we've already found this job or if it is new          
  queryjob = "SELECT count(*) as row_count from jobListings where URL = %s"
  cursor.execute(queryjob,(m_URL,))
  #Create default SQL script to insert into job table
  add_job = ("INSERT INTO jobListings (URL,jobTitle,jobLocation,jobPostingDate,jobLastUpdated,jobDescription,isactive) Values (%(URL)s,%(jobTitle)s,%(jobLocation)s,%(jobPostingDate)s,%(lastUpdate)s,%(desc)s,%(isactive)s)")
  if cursor.fetchall()[0][0] == 1:
    #We found a match! Overwrite the SQL command to update the date and description
    add_job = "UPDATE jobListings set jobLastUpdated = %(jobPostingDate)s,jobDescription = %(desc)s,isactive = 1 WHERE URL = %(URL)s"

  #Add the job data to the db
  cursor.execute(add_job,jobData)
  conn.commit()
  current = multiprocessing.current_process()
  print(current.name + ' : ' + jobTitle + ' - ' + jobLocation + ' - ' + m_URL)
  cursor.close()
  conn.close()
  time.sleep(7)

if __name__ == "__main__":
  #Load env variables for sensitive resources
  load_dotenv()
  dbUser = os.getenv('dbUser')
  db = os.environ.get('db')
  dbPass = os.getenv('dbPass')
  userEmail = os.getenv('userEmail') or ''
  userRepo = os.getenv('userRepo') or ''

  #Setup web brower
  
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
  divLinks = soup.select("div.g1-flex4.g2-flex2.g3-flex4.inner-wrap-space")
  #Make an array of URLs for passing to the thread pool
  links = [url+a["href"] for div in divLinks for a in div.select("a[href]")]
  
  #Clean up any duplicates
  cleanLinks = []
  for l in links:
    if l not in cleanLinks:
      cleanLinks.append(l)
  
  #Create a process pool and attach the getJob function
  pool = multiprocessing.Pool()
  pool.map(getJob, cleanLinks)
  
  print("All Done!")
