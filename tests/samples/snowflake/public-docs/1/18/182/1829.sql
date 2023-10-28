-- The following calls are equivalent.
-- Both log information-level messages.
SYSTEM$LOG('info', 'Information-level message');
SYSTEM$LOG_INFO('Information-level message');

-- The following calls are equivalent.
-- Both log error messages.
SYSTEM$LOG('error', 'Error message');
SYSTEM$LOG_ERROR('Error message');


-- The following calls are equivalent.
-- Both log warning messages.
SYSTEM$LOG('warning', 'Warning message');
SYSTEM$LOG_WARN('Warning message');

-- The following calls are equivalent.
-- Both log debug messages.
SYSTEM$LOG('debug', 'Debug message');
SYSTEM$LOG_DEBUG('Debug message');

-- The following calls are equivalent.
-- Both log trace messages.
SYSTEM$LOG('trace', 'Trace message');
SYSTEM$LOG_TRACE('Trace message');

-- The following calls are equivalent.
-- Both log fatal messages.
SYSTEM$LOG('fatal', 'Fatal message');
SYSTEM$LOG_FATAL('Fatal message');