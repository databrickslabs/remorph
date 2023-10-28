USE SCHEMA testdb.INFORMATION_SCHEMA;

SELECT table_name, comment FROM TABLES WHERE TABLE_SCHEMA = 'PUBLIC' ... ;

SELECT event_timestamp, user_name FROM TABLE(LOGIN_HISTORY( ... ));