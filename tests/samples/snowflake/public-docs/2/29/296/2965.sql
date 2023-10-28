CREATE SCHEMA my_schema COMMENT='this is comment1';

SHOW SCHEMAS LIKE '%schema%';


COMMENT ON SCHEMA my_schema IS 'now comment2';

SHOW SCHEMAS LIKE '%schema%';
