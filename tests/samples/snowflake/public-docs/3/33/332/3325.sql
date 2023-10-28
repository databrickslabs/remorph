CREATE TABLE mytable (date TIMESTAMP_NTZ, id NUMBER, content VARIANT) CLUSTER BY (date, id);

SHOW TABLES LIKE 'mytable';
