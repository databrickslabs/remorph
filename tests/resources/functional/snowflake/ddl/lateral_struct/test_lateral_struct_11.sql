-- snowflake sql:
SELECT level_1_key:level_2_key:'1' FROM demo1;

--revised snowflake sql:
SELECT
  demo1.level_key:"level_1_key":"level_2_key"['1'] AS value
FROM
    (
     select
        OBJECT_CONSTRUCT(
             'level_1_key', OBJECT_CONSTRUCT(
                'level_2_key', OBJECT_CONSTRUCT(
                   '1', 'desired_value'
                             )
                        )
                    ) as value
    )
AS demo1(level_key);


-- databricks sql:
SELECT level_1_key.level_2_key['1'] FROM demo1;

-- revised databricks sql:
SELECT
  level_key.level_1_key.level_2_key['1']
FROM
  VALUES
    (map('level_1_key', map('level_2_key', map('1', 'desired_value'))))
AS demo1(level_key);
