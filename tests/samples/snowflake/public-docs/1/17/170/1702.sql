select regexp_replace('firstname middlename lastname','(.*) (.*) (.*)','\\3, \\1 \\2') as "name sort" from dual;
