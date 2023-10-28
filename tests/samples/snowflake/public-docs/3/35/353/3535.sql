SELECT CURRENT_DATABASE();

--------------------+
 CURRENT_DATABASE() |
--------------------+
 TESTDB             |
--------------------+

CREATE DATABASE db1;

------------------------------------+
               status               |
------------------------------------+
 Database DB1 successfully created. |
------------------------------------+

SELECT CURRENT_DATABASE();

--------------------+
 CURRENT_DATABASE() |
--------------------+
 DB1                |
--------------------+

USE DATABASE testdb;

----------------------------------+
              status              |
----------------------------------+
 Statement executed successfully. |
----------------------------------+

SELECT current_database();

--------------------+
 CURRENT_DATABASE() |
--------------------+
 TESTDB             |
--------------------+