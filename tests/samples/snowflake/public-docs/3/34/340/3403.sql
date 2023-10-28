-- Create the table and insert data.
create table format1 (v varchar, i integer);
insert into format1 (v) values ('-101');
insert into format1 (v) values ('102-');
insert into format1 (v) values ('103');

-- Try to convert varchar to integer without a
-- format model.  This fails (as expected)
-- with a message similar to:
--    "Numeric value '102-' is not recognized"
update format1 set i = TO_NUMBER(v);

-- Now try again with a format specifier that allows the minus sign
-- to be at either the beginning or the end of the number.
-- Note the use of the vertical bar ("|") to indicate that
-- either format is acceptable.
update format1 set i = TO_NUMBER(v, 'MI999|999MI');
select i from format1;