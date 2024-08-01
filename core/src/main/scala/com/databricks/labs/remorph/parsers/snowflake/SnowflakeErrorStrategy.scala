package com.databricks.labs.remorph.parsers.snowflake

import com.databricks.labs.remorph.parsers.SqlErrorStrategy
import com.databricks.labs.remorph.parsers.snowflake.SnowflakeParser._
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
class SnowflakeErrorStrategy extends SqlErrorStrategy {

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
      SnowflakeErrorStrategy.ruleTranslation.get(methodName).foreach { translatedMessage =>
        // Only mention a batch if we have recovered all the way to the top rule
        val shouldAppend = if (methodName == "snowflakeFile" || methodName == "batch") {
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
      val tokenString = SnowflakeErrorStrategy.tokenTranslation.get(tokenId) match {
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
    set.subtract(SnowflakeErrorStrategy.keywordIDs)
  }
}

object SnowflakeErrorStrategy {

  // A map that will override the default display name for tokens that represent text with
  // pattern matches like IDENTIFIER, STRING, etc.
  private val tokenTranslation: Map[Int, String] = Map(
    DOUBLE_QUOTE_ID -> "Identifier",
    FLOAT -> "Float",
    ID -> "Identifier",
    ID2 -> "$Identifier",
    REAL -> "Real",
    STRING -> "'String'",
    DATE_LIT -> "Date literal",
    TIMESTAMP_LIT -> "Timestamp literal",
    DECIMAL -> "Decimal integer",
    FLOAT -> "Floating point number",
    REAL -> "Real number",
    -1 -> "End of batch",

    // When the next thing we expect can be every statement, we just say "statement"
    ALTER -> "Statement",
    BEGIN -> "Statement",
    COMMIT -> "Statement",
    CONTINUE -> "Statement",
    COPY -> "Statement",
    CREATE -> "Statement",
    DELETE -> "Statement",
    DESCRIBE -> "Statement",
    DROP -> "Statement",
    END -> "Statement",
    EXECUTE -> "Statement",
    EXPLAIN -> "Statement",
    FETCH -> "Statement",
    GRANT -> "Statement",
    IF -> "Statement",
    INSERT -> "Statement",
    LIST -> "Statement",
    MERGE -> "Statement",
    PUT -> "Statement",
    REMOVE -> "Statement",
    REVOKE -> "Statement",
    ROLLBACK -> "Statement",
    SELECT -> "Select Statement",
    SET -> "Statement",
    SHOW -> "Statement",
    TRUNCATE -> "Statement",
    UNDROP -> "Statement",
    UNSET -> "Statement",
    UPDATE -> "Statement",
    USE -> "Statement",
    WITHIN -> "Statement",

    // No need to distinguish between operators

    PIPE_PIPE -> "Operator",
    EQ -> "Operator",
    GT -> "Operator",
    GE -> "Operator",
    LT -> "Operator",
    LTGT -> "Operator",
    LE -> "Operator",
    STAR -> "Operator",
    DIVIDE -> "Operator",
    TILDA -> "Operator",
    NE -> "Operator",
    MINUS -> "Operator",
    PLUS -> "Operator")

  private val ruleTranslation: Map[String, String] = Map(
    "alterCommand" -> "ALTER command",
    "batch" -> "Snowflake batch",
    "beginTxn" -> "BEGIN WORK | TRANSACTION statement",
    "copyIntoTable" -> "COPY statement",
    "ddlObject" -> "TABLE object",
    "executeImmediate" -> "EXECUTE command",
    "explain" -> "EXPLAIN command",
    "groupByClause" -> "GROUP BY clause",
    "havingClause" -> "HAVING clause",
    "insertMultiTableStatement" -> "INSERT statement",
    "insertStatement" -> "INSERT statement",
    "joinClause" -> "JOIN clause",
    "limitClause" -> "LIMIT clause",
    "mergeStatement" -> "MERGE statement",
    "objectRef" -> "Object reference",
    "offsetClause" -> "OFFSET clause",
    "orderByClause" -> "ORDER BY clause",
    "otherCommand" -> "SQL command",
    "outputClause" -> "OUTPUT clause",
    "selectList" -> "SELECT list",
    "selectStatement" -> "SELECT statement",
    "snowflakeFile" -> "Snowflake batch",
    "topClause" -> "TOP clause",
    "update" -> "UPDATE statement",
    "updateElem" -> "UPDATE element specification",
    "updateStatement" -> "UPDATE statement",
    "updateStatement" -> "UPDATE statement",
    "updateWhereClause" -> "WHERE clause",
    "whereClause" -> "WHERE clause",
    "withTableHints" -> "WITH table hints",
    // Etc

    "tableSource" -> "table source",
    "tableSourceItem" -> "table source")

  private val keywordIDs: IntervalSet = new IntervalSet(
    ACCOUNTADMIN,
    ACTION,
    ACTION,
    AES,
    ALERT,
    ARRAY,
    ARRAY_AGG,
    AT_KEYWORD,
    CHECKSUM,
    CLUSTER,
    COLLATE,
    COLLECTION,
    COMMENT,
    CONDITION,
    CONFIGURATION,
    COPY_OPTIONS_,
    DATA,
    DATE,
    DATE_FORMAT,
    DEFINITION,
    DELTA,
    DENSE_RANK,
    DIRECTION,
    DOWNSTREAM,
    DUMMY,
    DYNAMIC,
    EDITION,
    END,
    EMAIL,
    EVENT,
    EXCHANGE,
    EXPIRY_DATE,
    FIRST,
    FIRST_NAME,
    FLATTEN,
    FLOOR,
    FUNCTION,
    GET,
    GLOBAL,
    IDENTIFIER,
    IDENTITY,
    IF,
    INDEX,
    INPUT,
    INTERVAL,
    JAVASCRIPT,
    KEY,
    KEYS,
    LANGUAGE,
    LAST_NAME,
    LAST_QUERY_ID,
    LEAD,
    LENGTH,
    LOCAL,
    MAX_CONCURRENCY_LEVEL,
    MODE,
    NAME,
    NETWORK,
    NOORDER,
    OFFSET,
    OPTION,
    ORDER,
    ORGADMIN,
    OUTBOUND,
    OUTER,
    PARTITION,
    PATH_,
    PATTERN,
    PORT,
    PROCEDURE_NAME,
    PROPERTY,
    PROVIDER,
    PUBLIC,
    RANK,
    RECURSIVE,
    REGION,
    REPLACE,
    RESOURCE,
    RESOURCES,
    RESPECT,
    RESTRICT,
    RESULT,
    RLIKE,
    ROLE,
    ROLLUP,
    SECURITYADMIN,
    SHARES,
    SOURCE,
    STAGE,
    START,
    STATE,
    STATS,
    SYSADMIN,
    TABLE,
    TAG,
    TAGS,
    TARGET_LAG,
    TEMP,
    TIME,
    TIMESTAMP,
    TIMEZONE,
    TYPE,
    URL,
    USER,
    USERADMIN,
    VALUE,
    VALUES,
    VERSION,
    WAREHOUSE,
    WAREHOUSE_TYPE)
}
