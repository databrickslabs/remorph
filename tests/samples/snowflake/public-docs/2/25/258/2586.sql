SELECT seq, key, value
FROM (SELECT object_agg(k, v) o FROM objectagg_example GROUP BY g),
    LATERAL FLATTEN(input => o);

-----+------+-------+
 SEQ | KEY  | VALUE |
-----+------+-------+
 1   | name | "Sue" |
 1   | zip  | 94401 |
 2   | age  | 21    |
 2   | name | "Joe" |
-----+------+-------+