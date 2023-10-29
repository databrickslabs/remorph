-- see https://learn.microsoft.com/en-us/sql/t-sql/queries/at-time-zone-transact-sql?view=sql-server-ver16

/*
    Moving back from DST to standard time in
    "Central European Standard Time" zone:
    offset changes from +02:00 -> +01:00.
    Change occurred on October 30th, 2022 at 03:00:00.
    Adjusted local time became 2022-10-30 02:00:00
*/

--Time before the change has DST offset (+02:00)
SELECT CONVERT(DATETIME2(0), '2022-10-30T01:01:00', 126)
AT TIME ZONE 'Central European Standard Time';
--Result: 2022-10-30 01:01:00 +02:00

/*
  Time from the "overlapped interval" is presented with DST offset (before the change)
*/
SELECT CONVERT(DATETIME2(0), '2022-10-30T02:00:00', 126)
AT TIME ZONE 'Central European Standard Time';
--Result: 2022-10-30 02:00:00 +02:00


--Time after 03:00 is regularly presented with the standard time offset (+01:00)
SELECT CONVERT(DATETIME2(0), '2022-10-30T03:01:00', 126)
AT TIME ZONE 'Central European Standard Time';
--Result: 2022-10-30 03:01:00 +01:00