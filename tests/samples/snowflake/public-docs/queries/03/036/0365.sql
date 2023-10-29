-- see https://docs.snowflake.com/en/sql-reference/constructs/changes

CREATE OR REPLACE TABLE t1 (
  id number(8) NOT NULL,
  c1 varchar(255) default NULL
);

-- Enable change tracking on the table.
ALTER TABLE t1 SET CHANGE_TRACKING = TRUE;

-- Initialize a session 'start timestamp' variable for the current timestamp.
SET ts1 = (SELECT CURRENT_TIMESTAMP());

INSERT INTO t1 (id,c1)
VALUES
(1,'red'),
(2,'blue'),
(3,'green');

-- Initialize a session 'end timestamp' variable for the current timestamp.
SET ts2 = (SELECT CURRENT_TIMESTAMP());

DELETE FROM t1;

-- Create a table populated by the change data between the start and end timestamps.
CREATE OR REPLACE TABLE t2 (
  c1 varchar(255) default NULL
  )
AS SELECT C1
  FROM t1
  CHANGES(INFORMATION => APPEND_ONLY)
  AT(TIMESTAMP => $ts1)
  END(TIMESTAMP => $ts2);

SELECT * FROM t2;
