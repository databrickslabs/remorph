-- tsql sql:
INSERT INTO collation_demo_2 (spanish_phrase_2)
SELECT spanish_phrase_2
FROM (
    VALUES ('hola mundo'), ('adiós mundo'), ('hasta luego'), ('buenos días')
) AS temp_result (spanish_phrase_2);
