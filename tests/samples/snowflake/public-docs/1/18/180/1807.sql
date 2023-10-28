SELECT SYSTEM$TYPEOF(CONCAT('every', 'body')) FROM (values(1)) v;

----------------------------------------+
 SYSTEM$TYPEOF(CONCAT('EVERY', 'BODY')) |
----------------------------------------+
 VARCHAR(9)[LOB]                        |
----------------------------------------+