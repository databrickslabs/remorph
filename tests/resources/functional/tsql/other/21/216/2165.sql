--Query type: DCL
IF EXISTS ( SELECT * FROM ( VALUES ( 'test_session' ) ) AS temp ( name ) WHERE name = 'test_session' ) DROP EVENT SESSION test_session ON SERVER;
