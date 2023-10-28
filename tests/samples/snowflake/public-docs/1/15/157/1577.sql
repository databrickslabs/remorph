-- create a database
create or replace database ex1_gor_x;
use database ex1_gor_x;
use schema PUBLIC;

-- create a set of tables
create or replace table x_tab_a (mycol int not null);
create or replace table x_tab_b (mycol int not null);
create or replace table x_tab_c (mycol int not null);

-- create views with increasing complexity of references
create or replace view x_view_d as
select * from x_tab_a
join x_tab_b
using ( mycol );

create or replace view x_view_e as
select x_tab_b.* from x_tab_b, x_tab_c
where x_tab_b.mycol=x_tab_c.mycol;

--create a second database
create or replace database ex1_gor_y;
use database ex1_gor_y;
use schema PUBLIC;

-- create a table in the second database
create or replace table y_tab_a (mycol int not null);

-- create more views with increasing levels of references
create or replace view y_view_b as
select * from ex1_gor_x.public.x_tab_a
join y_tab_a
using ( mycol );

create or replace view y_view_c as
select b.* from ex1_gor_x.public.x_tab_b b, ex1_gor_x.public.x_tab_c c
where b.mycol=c.mycol;

create or replace view y_view_d as
select * from ex1_gor_x.public.x_view_e;

create or replace view y_view_e as
select e.* from ex1_gor_x.public.x_view_e e, y_tab_a
where e.mycol=y_tab_a.mycol;

create or replace view y_view_f as
select e.* from ex1_gor_x.public.x_view_e e, ex1_gor_x.public.x_tab_c c, y_tab_a
where e.mycol=y_tab_a.mycol
and e.mycol=c.mycol;

-- retrieve the references for the last view created
select * from table(get_object_references(database_name=>'ex1_gor_y', schema_name=>'public', object_name=>'y_view_f'));
