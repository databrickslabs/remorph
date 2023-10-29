-- see https://learn.microsoft.com/en-us/sql/t-sql/queries/at-time-zone-transact-sql?view=sql-server-ver16

/*
  Moving to DST in "Central European Standard Time" zone:
  offset changes from +01:00 -> +02:00
  Change occurred on March 27th, 2022 at 02:00:00.
  Adjusted local time became 2022-03-27 03:00:00.
*/

--Time before DST change has standard time offset (+01:00)
SELECT CONVERT(DATETIME2(0), '2022-03-27T01:01:00', 126)
AT TIME ZONE 'Central European Standard Time';
--Result: 2022-03-27 01:01:00 +01:00

/*
  Adjusted time from the "gap interval" (between 02:00 and 03:00)
  is moved 1 hour ahead and presented with the summer time offset
  (after the DST change)
*/
SELECT CONVERT(DATETIME2(0), '2022-03-27T02:01:00', 126)
AT TIME ZONE 'Central European Standard Time';
--Result: 2022-03-27 03:01:00 +02:00
--Time after 03:00 is presented with the summer time offset (+02:00)
SELECT CONVERT(DATETIME2(0), '2022-03-27T03:01:00', 126)
AT TIME ZONE 'Central European Standard Time';
--Result: 2022-03-27 03:01:00 +02:00