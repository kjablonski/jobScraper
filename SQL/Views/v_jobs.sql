CREATE OR REPLACE VIEW v_jobs AS
  Select
    *
  FROM
    jobListings
  WHERE
    isactive = 1
