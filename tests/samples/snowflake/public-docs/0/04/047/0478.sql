SELECT a, b, c, NVL2(a, b, c) FROM i2;

--------+--------+--------+---------------+
   A    |   B    |   C    | NVL2(A, B, C) |
--------+--------+--------+---------------+
 0      | 5      | 3      | 5             |
 0      | 5      | [NULL] | 5             |
 0      | [NULL] | 3      | [NULL]        |
 0      | [NULL] | [NULL] | [NULL]        |
 [NULL] | 5      | 3      | 3             |
 [NULL] | 5      | [NULL] | [NULL]        |
 [NULL] | [NULL] | 3      | 3             |
 [NULL] | [NULL] | [NULL] | [NULL]        |
--------+--------+--------+---------------+