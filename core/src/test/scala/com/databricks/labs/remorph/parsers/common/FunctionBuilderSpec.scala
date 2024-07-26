package com.databricks.labs.remorph.parsers.common

import com.databricks.labs.remorph.parsers.intermediate.{IRHelpers, UnresolvedFunction}
import com.databricks.labs.remorph.parsers.snowflake.{NamedArgumentExpression, SnowflakeFunctionBuilder}
import com.databricks.labs.remorph.parsers.snowflake.SnowflakeFunctionConverters.SnowflakeSynonyms
import com.databricks.labs.remorph.parsers.tsql.TSqlFunctionBuilder
import com.databricks.labs.remorph.parsers.{snowflake, intermediate => ir, _}
import org.scalatest.flatspec.AnyFlatSpec
import org.scalatest.matchers.should.Matchers
import org.scalatest.prop.TableDrivenPropertyChecks

class FunctionBuilderSpec extends AnyFlatSpec with Matchers with TableDrivenPropertyChecks with IRHelpers {

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
      ("DATE", Some(FunctionDefinition.standard(1, 2).withConversionStrategy(SnowflakeSynonyms))),
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
      ("NVL", Some(FunctionDefinition.standard(2))),
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
      ("TIME", Some(FunctionDefinition.standard(1, 2).withConversionStrategy(SnowflakeSynonyms))),
      ("TIMEADD", Some(FunctionDefinition.standard(3))),
      ("TIMESTAMPADD", Some(FunctionDefinition.standard(3))),
      ("TIMESTAMPDIFF", Some(FunctionDefinition.standard(3))),
      ("TIMESTAMP_FROM_PARTS", Some(FunctionDefinition.standard(2, 8))),
      ("TO_ARRAY", Some(FunctionDefinition.standard(1))),
      ("TO_BOOLEAN", Some(FunctionDefinition.standard(1))),
      ("TO_CHAR", Some(FunctionDefinition.standard(1, 2).withConversionStrategy(SnowflakeSynonyms))),
      ("TO_DATE", Some(FunctionDefinition.standard(1, 2))),
      ("TO_DECIMAL", Some(FunctionDefinition.standard(1, 4))),
      ("TO_DOUBLE", Some(FunctionDefinition.standard(1, 2))),
      ("TO_JSON", Some(FunctionDefinition.standard(1))),
      ("TO_NUMBER", Some(FunctionDefinition.standard(1, 4))),
      ("TO_NUMERIC", Some(FunctionDefinition.standard(1, 4))),
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
      ("TRY_TO_DECIMAL", Some(FunctionDefinition.standard(1, 4))),
      ("TRY_TO_DOUBLE", Some(FunctionDefinition.standard(1, 2))),
      ("TRY_TO_NUMBER", Some(FunctionDefinition.standard(1, 4))),
      ("TRY_TO_NUMERIC", Some(FunctionDefinition.standard(1, 4))),
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

      ("ABS", Some(FunctionDefinition.standard(1))),
      ("ACOS", Some(FunctionDefinition.standard(1))),
      ("APPROX_COUNT_DISTINCT", Some(FunctionDefinition.standard(1))),
      ("APPROX_PERCENTILE", Some(FunctionDefinition.standard(2))),
      ("APPROX_PERCENTILE_CONT", Some(FunctionDefinition.standard(1))),
      ("APPROX_PERCENTILE_DISC", Some(FunctionDefinition.standard(1))),
      ("APP_NAME", Some(FunctionDefinition.standard(0))),
      ("APPLOCK_MODE", Some(FunctionDefinition.standard(3))),
      ("APPLOCK_TEST", Some(FunctionDefinition.standard(4))),
      ("ASCII", Some(FunctionDefinition.standard(1))),
      ("ASIN", Some(FunctionDefinition.standard(1))),
      ("ASSEMBLYPROPERTY", Some(FunctionDefinition.standard(2))),
      ("ATAN", Some(FunctionDefinition.standard(1))),
      ("ATN2", Some(FunctionDefinition.standard(2))),
      ("AVG", Some(FunctionDefinition.standard(1))),
      ("BINARY_CHECKSUM", Some(FunctionDefinition.standard(1, Int.MaxValue))),
      ("BIT_COUNT", Some(FunctionDefinition.standard(1))),
      ("CEILING", Some(FunctionDefinition.standard(1))),
      ("CERT_ID", Some(FunctionDefinition.standard(1))),
      ("CERTENCODED", Some(FunctionDefinition.standard(1))),
      ("CERTPRIVATEKEY", Some(FunctionDefinition.standard(2, 3))),
      ("CHAR", Some(FunctionDefinition.standard(1))),
      ("CHARINDEX", Some(FunctionDefinition.standard(2, 3))),
      ("CHECKSUM", Some(FunctionDefinition.standard(2, Int.MaxValue))),
      ("CHECKSUM_AGG", Some(FunctionDefinition.standard(1))),
      ("COALESCE", Some(FunctionDefinition.standard(1, Int.MaxValue))),
      ("COL_LENGTH", Some(FunctionDefinition.standard(2))),
      ("COL_NAME", Some(FunctionDefinition.standard(2))),
      ("COLUMNPROPERTY", Some(FunctionDefinition.standard(3))),
      ("COMPRESS", Some(FunctionDefinition.standard(1))),
      ("CONCAT", Some(FunctionDefinition.standard(2, Int.MaxValue))),
      ("CONCAT_WS", Some(FunctionDefinition.standard(3, Int.MaxValue))),
      ("CONNECTIONPROPERTY", Some(FunctionDefinition.notConvertible(1))),
      ("CONTEXT_INFO", Some(FunctionDefinition.standard(0))),
      ("CONVERT", Some(FunctionDefinition.standard(2, 3))),
      ("COS", Some(FunctionDefinition.standard(1))),
      ("COT", Some(FunctionDefinition.standard(1))),
      ("COUNT", Some(FunctionDefinition.standard(1))),
      ("COUNT_BIG", Some(FunctionDefinition.standard(1))),
      ("CUME_DIST", Some(FunctionDefinition.standard(0))),
      ("CURRENT_DATE", Some(FunctionDefinition.standard(0))),
      ("CURRENT_REQUEST_ID", Some(FunctionDefinition.standard(0))),
      ("CURRENT_TIMESTAMP", Some(FunctionDefinition.standard(0))),
      ("CURRENT_TIMEZONE", Some(FunctionDefinition.standard(0))),
      ("CURRENT_TIMEZONE_ID", Some(FunctionDefinition.standard(0))),
      ("CURRENT_TRANSACTION_ID", Some(FunctionDefinition.standard(0))),
      ("CURRENT_USER", Some(FunctionDefinition.standard(0))),
      ("CURSOR_ROWS", Some(FunctionDefinition.standard(0))),
      ("CURSOR_STATUS", Some(FunctionDefinition.standard(2))),
      ("DATABASE_PRINCIPAL_ID", Some(FunctionDefinition.standard(0, 1))),
      ("DATABASEPROPERTY", Some(FunctionDefinition.standard(2))),
      ("DATABASEPROPERTYEX", Some(FunctionDefinition.standard(2))),
      ("DATALENGTH", Some(FunctionDefinition.standard(1))),
      ("DATE_BUCKET", Some(FunctionDefinition.standard(3, 4))),
      ("DATE_DIFF_BIG", Some(FunctionDefinition.standard(3))),
      ("DATEADD", Some(FunctionDefinition.standard(3))),
      ("DATEDIFF", Some(FunctionDefinition.standard(3))),
      ("DATEFROMPARTS", Some(FunctionDefinition.standard(3))),
      ("DATENAME", Some(FunctionDefinition.standard(2))),
      ("DATEPART", Some(FunctionDefinition.standard(2))),
      ("DATETIME2FROMPARTS", Some(FunctionDefinition.standard(8))),
      ("DATETIMEFROMPARTS", Some(FunctionDefinition.standard(7))),
      ("DATETIMEOFFSETFROMPARTS", Some(FunctionDefinition.standard(10))),
      ("DATETRUNC", Some(FunctionDefinition.standard(2))),
      ("DAY", Some(FunctionDefinition.standard(1))),
      ("DB_ID", Some(FunctionDefinition.standard(0, 1))),
      ("DB_NAME", Some(FunctionDefinition.standard(0, 1))),
      ("DECOMPRESS", Some(FunctionDefinition.standard(1))),
      ("DEGREES", Some(FunctionDefinition.standard(1))),
      ("DENSE_RANK", Some(FunctionDefinition.standard(0))),
      ("DIFFERENCE", Some(FunctionDefinition.standard(2))),
      ("EOMONTH", Some(FunctionDefinition.standard(1, 2))),
      ("ERROR_LINE", Some(FunctionDefinition.standard(0))),
      ("ERROR_MESSAGE", Some(FunctionDefinition.standard(0))),
      ("ERROR_NUMBER", Some(FunctionDefinition.standard(0))),
      ("ERROR_PROCEDURE", Some(FunctionDefinition.standard(0))),
      ("ERROR_SEVERITY", Some(FunctionDefinition.standard(0))),
      ("ERROR_STATE", Some(FunctionDefinition.standard(0))),
      ("EXIST", Some(FunctionDefinition.xml(1))),
      ("EXP", Some(FunctionDefinition.standard(1))),
      ("FILE_ID", Some(FunctionDefinition.standard(1))),
      ("FILE_IDEX", Some(FunctionDefinition.standard(1))),
      ("FILE_NAME", Some(FunctionDefinition.standard(1))),
      ("FILEGROUP_ID", Some(FunctionDefinition.standard(1))),
      ("FILEGROUP_NAME", Some(FunctionDefinition.standard(1))),
      ("FILEGROUPPROPERTY", Some(FunctionDefinition.standard(2))),
      ("FILEPROPERTY", Some(FunctionDefinition.standard(2))),
      ("FILEPROPERTYEX", Some(FunctionDefinition.standard(2))),
      ("FIRST_VALUE", Some(FunctionDefinition.standard(1))),
      ("FLOOR", Some(FunctionDefinition.standard(1))),
      ("FORMAT", Some(FunctionDefinition.standard(2, 3))),
      ("FORMATMESSAGE", Some(FunctionDefinition.standard(2, Int.MaxValue))),
      ("FULLTEXTCATALOGPROPERTY", Some(FunctionDefinition.standard(2))),
      ("FULLTEXTSERVICEPROPERTY", Some(FunctionDefinition.standard(1))),
      ("GET_FILESTREAM_TRANSACTION_CONTEXT", Some(FunctionDefinition.standard(0))),
      ("GETANCESTGOR", Some(FunctionDefinition.standard(1))),
      ("GETANSINULL", Some(FunctionDefinition.standard(0, 1))),
      ("GETDATE", Some(FunctionDefinition.standard(0))),
      ("GETDESCENDANT", Some(FunctionDefinition.standard(2))),
      ("GETLEVEL", Some(FunctionDefinition.standard(0))),
      ("GETREPARENTEDVALUE", Some(FunctionDefinition.standard(2))),
      ("GETUTCDATE", Some(FunctionDefinition.standard(0))),
      ("GREATEST", Some(FunctionDefinition.standard(1, Int.MaxValue))),
      ("GROUPING", Some(FunctionDefinition.standard(1))),
      ("GROUPING_ID", Some(FunctionDefinition.standard(0, Int.MaxValue))),
      ("HAS_DBACCESS", Some(FunctionDefinition.standard(1))),
      ("HAS_PERMS_BY_NAME", Some(FunctionDefinition.standard(4, 5))),
      ("HOST_ID", Some(FunctionDefinition.standard(0))),
      ("HOST_NAME", Some(FunctionDefinition.standard(0))),
      ("IDENT_CURRENT", Some(FunctionDefinition.standard(1))),
      ("IDENT_INCR", Some(FunctionDefinition.standard(1))),
      ("IDENT_SEED", Some(FunctionDefinition.standard(1))),
      ("IDENTITY", Some(FunctionDefinition.standard(1, 3))),
      ("IFF", Some(FunctionDefinition.standard(3))),
      ("INDEX_COL", Some(FunctionDefinition.standard(3))),
      ("INDEXKEY_PROPERTY", Some(FunctionDefinition.standard(3))),
      ("INDEXPROPERTY", Some(FunctionDefinition.standard(3))),
      ("IS_MEMBER", Some(FunctionDefinition.standard(1))),
      ("IS_ROLEMEMBER", Some(FunctionDefinition.standard(1, 2))),
      ("IS_SRVROLEMEMBER", Some(FunctionDefinition.standard(1, 2))),
      ("ISDATE", Some(FunctionDefinition.standard(1))),
      ("ISDESCENDANTOF", Some(FunctionDefinition.standard(1))),
      ("ISJSON", Some(FunctionDefinition.standard(1, 2))),
      ("ISNUMERIC", Some(FunctionDefinition.standard(1))),
      ("JSON_MODIFY", Some(FunctionDefinition.standard(3))),
      ("JSON_PATH_EXISTS", Some(FunctionDefinition.standard(2))),
      ("JSON_QUERY", Some(FunctionDefinition.standard(2))),
      ("JSON_VALUE", Some(FunctionDefinition.standard(2))),
      ("LAG", Some(FunctionDefinition.standard(1, 3))),
      ("LAST_VALUE", Some(FunctionDefinition.standard(1))),
      ("LEAD", Some(FunctionDefinition.standard(1, 3))),
      ("LEAST", Some(FunctionDefinition.standard(1, Int.MaxValue))),
      ("LEFT", Some(FunctionDefinition.standard(2))),
      ("LEN", Some(FunctionDefinition.standard(1))),
      ("LOG", Some(FunctionDefinition.standard(1, 2))),
      ("LOG10", Some(FunctionDefinition.standard(1))),
      ("LOGINPROPERTY", Some(FunctionDefinition.standard(2))),
      ("LOWER", Some(FunctionDefinition.standard(1))),
      ("LTRIM", Some(FunctionDefinition.standard(1))),
      ("MAX", Some(FunctionDefinition.standard(1))),
      ("MIN", Some(FunctionDefinition.standard(1))),
      ("MIN_ACTIVE_ROWVERSION", Some(FunctionDefinition.standard(0))),
      ("MONTH", Some(FunctionDefinition.standard(1))),
      ("NCHAR", Some(FunctionDefinition.standard(1))),
      ("NEWID", Some(FunctionDefinition.standard(0))),
      ("NEWSEQUENTIALID", Some(FunctionDefinition.standard(0))),
      ("NODES", Some(FunctionDefinition.xml(1))),
      ("NTILE", Some(FunctionDefinition.standard(1))),
      ("NULLIF", Some(FunctionDefinition.standard(2))),
      ("OBJECT_DEFINITION", Some(FunctionDefinition.standard(1))),
      ("OBJECT_ID", Some(FunctionDefinition.standard(1, 2))),
      ("OBJECT_NAME", Some(FunctionDefinition.standard(1, 2))),
      ("OBJECT_SCHEMA_NAME", Some(FunctionDefinition.standard(1, 2))),
      ("OBJECTPROPERTY", Some(FunctionDefinition.standard(2))),
      ("OBJECTPROPERTYEX", Some(FunctionDefinition.standard(2))),
      ("ORIGINAL_DB_NAME", Some(FunctionDefinition.standard(0))),
      ("ORIGINAL_LOGIN", Some(FunctionDefinition.standard(0))),
      ("PARSE", Some(FunctionDefinition.notConvertible(2, 3))),
      ("PARSENAME", Some(FunctionDefinition.standard(2))),
      ("PATINDEX", Some(FunctionDefinition.standard(2))),
      ("PERCENTILE_CONT", Some(FunctionDefinition.standard(1))),
      ("PERCENTILE_DISC", Some(FunctionDefinition.standard(1))),
      ("PERMISSIONS", Some(FunctionDefinition.notConvertible(0, 2))),
      ("PI", Some(FunctionDefinition.standard(0))),
      ("POWER", Some(FunctionDefinition.standard(2))),
      ("PWDCOMPARE", Some(FunctionDefinition.standard(2, 3))),
      ("PWDENCRYPT", Some(FunctionDefinition.standard(1))),
      ("QUERY", Some(FunctionDefinition.xml(1))),
      ("QUOTENAME", Some(FunctionDefinition.standard(1, 2))),
      ("RADIANS", Some(FunctionDefinition.standard(1))),
      ("RAND", Some(FunctionDefinition.standard(0, 1))),
      ("RANK", Some(FunctionDefinition.standard(0))),
      ("REPLACE", Some(FunctionDefinition.standard(3))),
      ("REPLICATE", Some(FunctionDefinition.standard(2))),
      ("REVERSE", Some(FunctionDefinition.standard(1))),
      ("RIGHT", Some(FunctionDefinition.standard(2))),
      ("ROUND", Some(FunctionDefinition.standard(2, 3))),
      ("ROW_NUMBER", Some(FunctionDefinition.standard(0))),
      ("ROWCOUNT_BIG", Some(FunctionDefinition.standard(0))),
      ("RTRIM", Some(FunctionDefinition.standard(1))),
      ("SCHEMA_ID", Some(FunctionDefinition.standard(0, 1))),
      ("SCHEMA_NAME", Some(FunctionDefinition.standard(0, 1))),
      ("SCOPE_IDENTITY", Some(FunctionDefinition.standard(0))),
      ("SERVERPROPERTY", Some(FunctionDefinition.standard(1))),
      ("SESSION_CONTEXT", Some(FunctionDefinition.standard(1, 2))),
      ("SESSION_USER", Some(FunctionDefinition.standard(0))),
      ("SESSIONPROPERTY", Some(FunctionDefinition.standard(1))),
      ("SIGN", Some(FunctionDefinition.standard(1))),
      ("SIN", Some(FunctionDefinition.standard(1))),
      ("SMALLDATETIMEFROMPARTS", Some(FunctionDefinition.standard(5))),
      ("SOUNDEX", Some(FunctionDefinition.standard(1))),
      ("SPACE", Some(FunctionDefinition.standard(1))),
      ("SQL_VARIANT_PROPERTY", Some(FunctionDefinition.standard(2))),
      ("SQRT", Some(FunctionDefinition.standard(1))),
      ("SQUARE", Some(FunctionDefinition.standard(1))),
      ("STATS_DATE", Some(FunctionDefinition.standard(2))),
      ("STDEV", Some(FunctionDefinition.standard(1))),
      ("STDEVP", Some(FunctionDefinition.standard(1))),
      ("STR", Some(FunctionDefinition.standard(1, 3))),
      ("STRING_AGG", Some(FunctionDefinition.standard(2, 3))),
      ("STRING_ESCAPE", Some(FunctionDefinition.standard(2))),
      ("STUFF", Some(FunctionDefinition.standard(4))),
      ("SUBSTRING", Some(FunctionDefinition.standard(2, 3))),
      ("SUM", Some(FunctionDefinition.standard(1))),
      ("SUSER_ID", Some(FunctionDefinition.standard(0, 1))),
      ("SUSER_NAME", Some(FunctionDefinition.standard(0, 1))),
      ("SUSER_SID", Some(FunctionDefinition.standard(0, 2))),
      ("SUSER_SNAME", Some(FunctionDefinition.standard(0, 1))),
      ("SWITCHOFFSET", Some(FunctionDefinition.standard(2))),
      ("SYSDATETIME", Some(FunctionDefinition.standard(0))),
      ("SYSDATETIMEOFFSET", Some(FunctionDefinition.standard(0))),
      ("SYSTEM_USER", Some(FunctionDefinition.standard(0))),
      ("SYSUTCDATETIME", Some(FunctionDefinition.standard(0))),
      ("TAN", Some(FunctionDefinition.standard(1))),
      ("TIMEFROMPARTS", Some(FunctionDefinition.standard(5))),
      ("TODATETIMEOFFSET", Some(FunctionDefinition.standard(2))),
      ("TOSTRING", Some(FunctionDefinition.standard(0))),
      ("TRANSLATE", Some(FunctionDefinition.standard(3))),
      ("TRIM", Some(FunctionDefinition.standard(1, 2))),
      ("TYPE_ID", Some(FunctionDefinition.standard(1))),
      ("TYPE_NAME", Some(FunctionDefinition.standard(1))),
      ("TYPEPROPERTY", Some(FunctionDefinition.standard(2))),
      ("UNICODE", Some(FunctionDefinition.standard(1))),
      ("UPPER", Some(FunctionDefinition.standard(1))),
      ("USER", Some(FunctionDefinition.standard(0))),
      ("USER_ID", Some(FunctionDefinition.standard(0, 1))),
      ("USER_NAME", Some(FunctionDefinition.standard(0, 1))),
      ("VALUE", Some(FunctionDefinition.xml(2))),
      ("VAR", Some(FunctionDefinition.standard(1))),
      ("VARP", Some(FunctionDefinition.standard(1))),
      ("XACT_STATE", Some(FunctionDefinition.standard(0))),
      ("YEAR", Some(FunctionDefinition.standard(1))))

    val functionBuilder = new TSqlFunctionBuilder

    forAll(functions) { (functionName: String, expectedArity: Option[FunctionDefinition]) =>
      functionBuilder.functionDefinition(functionName) shouldEqual expectedArity
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

      ("ISNULL", Seq(simplyNamedColumn("x"), ir.Literal(integer = Some(1))), "IFNULL"),
      ("GET_BIT", Seq(simplyNamedColumn("x"), ir.Literal(integer = Some(1))), "GETBIT"),
      ("SET_BIT", Seq(simplyNamedColumn("x"), ir.Literal(integer = Some(1))), "SETBIT"),
      ("left_SHIFT", Seq(simplyNamedColumn("x"), ir.Literal(integer = Some(1))), "LEFTSHIFT"),
      ("RIGHT_SHIFT", Seq(simplyNamedColumn("x"), ir.Literal(integer = Some(1))), "RIGHTSHIFT"))

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

    val result1 = functionBuilder.buildFunction("ISNULL", Seq(simplyNamedColumn("x"), ir.Literal(integer = Some(0))))
    result1 shouldBe a[UnresolvedFunction]
  }

  "buildFunction" should "not resolve IFNULL when child dialect isn't Snowflake" in {
    val functionBuilder = new TSqlFunctionBuilder

    val result1 = functionBuilder.buildFunction("IFNULL", Seq(simplyNamedColumn("x"), ir.Literal(integer = Some(0))))
    result1 shouldBe a[UnresolvedFunction]
  }

  "buildFunction" should "Should preserve case if it can" in {
    val functionBuilder = new TSqlFunctionBuilder
    val result1 = functionBuilder.buildFunction("isnull", Seq(simplyNamedColumn("x"), ir.Literal(integer = Some(0))))
    result1 match {
      case f: ir.CallFunction => f.function_name shouldBe "ifnull"
      case _ => fail("ifnull conversion failed")
    }
  }

  "FunctionRename strategy" should "preserve original function if no match is found" in {
    val functionBuilder = new TSqlFunctionBuilder
    val result1 = functionBuilder.applyConversionStrategy(
      FunctionDefinition.standard(1),
      Seq(ir.Literal(integer = Some(66))),
      "Abs")
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
