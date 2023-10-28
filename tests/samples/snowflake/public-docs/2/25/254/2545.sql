SELECT OBJECT_KEYS (
           PARSE_JSON (
               '{
                    "level_1_A": {
                                 "level_2": "two"
                                 },
                    "level_1_B": "one"
                    }'
               )
           ) AS keys
    ORDER BY 1;