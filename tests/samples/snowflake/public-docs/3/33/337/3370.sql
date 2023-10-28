begin transaction;
insert into tracker_1 values (00, 'outer_alpha');
call sp1_outer('begin transaction', 'begin transaction', 'commit', 'rollback');
insert into tracker_1 values (09, 'outer_charlie');
commit;