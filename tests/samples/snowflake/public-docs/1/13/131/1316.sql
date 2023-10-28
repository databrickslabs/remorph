select  0, split_part('11.22.33', '.',  0) UNION
select  1, split_part('11.22.33', '.',  1) UNION
select  2, split_part('11.22.33', '.',  2) UNION
select  3, split_part('11.22.33', '.',  3) UNION
select  4, split_part('11.22.33', '.',  4) UNION
select -1, split_part('11.22.33', '.', -1) UNION
select -2, split_part('11.22.33', '.', -2) UNION
select -3, split_part('11.22.33', '.', -3) UNION
select -4, split_part('11.22.33', '.', -4)
;