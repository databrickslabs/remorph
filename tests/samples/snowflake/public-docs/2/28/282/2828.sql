declare
    e1 exception;
    e2 exception;
begin
    statement_1;
    ...
    RETURN x;
exception
    when e1 then begin
        ...
        RETURN y;
        end;
    when e2 then begin
        ...
        RETURN z;
        end;
end;