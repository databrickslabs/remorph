create procedure sp1()
returns varchar
language javascript
AS
$$
    // This is part of the outer transaction that started before this
    // stored procedure was called. This is committed or rolled back
    // as part of that outer transaction.
    snowflake.execute (
        {sqlText: "insert into tracker_1 values (11, 'p1_alpha')"}
        );

    // This is an independent transaction. Anything inserted as part of this
    // transaction is committed or rolled back based on this transaction.
    snowflake.execute (
        {sqlText: "begin transaction"}
        );
    snowflake.execute (
        {sqlText: "insert into tracker_2 values (12, 'p1_bravo')"}
        );
    snowflake.execute (
        {sqlText: "rollback"}
        );

    // This is part of the outer transaction started before this
    // stored procedure was called. This is committed or rolled back
    // as part of that outer transaction.
    snowflake.execute (
        {sqlText: "insert into tracker_1 values (13, 'p1_charlie')"}
        );

    // Dummy value.
    return "";
$$;