-- see https://docs.snowflake.com/en/sql-reference/functions/flatten

create or replace table persons as
    select column1 as id, parse_json(column2) as c
 from values
   (12712555,
   '{ name:  { first: "John", last: "Smith"},
     contact: [
     { business:[
       { type: "phone", content:"555-1234" },
       { type: "email", content:"j.smith@company.com" } ] } ] }'),
   (98127771,
   '{ name:  { first: "Jane", last: "Doe"},
     contact: [
     { business:[
       { type: "phone", content:"555-1236" },
       { type: "email", content:"j.doe@company.com" } ] } ] }') v;

 -- Note the multiple instances of LATERAL FLATTEN in the FROM clause of the following query.
 -- Each LATERAL view is based on the previous one to refer to elements in
 -- multiple levels of arrays.

 SELECT id as "ID",
   f.value AS "Contact",
   f1.value:type AS "Type",
   f1.value:content AS "Details"
 FROM persons p,
   lateral flatten(input => p.c, path => 'contact') f,
   lateral flatten(input => f.value:business) f1;
