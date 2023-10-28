SELECT column1, PARSE_IP(column1, 'INET') FROM VALUES('192.168.242.188/24'), ('192.168.243.189/24');
--------------------+-----------------------------------+
 COLUMN1            | PARSE_IP(COLUMN1, 'INET')         |
--------------------+-----------------------------------|
 192.168.242.188/24 | {                                 |
                    |   "family": 4,                    |
                    |   "host": "192.168.242.188",      |
                    |   "ip_fields": [                  |
                    |     3232297660,                   |
                    |     0,                            |
                    |     0,                            |
                    |     0                             |
                    |   ],                              |
                    |   "ip_type": "inet",              |
                    |   "ipv4": 3232297660,             |
                    |   "ipv4_range_end": 3232297727,   |
                    |   "ipv4_range_start": 3232297472, |
                    |   "netmask_prefix_length": 24,    |
                    |   "snowflake$type": "ip_address"  |
                    | }                                 |
 192.168.243.189/24 | {                                 |
                    |   "family": 4,                    |
                    |   "host": "192.168.243.189",      |
                    |   "ip_fields": [                  |
                    |     3232297917,                   |
                    |     0,                            |
                    |     0,                            |
                    |     0                             |
                    |   ],                              |
                    |   "ip_type": "inet",              |
                    |   "ipv4": 3232297917,             |
                    |   "ipv4_range_end": 3232297983,   |
                    |   "ipv4_range_start": 3232297728, |
                    |   "netmask_prefix_length": 24,    |
                    |   "snowflake$type": "ip_address"  |
                    | }                                 |
--------------------+-----------------------------------+