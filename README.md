# JobScraper

JobScraper is a python script that scrapes the some job boards and stores the data in a SQL server

## Installation

Clone the repository to your machine.

```bash
git clone https://github.com/kjablonski/jobScraper.git
```
### Dependancies
JobScraper depends on the following python libraries:
* [dotenv][1]
* [requests][2]
* os
* pdb
* [beautifulsoup4][3]
* time
* [mysql-connector-python][4]
* datetime
* selenium

#### .env file
Sample .env file
```
dbUser=[USERNAME]
db=[DATABASE]
dbPass=[DB USER PASSWORD]
userEmail=[CONTACT EMAIL (Optional)]
userRepo=[SCRAPER REPOSITORY (Optional]
```
### SQL Setup
#TODO
## Usage

```bash
python jobScraper.py
```


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)

[1]:https://pypi.org/project/dotenv/
[2]:https://pypi.org/project/requests/
[3]:https://pypi.org/project/beautifulsoup4/
[4]:https://dev.mysql.com/doc/connector-python/en/
