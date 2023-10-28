SELECT a, b, NULLIF(a,b) FROM i;

--------+--------+-------------+
   a    |   b    | nullif(a,b) |
--------+--------+-------------+
 0      | 0      | [NULL]      |
 0      | 1      | 0           |
 0      | [NULL] | 0           |
 1      | 0      | 1           |
 1      | 1      | [NULL]      |
 1      | [NULL] | 1           |
 [NULL] | 0      | [NULL]      |
 [NULL] | 1      | [NULL]      |
 [NULL] | [NULL] | [NULL]      |
--------+--------+-------------+