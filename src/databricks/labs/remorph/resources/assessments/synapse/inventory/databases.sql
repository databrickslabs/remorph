--- Databases

SELECT
    NAME
     , DATABASE_ID
     , CREATE_DATE
     , STATE
     , STATE_DESC
     , COLLATION_NAME
FROM SYS.DATABASES WHERE name <> 'master' ;

