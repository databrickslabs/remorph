select id, regexp_substr(string1, 'the\\W+\\w+') as "RESULT"
    from demo2
    order by id;