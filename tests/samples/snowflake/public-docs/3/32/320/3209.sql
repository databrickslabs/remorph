desc table ssn_record;

---------------+-------------+--------+-------+---------+-------------+------------+--------+------------+---------+----------------------------+
      name     |    type     |  kind  | null? | default | primary key | unique key | check  | expression | comment |       policy name          |
---------------+-------------+--------+-------+---------+-------------+------------+--------+------------+---------+----------------------------+
EMPLOYEE_SSN_1 | VARCHAR(32) | COLUMN | Y     | [NULL]  | N           | N          | [NULL] | [NULL]     | [NULL]  | MY_DB.MY_SCHEMA.SSN_MASK_1 |
---------------+-------------+--------+-------+---------+-------------+------------+--------+------------+---------+----------------------------+