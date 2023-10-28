select regexp_instr('It was the best of times, it was the worst of times', '[[:alpha:]]{2,}st', 15, 1) as "result" from dual;
