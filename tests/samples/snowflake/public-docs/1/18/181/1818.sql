create procedure MYPROC()
returns double
language sql
as
$$
begin
    -- Add an event without attributes
    SYSTEM$ADD_EVENT('name_a');

    -- Add an event with attributes
    let attr := {'score':89, 'pass':true};
    SYSTEM$ADD_EVENT('name_b', attr);

    -- Set attributes for the span
    SYSTEM$SET_SPAN_ATTRIBUTES('{'attr1':'value1', 'attr2':true}');

    return 3.14;
end;
$$
;