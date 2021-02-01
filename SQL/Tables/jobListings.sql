CREATE TABLE `jobListings` (
  URL varchar(255) NOT NULL,
  jobTitle varchar(45) DEFAULT NULL,
  jobLocation varchar(45) DEFAULT NULL,
  jobPostingDate date DEFAULT NULL,
  jobLastUpdated date DEFAULT NULL,
  jobInactiveDate date DEFAULT NULL,
  jobDescription longtext,
  isactive tinyint DEFAULT NULL,
  PRIMARY KEY (URL)
) ENGINE=InnoDB DEFAULT CHARSET=utf8
