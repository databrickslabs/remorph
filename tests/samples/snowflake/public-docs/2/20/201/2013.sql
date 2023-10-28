-- create a table from the accumulated t-Digest state for testtable.c1
create or replace table resultstate as
    select approx_percentile_accumulate(c1) s from testtable;

-- Next, use the t-Digest state to compute percentiles for testtable.

-- returns an approximated value for the 1.5th percentile of testtable.c1
select approx_percentile_estimate(s, 0.015) from resultstate;

-- returns an approximated value for the 20th percentile of testtable.c1
select approx_percentile_estimate(s, 0.2) from resultstate;