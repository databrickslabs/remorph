CREATE TABLE my_table(my_column string COMMENT 'this is comment3');

DESC TABLE my_table;


COMMENT ON COLUMN my_table.my_column IS 'now comment4';

DESC TABLE my_table;
