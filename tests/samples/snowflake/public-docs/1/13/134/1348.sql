WITH
lookup AS (
  SELECT column1 AS tag, PARSE_IP(column2, 'INET') AS obj FROM VALUES('San Francisco', '192.168.242.0/24'), ('New York', '192.168.243.0/24')
),
entries AS (
  SELECT PARSE_IP(column1, 'INET') AS ipv4 FROM VALUES('192.168.242.188/24'), ('192.168.243.189/24')
)
SELECT lookup.tag, entries.ipv4:host, entries.ipv4
FROM lookup, entries
WHERE lookup.tag = 'San Francisco'
AND entries.IPv4:ipv4 BETWEEN lookup.obj:ipv4_range_start AND lookup.obj:ipv4_range_end;

---------------+-------------------+-----------------------------------+
 TAG           | ENTRIES.IPV4:HOST | IPV4                              |
---------------+-------------------+-----------------------------------|
 San Francisco | "192.168.242.188" | {                                 |
               |                   |   "family": 4,                    |
               |                   |   "host": "192.168.242.188",      |
               |                   |   "ip_fields": [                  |
               |                   |     3232297660,                   |
               |                   |     0,                            |
               |                   |     0,                            |
               |                   |     0                             |
               |                   |   ],                              |
               |                   |   "ip_type": "inet",              |
               |                   |   "ipv4": 3232297660,             |
               |                   |   "ipv4_range_end": 3232297727,   |
               |                   |   "ipv4_range_start": 3232297472, |
               |                   |   "netmask_prefix_length": 24,    |
               |                   |   "snowflake$type": "ip_address"  |
               |                   | }                                 |
---------------+-------------------+-----------------------------------+