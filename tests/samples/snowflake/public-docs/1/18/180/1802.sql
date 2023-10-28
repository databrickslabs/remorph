SELECT SYSTEM$TYPEOF(null) FROM (values(1)) v;

---------------------+
 SYSTEM$TYPEOF(NULL) |
---------------------+
 NULL[LOB]           |
---------------------+