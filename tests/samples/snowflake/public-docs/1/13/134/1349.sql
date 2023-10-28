CREATE OR REPLACE TABLE ipv6_lookup (tag String, obj VARIANT);

-----------------------------------------+
 status                                  |
-----------------------------------------|
 Table IPV6_LOOKUP successfully created. |
-----------------------------------------+

INSERT INTO ipv6_lookup
    SELECT column1 AS tag, parse_ip(column2, 'INET') AS obj
    FROM VALUES('west', 'fe80:12:20c:29ff::/64'), ('east', 'fe80:12:1:29ff::/64');

-------------------------+
 number of rows inserted |
-------------------------|
                       2 |
-------------------------+

CREATE OR REPLACE TABLE ipv6_entries (obj VARIANT);
------------------------------------------+
 status                                   |
------------------------------------------|
 Table IPV6_ENTRIES successfully created. |
------------------------------------------+

INSERT INTO ipv6_entries
    SELECT parse_ip(column1, 'INET') as obj
    FROM VALUES
        ('fe80:12:20c:29ff:fe2c:430:370:2/64'),
        ('fe80:12:20c:29ff:fe2c:430:370:00F0/64'),
        ('fe80:12:20c:29ff:fe2c:430:370:0F00/64'),
        ('fe80:12:20c:29ff:fe2c:430:370:F000/64'),
        ('fe80:12:20c:29ff:fe2c:430:370:FFFF/64'),
        ('fe80:12:1:29ff:fe2c:430:370:FFFF/64'),
        ('fe80:12:1:29ff:fe2c:430:370:F000/64'),
        ('fe80:12:1:29ff:fe2c:430:370:0F00/64'),
        ('fe80:12:1:29ff:fe2c:430:370:00F0/64'),
        ('fe80:12:1:29ff:fe2c:430:370:2/64');

-------------------------+
 number of rows inserted |
-------------------------|
                      10 |
-------------------------+

SELECT lookup.tag, entries.obj:host
    FROM ipv6_lookup AS lookup, ipv6_entries AS entries
    WHERE lookup.tag = 'east'
    AND entries.obj:hex_ipv6 BETWEEN lookup.obj:hex_ipv6_range_start AND lookup.obj:hex_ipv6_range_end;

------+------------------------------------+
 TAG  | ENTRIES.OBJ:HOST                   |
------+------------------------------------|
 east | "fe80:12:1:29ff:fe2c:430:370:FFFF" |
 east | "fe80:12:1:29ff:fe2c:430:370:F000" |
 east | "fe80:12:1:29ff:fe2c:430:370:0F00" |
 east | "fe80:12:1:29ff:fe2c:430:370:00F0" |
 east | "fe80:12:1:29ff:fe2c:430:370:2"    |
------+------------------------------------+