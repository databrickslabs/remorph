SELECT 
        TO_VARCHAR(GET_PATH(PARSE_JSON(json_data), 'level_1_key.level_2_key'))
            AS OLD_WAY,
        JSON_EXTRACT_PATH_TEXT(json_data, 'level_1_key.level_2_key')
            AS JSON_EXTRACT_PATH_TEXT
    FROM demo1
    ORDER BY id;