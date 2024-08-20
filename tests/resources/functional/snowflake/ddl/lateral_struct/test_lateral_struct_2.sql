
-- snowflake sql:
SELECT f.value:name AS "Contact",
                                        f.value:first,
                                        p.value:id::FLOAT AS "id_parsed",
                                        p.c:value:first,
                                        p.value
                                 FROM persons_struct p, lateral flatten(input => ${p}.${c}, path => 'contact') f;

-- databricks sql:
SELECT f.name AS `Contact`,
                      f.first,
                      CAST(p.value.id AS DOUBLE) AS `id_parsed`,
                      p.c.value.first,
                      p.value
               FROM persons_struct AS p LATERAL VIEW EXPLODE($p.$c.contact) AS f;
