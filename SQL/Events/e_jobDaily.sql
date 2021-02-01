DROP EVENT IF EXISTS e_jobDaily;
DELIMITER ||
CREATE EVENT e_jobDaily
  ON SCHEDULE EVERY 1 DAY
  COMMENT 'Cleans the job table'
  DO
  BEGIN
      CALL sp_jobStatus();
  END||
DELIMITER ;
