-- snowflake sql:
SELECT
  demo.level_key:"level_1_key":"level_2_key"['1'] AS col
FROM
    (
     select
        OBJECT_CONSTRUCT(
             'level_1_key', OBJECT_CONSTRUCT(
                'level_2_key', OBJECT_CONSTRUCT(
                   '1', 'desired_value'
                             )
                        )
                    ) as col
    )
AS demo(level_key);


-- databricks sql:
SELECT
 demo.level_key.level_1_key.level_2_key['1'] as col
FROM
  (SELECT STRUCT(
      STRUCT(
        STRUCT('desired_value' AS `1`) AS level_2_key
      ) AS level_1_key
    ) as col)
AS demo(level_key);
