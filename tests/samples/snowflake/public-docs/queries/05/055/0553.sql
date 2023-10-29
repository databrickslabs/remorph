-- see https://docs.snowflake.com/en/sql-reference/data-types-datetime

CREATE TABLE timestamp_demo_table(t  TIMESTAMP,
                                  t_tz TIMESTAMP_TZ,
                                  t_ntz TIMESTAMP_NTZ,
                                  t_ltz TIMESTAMP_LTZ);
INSERT INTO timestamp_demo_table (t, t_tz, t_ntz, t_ltz) VALUES (
    '2020-03-12 01:02:03.123456789',
    '2020-03-12 01:02:03.123456789',
    '2020-03-12 01:02:03.123456789',
    '2020-03-12 01:02:03.123456789'
    );