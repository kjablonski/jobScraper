CREATE OR REPLACE VIEW v_activeJobs as
Select
  URL,
  jobTitle,
  jobLocation,
  substring_index(jobLocation, ',', 1) as jobLocationCity,
  substring_index(jobLocation, ',',-1) as jobLocationState,
  jobPostingDate,
  jobLastUpdated,
  jobDescription,
  company
from Jobs.jobListings
where isactive
