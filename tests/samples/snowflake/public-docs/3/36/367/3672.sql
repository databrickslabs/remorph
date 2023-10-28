-- Set the default behavior
ALTER SESSION SET QUOTED_IDENTIFIERS_IGNORE_CASE = false;

-- Create a table with a double-quoted identifier
CREATE TABLE "Tab" (i int);  -- stored as "Tab"

-- Create a table with an unquoted identifier
CREATE TABLE TAB(j int);     -- stored as "TAB"

-- This query retrieves "Tab"
SELECT * FROM "Tab";         -- searches for "Tab"

-- Change to the all-uppercase behavior
ALTER SESSION SET QUOTED_IDENTIFIERS_IGNORE_CASE = true;

-- This query retrieves "TAB"
SELECT * FROM "Tab";         -- searches for "TAB"