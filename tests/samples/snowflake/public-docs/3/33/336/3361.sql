create procedure log_message(MESSAGE VARCHAR)
returns varchar
language javascript
AS
$$
    // This is an independent transaction. Anything inserted as part of this
    // transaction is committed or rolled back based on this transaction.
    snowflake.execute (
        {sqlText: "begin transaction"}
        );
    snowflake.execute (
        {sqlText: "insert into log_table values ('" + MESSAGE + "')"}
        );
    snowflake.execute (
        {sqlText: "commit"}
        );

    // Dummy value.
    return "";
$$;

create procedure update_data()
returns varchar
language javascript
AS
$$
    snowflake.execute (
        {sqlText: "begin transaction"}
        );
    snowflake.execute (
        {sqlText: "insert into data_table (id) values (17)"}
        );
    snowflake.execute (
        {sqlText: "call log_message('You should see this saved.')"}
        );
    snowflake.execute (
        {sqlText: "rollback"}
        );

    // Dummy value.
    return "";
$$;