-- see https://docs.snowflake.com/en/sql-reference/constructs/changes

CREATE OR REPLACE TABLE t1 (
   id number(8) NOT NULL,
   c1 varchar(255) default NULL
 );

-- Enable change tracking on the table.
 ALTER TABLE t1 SET CHANGE_TRACKING = TRUE;

 -- Initialize a session variable for the current timestamp.
 SET ts1 = (SELECT CURRENT_TIMESTAMP());

 INSERT INTO t1 (id,c1)
 VALUES
 (1,'red'),
 (2,'blue'),
 (3,'green');

 DELETE FROM t1 WHERE id = 1;

 UPDATE t1 SET c1 = 'purple' WHERE id = 2;

 -- Query the change tracking metadata in the table during the interval from $ts1 to the current time.
 -- Return the full delta of the changes.
 SELECT *
 FROM t1
   CHANGES(INFORMATION => DEFAULT)
   AT(TIMESTAMP => $ts1);


 -- Query the change tracking metadata in the table during the interval from $ts1 to the current time.
 -- Return the append-only changes.
 SELECT *
 FROM t1
   CHANGES(INFORMATION => APPEND_ONLY)
   AT(TIMESTAMP => $ts1);
