drop procedure if exists sp_jobStatus;
DELIMITER ||
create PROCEDURE sp_jobStatus ()
BEGIN
  UPDATE jobListings SET
    isactive = 0,
    jobInactiveDate = CURRENT_DATE
  WHERE
    isactive = 1 and 
    jobLastUpdated <= adddate(CURRENT_DATE, INTERVAL -2 DAY);
END ||
DELIMITER ;
