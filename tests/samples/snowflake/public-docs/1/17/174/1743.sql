select regexp_instr('It was the best of times, it was the worst of times', 'the\\W+(\\w+)',1,1,0,'e') as "result" from dual;
