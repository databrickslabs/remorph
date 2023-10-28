SELECT current_schema();

------------------+
 CURRENT_SCHEMA() |
------------------+
 TESTSCHEMA       |
------------------+

CREATE DATABASE db1;

------------------------------------+
               status               |
------------------------------------+
 Database DB1 successfully created. |
------------------------------------+

SELECT current_schema();

------------------+
 CURRENT_SCHEMA() |
------------------+
 PUBLIC           |
------------------+

CREATE SCHEMA sch1;

-----------------------------------+
              status               |
-----------------------------------+
 Schema SCH1 successfully created. |
-----------------------------------+

SELECT current_schema();

------------------+
 CURRENT_SCHEMA() |
------------------+
 SCH1             |
------------------+

USE SCHEMA public;

----------------------------------+
              status              |
----------------------------------+
 Statement executed successfully. |
----------------------------------+

SELECT current_schema();

------------------+
 CURRENT_SCHEMA() |
------------------+
 PUBLIC           |
------------------+