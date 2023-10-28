create table sample_numbers (f float);
insert into sample_numbers (f) values (1.2);
insert into sample_numbers (f) values (123.456);
insert into sample_numbers (f) values (1234.56);
insert into sample_numbers (f) values (-123456.789);
select to_varchar(f, '999,999.999'), to_varchar(f, 'S000,000.000') from sample_numbers;