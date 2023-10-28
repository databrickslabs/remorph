create procedure sp2_inner(
    USE_BEGIN varchar,
    USE_COMMIT_OR_ROLLBACK varchar)
returns varchar
language javascript
AS
$$
    snowflake.execute (
        {sqlText: "insert into tracker_2 values (21, 'p2_alpha')"}
        );

    if (USE_BEGIN != '')  {
        snowflake.execute (
            {sqlText: USE_BEGIN}
            );
        }
    snowflake.execute (
        {sqlText: "insert into tracker_3 values (22, 'p2_bravo')"}
        );
    if (USE_COMMIT_OR_ROLLBACK != '')  {
        snowflake.execute (
            {sqlText: USE_COMMIT_OR_ROLLBACK}
            );
        }

    snowflake.execute (
        {sqlText: "insert into tracker_2 values (23, 'p2_charlie')"}
        );

    // Dummy value.
    return "";
$$;