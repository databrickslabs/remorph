
-- snowflake sql:
 select varchar1,
                                        float1::varchar,
                                        variant1:"Loan Number"::varchar from tmp;
                              ;

-- databricks sql:
SELECT varchar1, CAST(float1 AS STRING), CAST(variant1.`Loan Number` AS STRING) FROM tmp;
