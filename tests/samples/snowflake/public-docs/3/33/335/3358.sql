begin transaction;
insert into tracker_1 values (00, 'outer_alpha');
call sp1();
insert into tracker_1 values (09, 'outer_zulu');
commit;