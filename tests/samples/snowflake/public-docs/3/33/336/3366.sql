create procedure sp1_outer(
    USE_BEGIN varchar,
    USE_INNER_BEGIN varchar,
    USE_INNER_COMMIT_OR_ROLLBACK varchar,
    USE_COMMIT_OR_ROLLBACK varchar
    )
returns varchar
language javascript
AS
$$
    // This should be part of the outer transaction started before this
    // stored procedure was called. This should be committed or rolled back
    // as part of that outer transaction.
    snowflake.execute (
        {sqlText: "insert into tracker_1 values (11, 'p1_alpha')"}
        );

    // This is an independent transaction. Anything inserted as part of this
    // transaction is committed or rolled back based on this transaction.
    if (USE_BEGIN != '')  {
        snowflake.execute (
            {sqlText: USE_BEGIN}
            );
        }
    snowflake.execute (
        {sqlText: "insert into tracker_2 values (12, 'p1_bravo')"}
        );
    // Call (and optionally begin/commit-or-rollback) an inner stored proc...
    var command = "call sp2_inner('";
    command = command.concat(USE_INNER_BEGIN);
    command = command.concat("', '");
    command = command.concat(USE_INNER_COMMIT_OR_ROLLBACK);
    command = command.concat( "')" );
    snowflake.execute (
        {sqlText: command}
        );
    if (USE_COMMIT_OR_ROLLBACK != '') {
        snowflake.execute (
            {sqlText: USE_COMMIT_OR_ROLLBACK}
            );
        }

    // This is part of the outer transaction started before this
    // stored procedure was called. This is committed or rolled back
    // as part of that outer transaction.
    snowflake.execute (
        {sqlText: "insert into tracker_1 values (13, 'p1_charlie')"}
        );

    // Dummy value.
    return "";
$$;