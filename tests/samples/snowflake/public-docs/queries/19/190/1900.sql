-- see https://docs.snowflake.com/en/sql-reference/functions/system_log

SYSTEM$LOG('<level>', <message>);

SYSTEM$LOG_TRACE(<message>);
SYSTEM$LOG_DEBUG(<message>);
SYSTEM$LOG_INFO(<message>);
SYSTEM$LOG_WARN(<message>);
SYSTEM$LOG_ERROR(<message>);
SYSTEM$LOG_FATAL(<message>);