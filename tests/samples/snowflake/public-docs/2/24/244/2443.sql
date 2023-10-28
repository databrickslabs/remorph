create or replace table varbin (v variant);
insert into varbin select to_variant(to_binary('snow', 'utf-8'));