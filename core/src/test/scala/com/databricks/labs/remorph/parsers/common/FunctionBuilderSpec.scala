package com.databricks.labs.remorph.parsers.common

import com.databricks.labs.remorph.parsers.snowflake.{NamedArgumentExpression, SnowflakeFunctionBuilder}
import com.databricks.labs.remorph.parsers.snowflake.SnowflakeFunctionConverters.SynonymOf
import com.databricks.labs.remorph.parsers.tsql.TSqlFunctionBuilder
import com.databricks.labs.remorph.parsers._
import com.databricks.labs.remorph.{intermediate => ir}
import org.scalatest.flatspec.AnyFlatSpec
import org.scalatest.matchers.should.Matchers
import org.scalatest.prop.TableDrivenPropertyChecks

class FunctionBuilderSpec extends AnyFlatSpec with Matchers with TableDrivenPropertyChecks with ir.IRHelpers {

  "TSqlFunctionBuilder" should "return correct arity for each function" in {
    val functions = Table(
      ("functionName", "expectedArity"), // Header

      // TSQL specific
      ("@@CURSOR_ROWS", Some(FunctionDefinition.notConvertible(0))),
      ("@@FETCH_STATUS", Some(FunctionDefinition.notConvertible(0))),
      ("CUBE", Some(FunctionDefinition.standard(1, Int.MaxValue))),
      ("MODIFY", Some(FunctionDefinition.xml(1))),
      ("ROLLUP", Some(FunctionDefinition.standard(1, Int.MaxValue))))

    val functionBuilder = new TSqlFunctionBuilder
    forAll(functions) { (functionName: String, expectedArity: Option[FunctionDefinition]) =>
      functionBuilder.functionDefinition(functionName) shouldEqual expectedArity
    }
  }

  "SnowFlakeFunctionBuilder" should "return correct arity for each function" in {
    val functions = Table(
      ("functionName", "expectedArity"), // Header

      // Snowflake specific
      ("ADD_MONTHS", Some(FunctionDefinition.standard(2))),
      ("ANY_VALUE", Some(FunctionDefinition.standard(1))),
      ("APPROX_TOP_K", Some(FunctionDefinition.standard(1, 3))),
      ("ARRAYS_OVERLAP", Some(FunctionDefinition.standard(2))),
      ("ARRAY_AGG", Some(FunctionDefinition.standard(1))),
      ("ARRAY_APPEND", Some(FunctionDefinition.standard(2))),
      ("ARRAY_CAT", Some(FunctionDefinition.standard(2))),
      ("ARRAY_COMPACT", Some(FunctionDefinition.standard(1))),
      ("ARRAY_CONSTRUCT", Some(FunctionDefinition.standard(0, Int.MaxValue))),
      ("ARRAY_CONSTRUCT_COMPACT", Some(FunctionDefinition.standard(0, Int.MaxValue))),
      ("ARRAY_CONTAINS", Some(FunctionDefinition.standard(2))),
      ("ARRAY_DISTINCT", Some(FunctionDefinition.standard(1))),
      ("ARRAY_EXCEPT", Some(FunctionDefinition.standard(2))),
      ("ARRAY_INSERT", Some(FunctionDefinition.standard(3))),
      ("ARRAY_INTERSECTION", Some(FunctionDefinition.standard(2))),
      ("ARRAY_POSITION", Some(FunctionDefinition.standard(2))),
      ("ARRAY_PREPEND", Some(FunctionDefinition.standard(2))),
      ("ARRAY_REMOVE", Some(FunctionDefinition.standard(2))),
      ("ARRAY_SIZE", Some(FunctionDefinition.standard(1))),
      ("ARRAY_SLICE", Some(FunctionDefinition.standard(3))),
      ("ARRAY_TO_STRING", Some(FunctionDefinition.standard(2))),
      ("ATAN2", Some(FunctionDefinition.standard(2))),
      ("BASE64_DECODE_STRING", Some(FunctionDefinition.standard(1, 2))),
      ("BASE64_ENCODE", Some(FunctionDefinition.standard(1, 3))),
      ("BITOR_AGG", Some(FunctionDefinition.standard(1))),
      ("BOOLAND_AGG", Some(FunctionDefinition.standard(1))),
      ("CEIL", Some(FunctionDefinition.standard(1, 2))),
      ("COLLATE", Some(FunctionDefinition.standard(2))),
      ("COLLATION", Some(FunctionDefinition.standard(1))),
      ("CONTAINS", Some(FunctionDefinition.standard(2))),
      ("CONVERT_TIMEZONE", Some(FunctionDefinition.standard(2, 3))),
      ("CORR", Some(FunctionDefinition.standard(2))),
      ("COUNT_IF", Some(FunctionDefinition.standard(1))),
      ("CURRENT_DATABASE", Some(FunctionDefinition.standard(0))),
      ("CURRENT_TIMESTAMP", Some(FunctionDefinition.standard(0, 1))),
      ("DATEDIFF", Some(FunctionDefinition.standard(3))),
      ("DATE", Some(FunctionDefinition.standard(1, 2).withConversionStrategy(SynonymOf("TO_DATE")))),
      ("DATEFROMPARTS", Some(FunctionDefinition.standard(3).withConversionStrategy(SynonymOf("DATE_FROM_PARTS")))),
      ("DATE_FROM_PARTS", Some(FunctionDefinition.standard(3))),
      ("DATE_PART", Some(FunctionDefinition.standard(2))),
      ("DATE_TRUNC", Some(FunctionDefinition.standard(2))),
      ("DAYNAME", Some(FunctionDefinition.standard(1))),
      ("DECODE", Some(FunctionDefinition.standard(3, Int.MaxValue))),
      ("DENSE_RANK", Some(FunctionDefinition.standard(0))),
      ("DIV0", Some(FunctionDefinition.standard(2))),
      ("DIV0NULL", Some(FunctionDefinition.standard(2))),
      ("EDITDISTANCE", Some(FunctionDefinition.standard(2, 3))),
      ("ENDSWITH", Some(FunctionDefinition.standard(2))),
      ("EQUAL_NULL", Some(FunctionDefinition.standard(2))),
      ("EXTRACT", Some(FunctionDefinition.standard(2))),
      ("FLATTEN", Some(FunctionDefinition.symbolic(Set("INPUT"), Set("PATH", "OUTER", "RECURSIVE", "MODE")))),
      ("GET", Some(FunctionDefinition.standard(2))),
      ("HASH", Some(FunctionDefinition.standard(1, Int.MaxValue))),
      ("HOUR", Some(FunctionDefinition.standard(1))),
      ("IFNULL", Some(FunctionDefinition.standard(1, 2))),
      ("INITCAP", Some(FunctionDefinition.standard(1, 2))),
      ("ISNULL", Some(FunctionDefinition.standard(1))),
      ("IS_INTEGER", Some(FunctionDefinition.standard(1))),
      ("JSON_EXTRACT_PATH_TEXT", Some(FunctionDefinition.standard(2))),
      ("LAST_DAY", Some(FunctionDefinition.standard(1, 2))),
      ("LEFT", Some(FunctionDefinition.standard(2))),
      ("LPAD", Some(FunctionDefinition.standard(2, 3))),
      ("LTRIM", Some(FunctionDefinition.standard(1, 2))),
      ("MEDIAN", Some(FunctionDefinition.standard(1))),
      ("MINUTE", Some(FunctionDefinition.standard(1))),
      ("MOD", Some(FunctionDefinition.standard(2))),
      ("MODE", Some(FunctionDefinition.standard(1))),
      ("MONTHNAME", Some(FunctionDefinition.standard(1))),
      ("NEXT_DAY", Some(FunctionDefinition.standard(2))),
      ("NULLIFZERO", Some(FunctionDefinition.standard(1))),
      ("NTH_VAlUE", Some(FunctionDefinition.standard(2))),
      ("NVL", Some(FunctionDefinition.standard(2).withConversionStrategy(SynonymOf("IFNULL")))),
      ("NVL2", Some(FunctionDefinition.standard(3))),
      ("OBJECT_CONSTRUCT", Some(FunctionDefinition.standard(0, Int.MaxValue))),
      ("OBJECT_KEYS", Some(FunctionDefinition.standard(1))),
      ("PARSE_JSON", Some(FunctionDefinition.standard(1))),
      ("PARSE_URL", Some(FunctionDefinition.standard(1, 2))),
      ("POSITION", Some(FunctionDefinition.standard(2, 3))),
      ("RANDOM", Some(FunctionDefinition.standard(0, 1))),
      ("RANK", Some(FunctionDefinition.standard(0))),
      ("REGEXP_COUNT", Some(FunctionDefinition.standard(2, 4))),
      ("REGEXP_INSTR", Some(FunctionDefinition.standard(2, 7))),
      ("REGEXP_LIKE", Some(FunctionDefinition.standard(2, 3))),
      ("REGEXP_REPLACE", Some(FunctionDefinition.standard(2, 6))),
      ("REGEXP_SUBSTR", Some(FunctionDefinition.standard(2, 6))),
      ("REGR_INTERCEPT", Some(FunctionDefinition.standard(2))),
      ("REGR_R2", Some(FunctionDefinition.standard(2))),
      ("REGR_SLOPE", Some(FunctionDefinition.standard(2))),
      ("REPEAT", Some(FunctionDefinition.standard(2))),
      ("RIGHT", Some(FunctionDefinition.standard(2))),
      ("RLIKE", Some(FunctionDefinition.standard(2, 3))),
      ("ROUND", Some(FunctionDefinition.standard(1, 3))),
      ("RPAD", Some(FunctionDefinition.standard(2, 3))),
      ("RTRIM", Some(FunctionDefinition.standard(1, 2))),
      ("SECOND", Some(FunctionDefinition.standard(1))),
      ("SPLIT_PART", Some(FunctionDefinition.standard(3))),
      ("SQUARE", Some(FunctionDefinition.standard(1))),
      ("STARTSWITH", Some(FunctionDefinition.standard(2))),
      ("STDDEV", Some(FunctionDefinition.standard(1))),
      ("STDDEV_POP", Some(FunctionDefinition.standard(1))),
      ("STDDEV_SAMP", Some(FunctionDefinition.standard(1))),
      ("STRIP_NULL_VALUE", Some(FunctionDefinition.standard(1))),
      ("STRTOK", Some(FunctionDefinition.standard(1, 3))),
      ("STRTOK_TO_ARRAY", Some(FunctionDefinition.standard(1, 2))),
      ("SYSDATE", Some(FunctionDefinition.standard(0))),
      ("TIME", Some(FunctionDefinition.standard(1, 2).withConversionStrategy(SynonymOf("TO_TIME")))),
      ("TIMEADD", Some(FunctionDefinition.standard(3).withConversionStrategy(SynonymOf("DATEADD")))),
      ("TIMESTAMPADD", Some(FunctionDefinition.standard(3))),
      ("TIMESTAMPDIFF", Some(FunctionDefinition.standard(3).withConversionStrategy(SynonymOf("DATEDIFF")))),
      ("TIMESTAMP_FROM_PARTS", Some(FunctionDefinition.standard(2, 8))),
      ("TO_ARRAY", Some(FunctionDefinition.standard(1, 2))),
      ("TO_BOOLEAN", Some(FunctionDefinition.standard(1))),
      ("TO_CHAR", Some(FunctionDefinition.standard(1, 2).withConversionStrategy(SynonymOf("TO_VARCHAR")))),
      ("TO_DATE", Some(FunctionDefinition.standard(1, 2))),
      ("TO_DECIMAL", Some(FunctionDefinition.standard(1, 4).withConversionStrategy(SynonymOf("TO_NUMBER")))),
      ("TO_DOUBLE", Some(FunctionDefinition.standard(1, 2))),
      ("TO_JSON", Some(FunctionDefinition.standard(1))),
      ("TO_NUMBER", Some(FunctionDefinition.standard(1, 4))),
      ("TO_NUMERIC", Some(FunctionDefinition.standard(1, 4).withConversionStrategy(SynonymOf("TO_NUMBER")))),
      ("TO_OBJECT", Some(FunctionDefinition.standard(1))),
      ("TO_TIME", Some(FunctionDefinition.standard(1, 2))),
      ("TO_TIMESTAMP", Some(FunctionDefinition.standard(1, 2))),
      ("TO_TIMESTAMP_LTZ", Some(FunctionDefinition.standard(1, 2))),
      ("TO_TIMESTAMP_NTZ", Some(FunctionDefinition.standard(1, 2))),
      ("TO_TIMESTAMP_TZ", Some(FunctionDefinition.standard(1, 2))),
      ("TO_VARCHAR", Some(FunctionDefinition.standard(1, 2))),
      ("TO_VARIANT", Some(FunctionDefinition.standard(1))),
      ("TRIM", Some(FunctionDefinition.standard(1, 2))),
      ("TRUNC", Some(FunctionDefinition.standard(2))),
      ("TRY_BASE64_DECODE_STRING", Some(FunctionDefinition.standard(1, 2))),
      ("TRY_PARSE_JSON", Some(FunctionDefinition.standard(1))),
      ("TRY_TO_BINARY", Some(FunctionDefinition.standard(1, 2))),
      ("TRY_TO_BOOLEAN", Some(FunctionDefinition.standard(1))),
      ("TRY_TO_DATE", Some(FunctionDefinition.standard(1, 2))),
      ("TRY_TO_DECIMAL", Some(FunctionDefinition.standard(1, 4).withConversionStrategy(SynonymOf("TRY_TO_NUMBER")))),
      ("TRY_TO_DOUBLE", Some(FunctionDefinition.standard(1, 2))),
      ("TRY_TO_NUMBER", Some(FunctionDefinition.standard(1, 4))),
      ("TRY_TO_NUMERIC", Some(FunctionDefinition.standard(1, 4).withConversionStrategy(SynonymOf("TRY_TO_NUMBER")))),
      ("TRY_TO_TIME", Some(FunctionDefinition.standard(1, 2))),
      ("TRY_TO_TIMESTAMP", Some(FunctionDefinition.standard(1, 2))),
      ("TRY_TO_TIMESTAMP_LTZ", Some(FunctionDefinition.standard(1, 2))),
      ("TRY_TO_TIMESTAMP_NTZ", Some(FunctionDefinition.standard(1, 2))),
      ("TRY_TO_TIMESTAMP_TZ", Some(FunctionDefinition.standard(1, 2))),
      ("TYPEOF", Some(FunctionDefinition.standard(1))),
      ("UUID_STRING", Some(FunctionDefinition.standard(0, 2))),
      ("ZEROIFNULL", Some(FunctionDefinition.standard(1))))

    val functionBuilder = new SnowflakeFunctionBuilder
    forAll(functions) { (functionName: String, expectedArity: Option[FunctionDefinition]) =>
      functionBuilder.functionDefinition(functionName) shouldEqual expectedArity
    }
  }

  "FunctionBuilder" should "return correct arity for each function" in {

    val functions = Table(
      ("functionName", "expectedArity"), // Header

      ("ABS", FunctionDefinition.standard(1)),
      ("ACOS", FunctionDefinition.standard(1)),
      ("APPROX_COUNT_DISTINCT", FunctionDefinition.standard(1)),
      ("APPROX_PERCENTILE", FunctionDefinition.standard(2)),
      ("APPROX_PERCENTILE_CONT", FunctionDefinition.standard(1)),
      ("APPROX_PERCENTILE_DISC", FunctionDefinition.standard(1)),
      ("APP_NAME", FunctionDefinition.standard(0)),
      ("APPLOCK_MODE", FunctionDefinition.standard(3)),
      ("APPLOCK_TEST", FunctionDefinition.standard(4)),
      ("ASCII", FunctionDefinition.standard(1)),
      ("ASIN", FunctionDefinition.standard(1)),
      ("ASSEMBLYPROPERTY", FunctionDefinition.standard(2)),
      ("ATAN", FunctionDefinition.standard(1)),
      ("ATN2", FunctionDefinition.standard(2)),
      ("AVG", FunctionDefinition.standard(1)),
      ("BINARY_CHECKSUM", FunctionDefinition.standard(1, Int.MaxValue)),
      ("BIT_COUNT", FunctionDefinition.standard(1)),
      ("CEILING", FunctionDefinition.standard(1)),
      ("CERT_ID", FunctionDefinition.standard(1)),
      ("CERTENCODED", FunctionDefinition.standard(1)),
      ("CERTPRIVATEKEY", FunctionDefinition.standard(2, 3)),
      ("CHAR", FunctionDefinition.standard(1)),
      ("CHARINDEX", FunctionDefinition.standard(2, 3)),
      ("CHECKSUM", FunctionDefinition.standard(2, Int.MaxValue)),
      ("CHECKSUM_AGG", FunctionDefinition.standard(1)),
      ("COALESCE", FunctionDefinition.standard(1, Int.MaxValue)),
      ("COL_LENGTH", FunctionDefinition.standard(2)),
      ("COL_NAME", FunctionDefinition.standard(2)),
      ("COLUMNPROPERTY", FunctionDefinition.standard(3)),
      ("COMPRESS", FunctionDefinition.standard(1)),
      ("CONCAT", FunctionDefinition.standard(2, Int.MaxValue)),
      ("CONCAT_WS", FunctionDefinition.standard(3, Int.MaxValue)),
      ("CONNECTIONPROPERTY", FunctionDefinition.notConvertible(1)),
      ("CONTEXT_INFO", FunctionDefinition.standard(0)),
      ("CONVERT", FunctionDefinition.standard(2, 3)),
      ("COS", FunctionDefinition.standard(1)),
      ("COT", FunctionDefinition.standard(1)),
      ("COUNT", FunctionDefinition.standard(1)),
      ("COUNT_BIG", FunctionDefinition.standard(1)),
      ("CUME_DIST", FunctionDefinition.standard(0)),
      ("CURRENT_DATE", FunctionDefinition.standard(0)),
      ("CURRENT_REQUEST_ID", FunctionDefinition.standard(0)),
      ("CURRENT_TIMESTAMP", FunctionDefinition.standard(0)),
      ("CURRENT_TIMEZONE", FunctionDefinition.standard(0)),
      ("CURRENT_TIMEZONE_ID", FunctionDefinition.standard(0)),
      ("CURRENT_TRANSACTION_ID", FunctionDefinition.standard(0)),
      ("CURRENT_USER", FunctionDefinition.standard(0)),
      ("CURSOR_ROWS", FunctionDefinition.standard(0)),
      ("CURSOR_STATUS", FunctionDefinition.standard(2)),
      ("DATABASE_PRINCIPAL_ID", FunctionDefinition.standard(0, 1)),
      ("DATABASEPROPERTY", FunctionDefinition.standard(2)),
      ("DATABASEPROPERTYEX", FunctionDefinition.standard(2)),
      ("DATALENGTH", FunctionDefinition.standard(1)),
      ("DATE_BUCKET", FunctionDefinition.standard(3, 4)),
      ("DATE_DIFF_BIG", FunctionDefinition.standard(3)),
      ("DATEADD", FunctionDefinition.standard(3)),
      ("DATEDIFF", FunctionDefinition.standard(3)),
      ("DATEFROMPARTS", FunctionDefinition.standard(3)),
      ("DATENAME", FunctionDefinition.standard(2)),
      ("DATEPART", FunctionDefinition.standard(2)),
      ("DATETIME2FROMPARTS", FunctionDefinition.standard(8)),
      ("DATETIMEFROMPARTS", FunctionDefinition.standard(7)),
      ("DATETIMEOFFSETFROMPARTS", FunctionDefinition.standard(10)),
      ("DATETRUNC", FunctionDefinition.standard(2)),
      ("DAY", FunctionDefinition.standard(1)),
      ("DB_ID", FunctionDefinition.standard(0, 1)),
      ("DB_NAME", FunctionDefinition.standard(0, 1)),
      ("DECOMPRESS", FunctionDefinition.standard(1)),
      ("DEGREES", FunctionDefinition.standard(1)),
      ("DENSE_RANK", FunctionDefinition.standard(0)),
      ("DIFFERENCE", FunctionDefinition.standard(2)),
      ("EOMONTH", FunctionDefinition.standard(1, 2)),
      ("ERROR_LINE", FunctionDefinition.standard(0)),
      ("ERROR_MESSAGE", FunctionDefinition.standard(0)),
      ("ERROR_NUMBER", FunctionDefinition.standard(0)),
      ("ERROR_PROCEDURE", FunctionDefinition.standard(0)),
      ("ERROR_SEVERITY", FunctionDefinition.standard(0)),
      ("ERROR_STATE", FunctionDefinition.standard(0)),
      ("EXIST", FunctionDefinition.xml(1)),
      ("EXP", FunctionDefinition.standard(1)),
      ("FILE_ID", FunctionDefinition.standard(1)),
      ("FILE_IDEX", FunctionDefinition.standard(1)),
      ("FILE_NAME", FunctionDefinition.standard(1)),
      ("FILEGROUP_ID", FunctionDefinition.standard(1)),
      ("FILEGROUP_NAME", FunctionDefinition.standard(1)),
      ("FILEGROUPPROPERTY", FunctionDefinition.standard(2)),
      ("FILEPROPERTY", FunctionDefinition.standard(2)),
      ("FILEPROPERTYEX", FunctionDefinition.standard(2)),
      ("FIRST_VALUE", FunctionDefinition.standard(1)),
      ("FLOOR", FunctionDefinition.standard(1)),
      ("FORMAT", FunctionDefinition.standard(2, 3)),
      ("FORMATMESSAGE", FunctionDefinition.standard(2, Int.MaxValue)),
      ("FULLTEXTCATALOGPROPERTY", FunctionDefinition.standard(2)),
      ("FULLTEXTSERVICEPROPERTY", FunctionDefinition.standard(1)),
      ("GET_FILESTREAM_TRANSACTION_CONTEXT", FunctionDefinition.standard(0)),
      ("GETANCESTGOR", FunctionDefinition.standard(1)),
      ("GETANSINULL", FunctionDefinition.standard(0, 1)),
      ("GETDATE", FunctionDefinition.standard(0)),
      ("GETDESCENDANT", FunctionDefinition.standard(2)),
      ("GETLEVEL", FunctionDefinition.standard(0)),
      ("GETREPARENTEDVALUE", FunctionDefinition.standard(2)),
      ("GETUTCDATE", FunctionDefinition.standard(0)),
      ("GREATEST", FunctionDefinition.standard(1, Int.MaxValue)),
      ("GROUPING", FunctionDefinition.standard(1)),
      ("GROUPING_ID", FunctionDefinition.standard(0, Int.MaxValue)),
      ("HAS_DBACCESS", FunctionDefinition.standard(1)),
      ("HAS_PERMS_BY_NAME", FunctionDefinition.standard(4, 5)),
      ("HOST_ID", FunctionDefinition.standard(0)),
      ("HOST_NAME", FunctionDefinition.standard(0)),
      ("IDENT_CURRENT", FunctionDefinition.standard(1)),
      ("IDENT_INCR", FunctionDefinition.standard(1)),
      ("IDENT_SEED", FunctionDefinition.standard(1)),
      ("IDENTITY", FunctionDefinition.standard(1, 3)),
      ("IFF", FunctionDefinition.standard(3)),
      ("INDEX_COL", FunctionDefinition.standard(3)),
      ("INDEXKEY_PROPERTY", FunctionDefinition.standard(3)),
      ("INDEXPROPERTY", FunctionDefinition.standard(3)),
      ("IS_MEMBER", FunctionDefinition.standard(1)),
      ("IS_ROLEMEMBER", FunctionDefinition.standard(1, 2)),
      ("IS_SRVROLEMEMBER", FunctionDefinition.standard(1, 2)),
      ("ISDATE", FunctionDefinition.standard(1)),
      ("ISDESCENDANTOF", FunctionDefinition.standard(1)),
      ("ISJSON", FunctionDefinition.standard(1, 2)),
      ("ISNUMERIC", FunctionDefinition.standard(1)),
      ("JSON_MODIFY", FunctionDefinition.standard(3)),
      ("JSON_PATH_EXISTS", FunctionDefinition.standard(2)),
      ("JSON_QUERY", FunctionDefinition.standard(2)),
      ("JSON_VALUE", FunctionDefinition.standard(2)),
      ("LAG", FunctionDefinition.standard(1, 3)),
      ("LAST_VALUE", FunctionDefinition.standard(1)),
      ("LEAD", FunctionDefinition.standard(1, 3)),
      ("LEAST", FunctionDefinition.standard(1, Int.MaxValue)),
      ("LEFT", FunctionDefinition.standard(2)),
      ("LEN", FunctionDefinition.standard(1)),
      ("LOG", FunctionDefinition.standard(1, 2)),
      ("LOG10", FunctionDefinition.standard(1)),
      ("LOGINPROPERTY", FunctionDefinition.standard(2)),
      ("LOWER", FunctionDefinition.standard(1)),
      ("LTRIM", FunctionDefinition.standard(1)),
      ("MAX", FunctionDefinition.standard(1)),
      ("MIN", FunctionDefinition.standard(1)),
      ("MIN_ACTIVE_ROWVERSION", FunctionDefinition.standard(0)),
      ("MONTH", FunctionDefinition.standard(1)),
      ("NCHAR", FunctionDefinition.standard(1)),
      ("NEWID", FunctionDefinition.standard(0)),
      ("NEWSEQUENTIALID", FunctionDefinition.standard(0)),
      ("NODES", FunctionDefinition.xml(1)),
      ("NTILE", FunctionDefinition.standard(1)),
      ("NULLIF", FunctionDefinition.standard(2)),
      ("OBJECT_DEFINITION", FunctionDefinition.standard(1)),
      ("OBJECT_ID", FunctionDefinition.standard(1, 2)),
      ("OBJECT_NAME", FunctionDefinition.standard(1, 2)),
      ("OBJECT_SCHEMA_NAME", FunctionDefinition.standard(1, 2)),
      ("OBJECTPROPERTY", FunctionDefinition.standard(2)),
      ("OBJECTPROPERTYEX", FunctionDefinition.standard(2)),
      ("ORIGINAL_DB_NAME", FunctionDefinition.standard(0)),
      ("ORIGINAL_LOGIN", FunctionDefinition.standard(0)),
      ("PARSE", FunctionDefinition.notConvertible(2, 3)),
      ("PARSENAME", FunctionDefinition.standard(2)),
      ("PATINDEX", FunctionDefinition.standard(2)),
      ("PERCENTILE_CONT", FunctionDefinition.standard(1)),
      ("PERCENTILE_DISC", FunctionDefinition.standard(1)),
      ("PERMISSIONS", FunctionDefinition.notConvertible(0, 2)),
      ("PI", FunctionDefinition.standard(0)),
      ("POWER", FunctionDefinition.standard(2)),
      ("PWDCOMPARE", FunctionDefinition.standard(2, 3)),
      ("PWDENCRYPT", FunctionDefinition.standard(1)),
      ("QUERY", FunctionDefinition.xml(1)),
      ("QUOTENAME", FunctionDefinition.standard(1, 2)),
      ("RADIANS", FunctionDefinition.standard(1)),
      ("RAND", FunctionDefinition.standard(0, 1)),
      ("RANK", FunctionDefinition.standard(0)),
      ("REPLACE", FunctionDefinition.standard(3)),
      ("REPLICATE", FunctionDefinition.standard(2)),
      ("REVERSE", FunctionDefinition.standard(1)),
      ("RIGHT", FunctionDefinition.standard(2)),
      ("ROUND", FunctionDefinition.standard(1, 3)),
      ("ROW_NUMBER", FunctionDefinition.standard(0)),
      ("ROWCOUNT_BIG", FunctionDefinition.standard(0)),
      ("RTRIM", FunctionDefinition.standard(1)),
      ("SCHEMA_ID", FunctionDefinition.standard(0, 1)),
      ("SCHEMA_NAME", FunctionDefinition.standard(0, 1)),
      ("SCOPE_IDENTITY", FunctionDefinition.standard(0)),
      ("SERVERPROPERTY", FunctionDefinition.standard(1)),
      ("SESSION_CONTEXT", FunctionDefinition.standard(1, 2)),
      ("SESSION_USER", FunctionDefinition.standard(0)),
      ("SESSIONPROPERTY", FunctionDefinition.standard(1)),
      ("SIGN", FunctionDefinition.standard(1)),
      ("SIN", FunctionDefinition.standard(1)),
      ("SMALLDATETIMEFROMPARTS", FunctionDefinition.standard(5)),
      ("SOUNDEX", FunctionDefinition.standard(1)),
      ("SPACE", FunctionDefinition.standard(1)),
      ("SQL_VARIANT_PROPERTY", FunctionDefinition.standard(2)),
      ("SQRT", FunctionDefinition.standard(1)),
      ("SQUARE", FunctionDefinition.standard(1)),
      ("STATS_DATE", FunctionDefinition.standard(2)),
      ("STDEV", FunctionDefinition.standard(1)),
      ("STDEVP", FunctionDefinition.standard(1)),
      ("STR", FunctionDefinition.standard(1, 3)),
      ("STRING_AGG", FunctionDefinition.standard(2, 3)),
      ("STRING_ESCAPE", FunctionDefinition.standard(2)),
      ("STUFF", FunctionDefinition.standard(4)),
      ("SUBSTR", FunctionDefinition.standard(2, 3)),
      ("SUBSTRING", FunctionDefinition.standard(2, 3)),
      ("SUM", FunctionDefinition.standard(1)),
      ("SUSER_ID", FunctionDefinition.standard(0, 1)),
      ("SUSER_NAME", FunctionDefinition.standard(0, 1)),
      ("SUSER_SID", FunctionDefinition.standard(0, 2)),
      ("SUSER_SNAME", FunctionDefinition.standard(0, 1)),
      ("SWITCHOFFSET", FunctionDefinition.standard(2)),
      ("SYSDATETIME", FunctionDefinition.standard(0)),
      ("SYSDATETIMEOFFSET", FunctionDefinition.standard(0)),
      ("SYSTEM_USER", FunctionDefinition.standard(0)),
      ("SYSUTCDATETIME", FunctionDefinition.standard(0)),
      ("TAN", FunctionDefinition.standard(1)),
      ("TIMEFROMPARTS", FunctionDefinition.standard(5)),
      ("TODATETIMEOFFSET", FunctionDefinition.standard(2)),
      ("TOSTRING", FunctionDefinition.standard(0)),
      ("TRANSLATE", FunctionDefinition.standard(3)),
      ("TRIM", FunctionDefinition.standard(1, 2)),
      ("TYPE_ID", FunctionDefinition.standard(1)),
      ("TYPE_NAME", FunctionDefinition.standard(1)),
      ("TYPEPROPERTY", FunctionDefinition.standard(2)),
      ("UNICODE", FunctionDefinition.standard(1)),
      ("UPPER", FunctionDefinition.standard(1)),
      ("USER", FunctionDefinition.standard(0)),
      ("USER_ID", FunctionDefinition.standard(0, 1)),
      ("USER_NAME", FunctionDefinition.standard(0, 1)),
      ("VALUE", FunctionDefinition.xml(2)),
      ("VAR", FunctionDefinition.standard(1)),
      ("VARP", FunctionDefinition.standard(1)),
      ("XACT_STATE", FunctionDefinition.standard(0)),
      ("YEAR", FunctionDefinition.standard(1)))

    val functionBuilder = new TSqlFunctionBuilder

    forAll(functions) { (functionName: String, expectedArity: FunctionDefinition) =>
      {
        val actual = functionBuilder.functionDefinition(functionName)
        actual.nonEmpty shouldEqual true
        actual.map(_.arity) shouldEqual Some(expectedArity.arity)
      }
    }
  }

  "functionType" should "return correct function type for each TSQL function" in {
    val functions = Table(
      ("functionName", "expectedFunctionType"), // Header

      // This table needs to maintain an example of all types of functions in Arity and FunctionType
      // However, it is not necessary to test all functions, just one of each type.
      // However, note that there are no XML functions with VariableArity at the moment.
      ("MODIFY", XmlFunction),
      ("ABS", StandardFunction),
      ("VALUE", XmlFunction),
      ("CONCAT", StandardFunction),
      ("TRIM", StandardFunction))

    // Test all FunctionType combinations that currently exist
    val functionBuilder = new TSqlFunctionBuilder

    forAll(functions) { (functionName: String, expectedFunctionType: FunctionType) =>
      {
        functionBuilder.functionType(functionName) shouldEqual expectedFunctionType
      }
    }
  }

  "functionType" should "return UnknownFunction for tsql functions that do not exist" in {
    val functionBuilder = new TSqlFunctionBuilder
    val result = functionBuilder.functionType("DOES_NOT_EXIST")
    result shouldEqual UnknownFunction
  }

  "isConvertible method in FunctionArity" should "return true by default" in {
    val fixedArity = FunctionDefinition.standard(1)
    fixedArity.functionType should not be NotConvertibleFunction

    val variableArity = FunctionDefinition.standard(1, 2)
    variableArity should not be NotConvertibleFunction

  }

  "buildFunction" should "remove quotes and brackets from function names" in {
    val functionBuilder = new TSqlFunctionBuilder

    val quoteTable = Table(
      ("functionName", "expectedFunctionName"), // Header

      ("a", "a"), // Test function name with less than 2 characters
      ("'quoted'", "quoted"), // Test function name with matching quotes
      ("[bracketed]", "bracketed"), // Test function name with matching brackets
      ("\\backslashed\\", "backslashed"), // Test function name with matching backslashes
      ("\"doublequoted\"", "doublequoted") // Test function name with non-matching quotes
    )
    forAll(quoteTable) { (functionName: String, expectedFunctionName: String) =>
      {
        val r = functionBuilder.buildFunction(functionName, List.empty)
        r match {
          case f: ir.UnresolvedFunction => f.function_name shouldBe expectedFunctionName
          case _ => fail("Unexpected function type")
        }
      }
    }
  }

  "buildFunction" should "Apply known TSql conversion strategies" in {
    val functionBuilder = new TSqlFunctionBuilder

    val renameTable = Table(
      ("functionName", "params", "expectedFunctionName"), // Header

      ("ISNULL", Seq(simplyNamedColumn("x"), ir.Literal(1)), "IFNULL"),
      ("GET_BIT", Seq(simplyNamedColumn("x"), ir.Literal(1)), "GETBIT"),
      ("left_SHIFT", Seq(simplyNamedColumn("x"), ir.Literal(1)), "LEFTSHIFT"),
      ("RIGHT_SHIFT", Seq(simplyNamedColumn("x"), ir.Literal(1)), "RIGHTSHIFT"))

    forAll(renameTable) { (functionName: String, params: Seq[ir.Expression], expectedFunctionName: String) =>
      {
        val r = functionBuilder.buildFunction(functionName, params)
        r match {
          case f: ir.CallFunction => f.function_name shouldBe expectedFunctionName
          case _ => fail("Unexpected function type")
        }
      }
    }
  }

  "buildFunction" should "not resolve IFNULL when child dialect isn't TSql" in {
    val functionBuilder = new SnowflakeFunctionBuilder

    val result1 = functionBuilder.buildFunction("ISNULL", Seq(simplyNamedColumn("x"), ir.Literal(0)))
    result1 shouldBe a[ir.UnresolvedFunction]
  }

  "buildFunction" should "not resolve IFNULL when child dialect isn't Snowflake" in {
    val functionBuilder = new TSqlFunctionBuilder

    val result1 = functionBuilder.buildFunction("IFNULL", Seq(simplyNamedColumn("x"), ir.Literal(0)))
    result1 shouldBe a[ir.UnresolvedFunction]
  }

  "buildFunction" should "Should preserve case if it can" in {
    val functionBuilder = new TSqlFunctionBuilder
    val result1 = functionBuilder.buildFunction("isnull", Seq(simplyNamedColumn("x"), ir.Literal(0)))
    result1 match {
      case f: ir.CallFunction => f.function_name shouldBe "ifnull"
      case _ => fail("ifnull conversion failed")
    }
  }

  "FunctionRename strategy" should "preserve original function if no match is found" in {
    val functionBuilder = new TSqlFunctionBuilder
    val result1 = functionBuilder.applyConversionStrategy(FunctionDefinition.standard(1), Seq(ir.Literal(66)), "Abs")
    result1 match {
      case f: ir.CallFunction => f.function_name shouldBe "Abs"
      case _ => fail("UNKNOWN_FUNCTION conversion failed")
    }
  }

  "FunctionArity.verifyArguments" should "return true when arity is fixed and provided number of arguments matches" in {
    FunctionArity.verifyArguments(FixedArity(0), Seq()) shouldBe true
    FunctionArity.verifyArguments(FixedArity(1), Seq(ir.Noop)) shouldBe true
    FunctionArity.verifyArguments(FixedArity(2), Seq(ir.Noop, ir.Noop)) shouldBe true
  }

  "FunctionArity.verifyArguments" should
    "return true when arity is varying and provided number of arguments matches" in {
      FunctionArity.verifyArguments(VariableArity(0, 2), Seq()) shouldBe true
      FunctionArity.verifyArguments(VariableArity(0, 2), Seq(ir.Noop)) shouldBe true
      FunctionArity.verifyArguments(VariableArity(0, 2), Seq(ir.Noop, ir.Noop)) shouldBe true
    }

  "FunctionArity.verifyArguments" should "return true when arity is symbolic and arguments are provided named" in {
    val arity = SymbolicArity(Set("req1", "REQ2"), Set("opt1", "opt2", "opt3"))
    FunctionArity.verifyArguments(
      arity,
      Seq(NamedArgumentExpression("Req2", ir.Noop), snowflake.NamedArgumentExpression("REQ1", ir.Noop))) shouldBe true

    FunctionArity.verifyArguments(
      arity,
      Seq(
        snowflake.NamedArgumentExpression("Req2", ir.Noop),
        snowflake.NamedArgumentExpression("OPT1", ir.Noop),
        snowflake.NamedArgumentExpression("REQ1", ir.Noop))) shouldBe true

    FunctionArity.verifyArguments(
      arity,
      Seq(
        snowflake.NamedArgumentExpression("Req2", ir.Noop),
        snowflake.NamedArgumentExpression("OPT1", ir.Noop),
        snowflake.NamedArgumentExpression("OPT3", ir.Noop),
        snowflake.NamedArgumentExpression("OPT2", ir.Noop),
        snowflake.NamedArgumentExpression("REQ1", ir.Noop))) shouldBe true
  }

  "FunctionArity.verifyArguments" should "return true when arity is symbolic and arguments are provided unnamed" in {
    val arity = SymbolicArity(Set("req1", "REQ2"), Set("opt1", "opt2", "opt3"))

    FunctionArity.verifyArguments(arity, Seq( /*REQ1*/ ir.Noop, /*REQ2*/ ir.Noop)) shouldBe true
    FunctionArity.verifyArguments(arity, Seq( /*REQ1*/ ir.Noop, /*REQ2*/ ir.Noop, /*OPT1*/ ir.Noop)) shouldBe true
    FunctionArity.verifyArguments(
      arity,
      Seq( /*REQ1*/ ir.Noop, /*REQ2*/ ir.Noop, /*OPT1*/ ir.Noop, /*OPT2*/ ir.Noop)) shouldBe true
    FunctionArity.verifyArguments(
      arity,
      Seq( /*REQ1*/ ir.Noop, /*REQ2*/ ir.Noop, /*OPT1*/ ir.Noop, /*OPT2*/ ir.Noop, /*OPT3*/ ir.Noop)) shouldBe true
  }

  "FunctionArity.verifyArguments" should "return false otherwise" in {
    // not enough arguments
    FunctionArity.verifyArguments(FixedArity(1), Seq.empty) shouldBe false
    FunctionArity.verifyArguments(VariableArity(2, 3), Seq(ir.Noop)) shouldBe false
    FunctionArity.verifyArguments(
      SymbolicArity(Set("req1", "req2"), Set.empty),
      Seq(snowflake.NamedArgumentExpression("REQ2", ir.Noop))) shouldBe false
    FunctionArity.verifyArguments(SymbolicArity(Set("req1", "req2"), Set.empty), Seq(ir.Noop)) shouldBe false

    // too many arguments
    FunctionArity.verifyArguments(FixedArity(0), Seq(ir.Noop)) shouldBe false
    FunctionArity.verifyArguments(VariableArity(0, 1), Seq(ir.Noop, ir.Noop)) shouldBe false
    FunctionArity.verifyArguments(
      SymbolicArity(Set("req1", "req2"), Set.empty),
      Seq(ir.Noop, ir.Noop, ir.Noop)) shouldBe false

    // wrongly named arguments
    FunctionArity.verifyArguments(
      SymbolicArity(Set("req1"), Set("opt1")),
      Seq(
        snowflake.NamedArgumentExpression("REQ2", ir.Noop),
        snowflake.NamedArgumentExpression("REQ1", ir.Noop))) shouldBe false

    // mix of named and unnamed arguments
    FunctionArity.verifyArguments(
      SymbolicArity(Set("REQ"), Set("OPT")),
      Seq(ir.Noop, snowflake.NamedArgumentExpression("OPT", ir.Noop))) shouldBe false
  }
}
