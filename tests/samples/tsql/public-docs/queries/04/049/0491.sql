-- see https://learn.microsoft.com/en-us/sql/t-sql/statements/alter-availability-group-transact-sql?view=sql-server-ver16

ALTER AVAILABILITY GROUP [<name>] 
  SET (REQUIRED_SYNCHRONIZED_SECONDARIES_TO_COMMIT = <integer>);