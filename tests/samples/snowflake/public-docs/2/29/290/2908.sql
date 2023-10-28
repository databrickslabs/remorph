-- Setup for example.
CREATE TABLE target_orig (k NUMBER, v NUMBER);
INSERT INTO target_orig VALUES (0, 10);

CREATE TABLE src (k NUMBER, v NUMBER);
INSERT INTO src VALUES (0, 11), (0, 12), (0, 13);

-- Multiple updates conflict with each other.
-- If ERROR_ON_NONDETERMINISTIC_MERGE=true, returns an error;
-- otherwise updates target.v with a value (e.g. 11, 12, or 13) from one of the duplicate rows (row not defined).

CREATE OR REPLACE TABLE target CLONE target_orig;

MERGE INTO target
  USING src ON target.k = src.k
  WHEN MATCHED THEN UPDATE SET target.v = src.v;

-- Updates and deletes conflict with each other.
-- If ERROR_ON_NONDETERMINISTIC_MERGE=true, returns an error;
-- otherwise either deletes the row or updates target.v with a value (e.g. 12 or 13) from one of the duplicate rows (row not defined).

CREATE OR REPLACE TABLE target CLONE target_orig;

MERGE INTO target
  USING src ON target.k = src.k
  WHEN MATCHED AND src.v = 11 THEN DELETE
  WHEN MATCHED THEN UPDATE SET target.v = src.v;

-- Multiple deletes do not conflict with each other;
-- joined values that do not match any clause do not prevent the delete (src.v = 13).
-- Merge succeeds and the target row is deleted.

CREATE OR REPLACE TABLE target CLONE target_orig;

MERGE INTO target
  USING src ON target.k = src.k
  WHEN MATCHED AND src.v <= 12 THEN DELETE;

-- Joined values that do not match any clause do not prevent an update (src.v = 12, 13).
-- Merge succeeds and the target row is set to target.v = 11.

CREATE OR REPLACE TABLE target CLONE target_orig;

MERGE INTO target
  USING src ON target.k = src.k
  WHEN MATCHED AND src.v = 11 THEN UPDATE SET target.v = src.v;

-- Use GROUP BY in the source clause to ensure that each target row joins against one row
-- in the source:

CREATE OR REPLACE TABLE target CLONE target_orig;

MERGE INTO target USING (select k, max(v) as v from src group by k) AS b ON target.k = b.k
  WHEN MATCHED THEN UPDATE SET target.v = b.v
  WHEN NOT MATCHED THEN INSERT (k, v) VALUES (b.k, b.v);