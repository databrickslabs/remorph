-- Collation
SELECT LISTAGG(spanish_phrase, '|') 
        WITHIN GROUP (ORDER BY COLLATE(spanish_phrase, 'sp'))
    FROM collation_demo
    GROUP BY english_phrase;
-- Different collation.
SELECT LISTAGG(spanish_phrase, '|') 
        WITHIN GROUP (ORDER BY COLLATE(spanish_phrase, 'utf8'))
    FROM collation_demo
    GROUP BY english_phrase;