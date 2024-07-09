package com.databricks.labs.remorph.parsers.tsql

import com.databricks.labs.remorph.parsers.SqlErrorStrategy
import com.databricks.labs.remorph.parsers.tsql.TSqlParser._
import org.antlr.v4.runtime._
import org.antlr.v4.runtime.misc.IntervalSet

import scala.collection.convert.ImplicitConversions.`collection AsScalaIterable`
import scala.collection.mutable.ListBuffer

/**
 * Custom error strategy for SQL parsing <p> While we do not do anything super special here, we wish to override a
 * couple of the message generating methods and the token insert and delete messages, which do not create an exception
 * and don't allow us to create an error message in context. Additionally, we can now implement i18n, should that ever
 * become necessary.</p>
 *
 * <p>At the moment, we require valid SQL as child to the conversion process, but if we ever change that strategy, then
 * we can implement custom recovery steps here based upon context, though there is no improvement on the sync()
 * method.</p>
 */
class TSqlErrorStrategy extends SqlErrorStrategy {

  /**
   * Generate a message for the error.
   *
   * The exception contains a stack trace, from which we can construct a more informative error message than just
   * mismatched child and a huge list of things we were looking for.
   *
   * @param e
   *   the RecognitionException
   * @return
   *   the error message
   */
  override protected def generateMessage(recognizer: Parser, e: RecognitionException): String = {
    val messages = new ListBuffer[String]()

    val stringBuilder = new StringBuilder()

    // We build the messages by looking at the stack trace of the exception, but if the
    // rule translation is not found, or it is the same as the previous message, we skip it,
    // to avoid repeating the same message multiple times. This is because a recognition error
    // could be found in a parent rule or a child rule but there is no extra information
    // provided by being more specific about the rule location. ALos, in some productions
    // we may be embedded very deeply in the stack trace, so we want to avoid too many contexts
    // in a message.
    val stack = e.getStackTrace
    stack.foreach { traceElement =>
      val methodName = traceElement.getMethodName
      TSqlErrorStrategy.ruleTranslation.get(methodName).foreach { translatedMessage =>
        // Only mention a batch if we have recovered all the way to the top rule
        val shouldAppend = if (methodName == "tSqlFile") {
          messages.isEmpty
        } else {
          messages.isEmpty || messages.last != translatedMessage
        }

        if (shouldAppend) {
          messages.append(translatedMessage)
        }
      }
    }

    if (messages.nonEmpty) {
      stringBuilder.append("while parsing a ").append(messages.head)
    }

    for (i <- 1 until messages.size) {
      stringBuilder.append(" in a ").append(messages(i))
    }
    stringBuilder.toString()
  }

  /**
   * When building the list of expected tokens, we do some custom manipulation so that we do not produce a list of 750
   * possible tokens because there are so many keywords that can be used as id/column names. If ID is a valid expected
   * token, then we remove all the keywords that are there because they can be an ID.
   * @param expected
   *   the set of valid tokens at this point in the parse, where the error was found
   * @return
   *   the expected string with tokens renamed in more human friendly form
   */
  import scala.collection.mutable

  override protected def buildExpectedMessage(recognizer: Parser, expected: IntervalSet): String = {
    val expect = if (expected.contains(ID)) {
      removeIdKeywords(expected)
    } else {
      expected
    }

    val uniqueExpectedTokens = mutable.Set[String]()

    // Iterate through the expected tokens
    expect.toList.foreach { tokenId =>
      // Check if the token ID has a custom translation
      val tokenString = TSqlErrorStrategy.tokenTranslation.get(tokenId) match {
        case Some(translatedName) => translatedName
        case None => recognizer.getVocabulary.getDisplayName(tokenId)
      }
      uniqueExpectedTokens += tokenString
    }

    // Join the unique expected token strings with a comma and space for readability
    // but only take the first 12 tokens to avoid a huge list of expected tokens
    if (uniqueExpectedTokens.size <= 12) {
      return uniqueExpectedTokens.toSeq.sorted(capitalizedSort).mkString(", ")
    }
    uniqueExpectedTokens.toSeq.sorted(capitalizedSort).take(12).mkString(", ") + "..."
  }

  /**
   * Runs through the given interval and removes all the keywords that are in the set.
   * @param set
   *   The interval from whence to remove keywords that can be Identifiers
   */
  private def removeIdKeywords(set: IntervalSet): IntervalSet = {
    set.subtract(TSqlErrorStrategy.keywordIDs)
  }
}

object TSqlErrorStrategy {

  // A map that will override teh default display name for tokens that represent text with
  // pattern matches like IDENTIFIER, STRING, etc.
  private val tokenTranslation: Map[Int, String] = Map(
    AAPSEUDO -> "@@Reference",
    DOUBLE_QUOTE_ID -> "Identifier",
    FLOAT -> "Float",
    ID -> "Identifier",
    INT -> "Integer",
    LOCAL_ID -> "@Local",
    MONEY -> "$Currency",
    REAL -> "Real",
    SQUARE_BRACKET_ID -> "Identifier",
    STRING -> "'String'",
    TEMP_ID -> "Identifier",
    -1 -> "End of batch",

    // When the next thing we expect can be every statement, we just say "statement"
    ALTER -> "Statement",
    BACKUP -> "Statement",
    BEGIN -> "Statement",
    BREAK -> "Statement",
    CHECKPOINT -> "Statement",
    CLOSE -> "Statement",
    COMMIT -> "Statement",
    CONTINUE -> "Statement",
    CREATE -> "Statement",
    DEALLOCATE -> "Statement",
    DECLARE -> "Statement",
    DELETE -> "Statement",
    DROP -> "Statement",
    END -> "Statement",
    EXECUTE -> "Statement",
    EXECUTE -> "Statement",
    FETCH -> "Statement",
    GOTO -> "Statement",
    GRANT -> "Statement",
    IF -> "Statement",
    INSERT -> "Statement",
    KILL -> "Statement",
    MERGE -> "Statement",
    OPEN -> "Statement",
    PRINT -> "Statement",
    RAISERROR -> "Statement",
    RECONFIGURE -> "Statement",
    RETURN -> "Statement",
    REVERT -> "Statement",
    ROLLBACK -> "Statement",
    SAVE -> "Statement",
    SELECT -> "Select Statement",
    SET -> "Statement",
    SETUSER -> "Statement",
    SHUTDOWN -> "Statement",
    TRUNCATE -> "Statement",
    UPDATE -> "Statement",
    USE -> "Statement",
    WAITFOR -> "Statement",
    WHILE -> "Statement",
    WITHIN -> "Statement",

    // No need to distinguish between operators

    AND_ASSIGN -> "Assignment Operator",
    OR_ASSIGN -> "Assignment Operator",
    XOR_ASSIGN -> "Assignment Operator",
    BANG -> "Operator",
    BIT_AND -> "Operator",
    BIT_NOT -> "Operator",
    BIT_OR -> "Operator",
    BIT_XOR -> "Operator",
    DE -> "Operator",
    DIV -> "Operator",
    DOUBLE_BAR -> "Operator",
    EQ -> "Operator",
    GT -> "Operator",
    LT -> "Operator",
    ME -> "Operator",
    MEA -> "Operator",
    MINUS -> "Operator",
    MOD -> "Operator",
    PE -> "Operator",
    PLUS -> "Operator",
    SE -> "Operator")

  private val ruleTranslation: Map[String, String] = Map(
    "tSqlFile" -> "T-SQL batch",
    "selectStatement" -> "SELECT statement",
    "selectStatementStandalone" -> "SELECT statement",
    "selectList" -> "SELECT list",
    "selectListElement" -> "SELECT list element",
    "selectItem" -> "SELECT item",
    "fromClause" -> "FROM clause",
    "whereClause" -> "WHERE clause",
    "groupByClause" -> "GROUP BY clause",
    "havingClause" -> "HAVING clause",
    "orderByClause" -> "ORDER BY clause",
    "limitClause" -> "LIMIT clause",
    "offsetClause" -> "OFFSET clause",
    "joinClause" -> "JOIN clause",
    "joinCondition" -> "JOIN condition",
    "joinType" -> "JOIN type",
    "joinOn" -> "JOIN ON",
    "joinUsing" -> "JOIN USING",
    "joinTable" -> "JOIN table",
    "joinAlias" -> "JOIN alias",
    "joinColumn" -> "JOIN column",
    "joinExpression" -> "JOIN expression",
    "joinOperator" -> "JOIN operator",
    "joinSubquery" -> "JOIN subquery",
    "joinSubqueryAlias" -> "JOIN subquery alias",
    "joinSubqueryColumn" -> "JOIN subquery column",
    "joinSubqueryExpression" -> "JOIN subquery expression",
    "joinSubqueryOperator" -> "JOIN subquery operator",
    "joinSubqueryTable" -> "JOIN subquery table",
    "joinSubqueryTableAlias" -> "JOIN subquery table alias",
    "joinSubqueryTableColumn" -> "JOIN subquery table column",
    "joinSubqueryTableExpression" -> "JOIN subquery table expression",
    "joinSubqueryTableOperator" -> "JOIN subquery table operator",
    "joinSubqueryTableSubquery" -> "JOIN subquery table subquery",
    "joinSubqueryTableSubqueryAlias" -> "JOIN subquery table subquery alias",
    "joinSubqueryTableSubqueryColumn" -> "JOIN subquery table subquery column",
    "joinSubqueryTableSubqueryExpression" -> "JOIN subquery table subquery expression",
    "joinSubqueryTableSubqueryOperator" -> "JOIN subquery table subquery operator",
    "joinSubqueryTableSubqueryTable" -> "JOIN subquery table subquery table",
    "updateStatement" -> "UPDATE statement",
    "update" -> "UPDATE statement",
    "topClause" -> "TOP clause",
    "ddlObject" -> "TABLE object",
    "withTableHints" -> "WITH table hints",
    "updateElem" -> "UPDATE element specification",
    "outputClause" -> "OUTPUT clause",
    "updateWhereClause" -> "WHERE clause",
    "optionClause" -> "OPTION clause",

    // Etc
    "tableSource" -> "table source",
    "tableSourceItem" -> "table source")

  private val keywordIDs: IntervalSet = new IntervalSet(
    ABORT,
    ABORT_AFTER_WAIT,
    ABSENT,
    ABSOLUTE,
    ACCENT_SENSITIVITY,
    ACCESS,
    ACTION,
    ACTIVATION,
    ACTIVE,
    ADD,
    ADDRESS,
    ADMINISTER,
    AES,
    AES_128,
    AES_192,
    AES_256,
    AFFINITY,
    AFTER,
    AGGREGATE,
    ALGORITHM,
    ALL_CONSTRAINTS,
    ALL_ERRORMSGS,
    ALL_INDEXES,
    ALL_LEVELS,
    ALLOW_CONNECTIONS,
    ALLOW_ENCRYPTED_VALUE_MODIFICATIONS,
    ALLOW_MULTIPLE_EVENT_LOSS,
    ALLOW_PAGE_LOCKS,
    ALLOW_ROW_LOCKS,
    ALLOW_SINGLE_EVENT_LOSS,
    ALLOW_SNAPSHOT_ISOLATION,
    ALLOWED,
    ALWAYS,
    ANONYMOUS,
    ANSI_DEFAULTS,
    ANSI_NULL_DEFAULT,
    ANSI_NULL_DFLT_OFF,
    ANSI_NULL_DFLT_ON,
    ANSI_NULLS,
    ANSI_PADDING,
    ANSI_WARNINGS,
    APPEND,
    APPLICATION,
    APPLICATION_LOG,
    APPLY,
    ARITHABORT,
    ARITHIGNORE,
    ASSEMBLY,
    ASYMMETRIC,
    ASYNCHRONOUS_COMMIT,
    AT_KEYWORD,
    AUDIT,
    AUDIT_GUID,
    AUTHENTICATE,
    AUTHENTICATION,
    AUTO,
    AUTO_CLEANUP,
    AUTO_CLOSE,
    AUTO_CREATE_STATISTICS,
    AUTO_DROP,
    AUTO_SHRINK,
    AUTO_UPDATE_STATISTICS,
    AUTO_UPDATE_STATISTICS_ASYNC,
    AUTOGROW_ALL_FILES,
    AUTOGROW_SINGLE_FILE,
    AUTOMATED_BACKUP_PREFERENCE,
    AUTOMATIC,
    AVAILABILITY,
    AVAILABILITY_MODE,
    BACKUP_CLONEDB,
    BACKUP_PRIORITY,
    BASE64,
    BEFORE,
    BEGIN_DIALOG,
    BIGINT,
    BINARY_KEYWORD,
    BINDING,
    BLOB_STORAGE,
    BLOCK,
    BLOCKERS,
    BLOCKSIZE,
    BROKER,
    BROKER_INSTANCE,
    BUFFER,
    BUFFERCOUNT,
    BULK_LOGGED,
    CACHE,
    CALLED,
    CALLER,
    CAP_CPU_PERCENT,
    CAST,
    CATALOG,
    CATCH,
    CERTIFICATE,
    CHANGE,
    CHANGE_RETENTION,
    CHANGE_TRACKING,
    CHANGES,
    CHANGETABLE,
    CHECK_EXPIRATION,
    CHECK_POLICY,
    CHECKALLOC,
    CHECKCATALOG,
    CHECKCONSTRAINTS,
    CHECKDB,
    CHECKFILEGROUP,
    CHECKSUM,
    CHECKTABLE,
    CLASSIFIER_FUNCTION,
    CLEANTABLE,
    CLEANUP,
    CLONEDATABASE,
    CLUSTER,
    COLLECTION,
    COLUMN_ENCRYPTION_KEY,
    COLUMN_MASTER_KEY,
    COLUMNS,
    COLUMNSTORE,
    COLUMNSTORE_ARCHIVE,
    COMMITTED,
    COMPATIBILITY_LEVEL,
    COMPRESS_ALL_ROW_GROUPS,
    COMPRESSION,
    COMPRESSION_DELAY,
    CONCAT,
    CONCAT_NULL_YIELDS_NULL,
    CONFIGURATION,
    CONNECT,
    CONNECTION,
    CONTAINMENT,
    CONTENT,
    CONTEXT,
    CONTINUE_AFTER_ERROR,
    CONTRACT,
    CONTRACT_NAME,
    CONTROL,
    CONVERSATION,
    COOKIE,
    COPY_ONLY,
    COUNTER,
    CPU,
    CREATE_NEW,
    CREATION_DISPOSITION,
    CREDENTIAL,
    CRYPTOGRAPHIC,
    CURSOR_CLOSE_ON_COMMIT,
    CURSOR_DEFAULT,
    CYCLE,
    DATA,
    DATA_COMPRESSION,
    DATA_PURITY,
    DATA_SOURCE,
    DATABASE_MIRRORING,
    DATASPACE,
    DATE_CORRELATION_OPTIMIZATION,
    DAYS,
    DB_CHAINING,
    DB_FAILOVER,
    DBCC,
    DBREINDEX,
    DDL,
    DECRYPTION,
    DEFAULT,
    DEFAULT_DATABASE,
    DEFAULT_DOUBLE_QUOTE,
    DEFAULT_FULLTEXT_LANGUAGE,
    DEFAULT_LANGUAGE,
    DEFAULT_SCHEMA,
    DEFINITION,
    DELAY,
    DELAYED_DURABILITY,
    DELETED,
    DEPENDENTS,
    DES,
    DESCRIPTION,
    DESX,
    DETERMINISTIC,
    DHCP,
    DIAGNOSTICS,
    DIALOG,
    DIFFERENTIAL,
    DIRECTORY_NAME,
    DISABLE,
    DISABLE_BROKER,
    DISABLED,
    DISTRIBUTION,
    DOCUMENT,
    DROP_EXISTING,
    DROPCLEANBUFFERS,
    DTC_SUPPORT,
    DYNAMIC,
    ELEMENTS,
    EMERGENCY,
    EMPTY,
    ENABLE,
    ENABLE_BROKER,
    ENABLED,
    ENCRYPTED,
    ENCRYPTED_VALUE,
    ENCRYPTION,
    ENCRYPTION_TYPE,
    ENDPOINT,
    ENDPOINT_URL,
    ERROR,
    ERROR_BROKER_CONVERSATIONS,
    ESTIMATEONLY,
    EVENT,
    EVENT_RETENTION_MODE,
    EXCLUSIVE,
    EXECUTABLE,
    EXECUTABLE_FILE,
    EXPIREDATE,
    EXPIRY_DATE,
    EXPLICIT,
    EXTENDED_LOGICAL_CHECKS,
    EXTENSION,
    EXTERNAL_ACCESS,
    FAIL_OPERATION,
    FAILOVER,
    FAILOVER_MODE,
    FAILURE,
    FAILURE_CONDITION_LEVEL,
    FAILURECONDITIONLEVEL,
    FAN_IN,
    FAST_FORWARD,
    FILE_SNAPSHOT,
    FILEGROUP,
    FILEGROWTH,
    FILENAME,
    FILEPATH,
    FILESTREAM,
    FILESTREAM_ON,
    FILTER,
    FIRST,
    FMTONLY,
    FOLLOWING,
    FOR,
    FORCE,
    FORCE_FAILOVER_ALLOW_DATA_LOSS,
    FORCE_SERVICE_ALLOW_DATA_LOSS,
    FORCEPLAN,
    FORCESCAN,
    FORCESEEK,
    FORMAT,
    FORWARD_ONLY,
    FREE,
    FULLSCAN,
    FULLTEXT,
    GB,
    GENERATED,
    GET,
    GETROOT,
    GLOBAL,
    GO,
    GOVERNOR,
    GROUP_MAX_REQUESTS,
    GROUPING,
    HADR,
    HASH,
    HASHED,
    HEALTH_CHECK_TIMEOUT,
    HEALTHCHECKTIMEOUT,
    HEAP,
    HIDDEN_KEYWORD,
    HIERARCHYID,
    HIGH,
    HONOR_BROKER_PRIORITY,
    HOURS,
    IDENTITY_VALUE,
    IGNORE_CONSTRAINTS,
    IGNORE_DUP_KEY,
    IGNORE_REPLICATED_TABLE_CACHE,
    IGNORE_TRIGGERS,
    IIF,
    IMMEDIATE,
    IMPERSONATE,
    IMPLICIT_TRANSACTIONS,
    IMPORTANCE,
    INCLUDE,
    INCLUDE_NULL_VALUES,
    INCREMENT,
    INCREMENTAL,
    INFINITE,
    INIT,
    INITIATOR,
    INPUT,
    INSENSITIVE,
    INSERTED,
    INSTEAD,
    IO,
    IP,
    ISOLATION,
    JOB,
    JSON,
    JSON_ARRAY,
    JSON_OBJECT,
    KB,
    KEEPDEFAULTS,
    KEEPIDENTITY,
    KERBEROS,
    KEY_PATH,
    KEY_SOURCE,
    KEY_STORE_PROVIDER_NAME,
    KEYS,
    KEYSET,
    KWINT,
    LANGUAGE,
    LAST,
    LEVEL,
    LIBRARY,
    LIFETIME,
    LINKED,
    LINUX,
    LIST,
    LISTENER,
    LISTENER_IP,
    LISTENER_PORT,
    LISTENER_URL,
    LOB_COMPACTION,
    LOCAL,
    LOCAL_SERVICE_NAME,
    LOCATION,
    LOCK,
    LOCK_ESCALATION,
    LOGIN,
    LOOP,
    LOW,
    MANUAL,
    MARK,
    MASK,
    MASKED,
    MASTER,
    MATCHED,
    MATERIALIZED,
    MAX,
    MAX_CPU_PERCENT,
    MAX_DISPATCH_LATENCY,
    MAX_DOP,
    MAX_DURATION,
    MAX_EVENT_SIZE,
    MAX_FILES,
    MAX_IOPS_PER_VOLUME,
    MAX_MEMORY,
    MAX_MEMORY_PERCENT,
    MAX_OUTSTANDING_IO_PER_VOLUME,
    MAX_PROCESSES,
    MAX_QUEUE_READERS,
    MAX_ROLLOVER_FILES,
    MAX_SIZE,
    MAXSIZE,
    MAXTRANSFER,
    MAXVALUE,
    MB,
    MEDIADESCRIPTION,
    MEDIANAME,
    MEDIUM,
    MEMBER,
    MEMORY_OPTIMIZED_DATA,
    MEMORY_PARTITION_MODE,
    MESSAGE,
    MESSAGE_FORWARD_SIZE,
    MESSAGE_FORWARDING,
    MIN_CPU_PERCENT,
    MIN_IOPS_PER_VOLUME,
    MIN_MEMORY_PERCENT,
    MINUTES,
    MINVALUE,
    MIRROR,
    MIRROR_ADDRESS,
    MIXED_PAGE_ALLOCATION,
    MODE,
    MODIFY,
    MOVE,
    MULTI_USER,
    MUST_CHANGE,
    NAME,
    NESTED_TRIGGERS,
    NEW_ACCOUNT,
    NEW_BROKER,
    NEW_PASSWORD,
    NEWNAME,
    NEXT,
    NO,
    NO_CHECKSUM,
    NO_COMPRESSION,
    NO_EVENT_LOSS,
    NO_INFOMSGS,
    NO_QUERYSTORE,
    NO_STATISTICS,
    NO_TRUNCATE,
    NOCOUNT,
    NODES,
    NOEXEC,
    NOEXPAND,
    NOFORMAT,
    NOINDEX,
    NOINIT,
    NOLOCK,
    NON_TRANSACTED_ACCESS,
    NONE,
    NORECOMPUTE,
    NORECOVERY,
    NOREWIND,
    NOSKIP,
    NOTIFICATION,
    NOTIFICATIONS,
    NOUNLOAD,
    NTILE,
    NTLM,
    NUMANODE,
    NUMBER,
    NUMERIC_ROUNDABORT,
    OBJECT,
    OFFLINE,
    OFFSET,
    OLD_ACCOUNT,
    OLD_PASSWORD,
    ON_FAILURE,
    ON,
    OFF,
    ONLINE,
    ONLY,
    OPEN_EXISTING,
    OPENJSON,
    OPERATIONS,
    OPTIMISTIC,
    OUT,
    OUTPUT,
    OVERRIDE,
    OWNER,
    OWNERSHIP,
    PAD_INDEX,
    PAGE,
    PAGE_VERIFY,
    PAGECOUNT,
    PAGLOCK,
    PARAM_NODE,
    PARAMETERIZATION,
    PARSEONLY,
    PARTIAL,
    PARTITION,
    PARTITIONS,
    PARTNER,
    PASSWORD,
    PATH,
    PAUSE,
    PDW_SHOWSPACEUSED,
    PER_CPU,
    PER_DB,
    PER_NODE,
    PERMISSION_SET,
    PERSIST_SAMPLE_PERCENT,
    PERSISTED,
    PHYSICAL_ONLY,
    PLATFORM,
    POISON_MESSAGE_HANDLING,
    POLICY,
    POOL,
    PORT,
    PRECEDING,
    PRECISION,
    PREDICATE,
    PRIMARY_ROLE,
    PRIOR,
    PRIORITY,
    PRIORITY_LEVEL,
    PRIVATE,
    PRIVATE_KEY,
    PRIVILEGES,
    PROCCACHE,
    PROCEDURE_NAME,
    PROCESS,
    PROFILE,
    PROPERTY,
    PROVIDER,
    PROVIDER_KEY_NAME,
    PYTHON,
    QUERY,
    QUEUE,
    QUEUE_DELAY,
    QUOTED_IDENTIFIER,
    R,
    RANDOMIZED,
    RANGE,
    RC2,
    RC4,
    RC4_128,
    READ_COMMITTED_SNAPSHOT,
    READ_ONLY,
    READ_ONLY_ROUTING_LIST,
    READ_WRITE,
    READ_WRITE_FILEGROUPS,
    READCOMMITTED,
    READCOMMITTEDLOCK,
    READONLY,
    READPAST,
    READUNCOMMITTED,
    READWRITE,
    REBUILD,
    RECEIVE,
    RECOVERY,
    RECURSIVE_TRIGGERS,
    REGENERATE,
    RELATED_CONVERSATION,
    RELATED_CONVERSATION_GROUP,
    RELATIVE,
    REMOTE,
    REMOTE_PROC_TRANSACTIONS,
    REMOTE_SERVICE_NAME,
    REMOVE,
    REORGANIZE,
    REPAIR_ALLOW_DATA_LOSS,
    REPAIR_FAST,
    REPAIR_REBUILD,
    REPEATABLE,
    REPEATABLEREAD,
    REPLACE,
    REPLICA,
    REQUEST_MAX_CPU_TIME_SEC,
    REQUEST_MAX_MEMORY_GRANT_PERCENT,
    REQUEST_MEMORY_GRANT_TIMEOUT_SEC,
    REQUIRED,
    REQUIRED_SYNCHRONIZED_SECONDARIES_TO_COMMIT,
    RESAMPLE,
    RESERVE_DISK_SPACE,
    RESET,
    RESOURCE,
    RESOURCE_MANAGER_LOCATION,
    RESOURCES,
    RESTART,
    RESTRICTED_USER,
    RESUMABLE,
    RESUME,
    RETAINDAYS,
    RETENTION,
    RETURNS,
    REWIND,
    ROLE,
    ROOT,
    ROUND_ROBIN,
    ROUTE,
    ROW,
    ROWGUID,
    ROWLOCK,
    ROWS,
    RSA_512,
    RSA_1024,
    RSA_2048,
    RSA_3072,
    RSA_4096,
    SAFE,
    SAFETY,
    SAMPLE,
    SCHEDULER,
    SCHEMABINDING,
    SCHEME,
    SCOPED,
    SCRIPT,
    SCROLL,
    SCROLL_LOCKS,
    SEARCH,
    SECONDARY,
    SECONDARY_ONLY,
    SECONDARY_ROLE,
    SECONDS,
    SECRET,
    SECURABLES,
    SECURITY,
    SECURITY_LOG,
    SEEDING_MODE,
    SELF,
    SEMI_SENSITIVE,
    SEND,
    SENT,
    SEQUENCE,
    SEQUENCE_NUMBER,
    SERIALIZABLE,
    SERVER,
    SERVICE,
    SERVICE_BROKER,
    SERVICE_NAME,
    SERVICEBROKER,
    SESSION,
    SESSION_TIMEOUT,
    SETTINGS,
    SHARE,
    SHARED,
    SHOWCONTIG,
    SHOWPLAN,
    SHOWPLAN_ALL,
    SHOWPLAN_TEXT,
    SHOWPLAN_XML,
    SHRINKLOG,
    SID,
    SIGNATURE,
    SINGLE_USER,
    SIZE,
    SKIP_KEYWORD,
    SMALLINT,
    SNAPSHOT,
    SOFTNUMA,
    SORT_IN_TEMPDB,
    SOURCE,
    SP_EXECUTESQL,
    SPARSE,
    SPATIAL_WINDOW_MAX_CELLS,
    SPECIFICATION,
    SPLIT,
    SQL,
    SQLDUMPERFLAGS,
    SQLDUMPERPATH,
    SQLDUMPERTIMEOUT,
    STANDBY,
    START,
    START_DATE,
    STARTED,
    STARTUP_STATE,
    STATE,
    STATIC,
    STATISTICS_INCREMENTAL,
    STATISTICS_NORECOMPUTE,
    STATS,
    STATS_STREAM,
    STATUS,
    STATUSONLY,
    STOP,
    STOP_ON_ERROR,
    STOPLIST,
    STOPPED,
    SUBJECT,
    SUBSCRIBE,
    SUBSCRIPTION,
    SUPPORTED,
    SUSPEND,
    SWITCH,
    SYMMETRIC,
    SYNCHRONOUS_COMMIT,
    SYNONYM,
    SYSTEM,
    TABLE,
    TABLERESULTS,
    TABLOCK,
    TABLOCKX,
    TAKE,
    TAPE,
    TARGET,
    TARGET_RECOVERY_TIME,
    TB,
    TCP,
    TEXTIMAGE_ON,
    THROW,
    TIES,
    TIMEOUT,
    TIMER,
    TINYINT,
    TORN_PAGE_DETECTION,
    TOSTRING,
    TRACE,
    TRACK_CAUSALITY,
    TRACKING,
    TRANSACTION_ID,
    TRANSFER,
    TRANSFORM_NOISE_WORDS,
    TRIPLE_DES,
    TRIPLE_DES_3KEY,
    TRUSTWORTHY,
    TRY,
    TRY_CAST,
    TSQL,
    TWO_DIGIT_YEAR_CUTOFF,
    TYPE,
    TYPE_WARNING,
    UNBOUNDED,
    UNCHECKED,
    UNCOMMITTED,
    UNLIMITED,
    UNLOCK,
    UNMASK,
    UNSAFE,
    UOW,
    UPDLOCK,
    URL,
    USED,
    USING,
    VALID_XML,
    VALIDATION,
    VALUE,
    VAR,
    VERBOSELOGGING,
    VERIFY_CLONEDB,
    VERSION,
    VIEW_METADATA,
    VISIBILITY,
    WAIT,
    WAIT_AT_LOW_PRIORITY,
    WELL_FORMED_XML,
    WINDOWS,
    WITHOUT,
    WITHOUT_ARRAY_WRAPPER,
    WITNESS,
    WORK,
    WORKLOAD,
    XACT_ABORT,
    XLOCK,
    XML,
    XML_COMPRESSION,
    XMLDATA,
    XMLNAMESPACES,
    XMLSCHEMA,
    XSINIL,
    ZONE)
}
