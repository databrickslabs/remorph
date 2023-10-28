SELECT * FROM collation_demo 
    WHERE spanish_phrase = uncollated_phrase COLLATE 'sp';