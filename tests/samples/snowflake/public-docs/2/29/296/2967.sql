CREATE VIEW my_view comment='this is comment5' AS (SELECT * FROM my_table);

SHOW VIEWS LIKE 'my_view';


COMMENT ON VIEW my_view IS 'now comment6';

SHOW VIEWS LIKE 'my_view';
