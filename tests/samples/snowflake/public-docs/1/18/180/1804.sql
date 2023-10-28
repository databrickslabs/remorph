SELECT SYSTEM$TYPEOF(1e10) FROM (values(1)) v;

---------------------+
 SYSTEM$TYPEOF(1E10) |
---------------------+
 NUMBER(11,0)[SB8]   |
---------------------+