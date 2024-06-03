package com.databricks.labs.remorph.parsers.common

import com.databricks.labs.remorph.parsers.intermediate.UnresolvedFunction
import com.databricks.labs.remorph.parsers.{intermediate => ir, _}
import org.scalatest.flatspec.AnyFlatSpec
import org.scalatest.matchers.should.Matchers
import org.scalatest.prop.TableDrivenPropertyChecks

class FunctionBuilderSpec extends AnyFlatSpec with Matchers with TableDrivenPropertyChecks {

  // While this appears to be somewhat redundant, it will catch any changes in the functionArity method
  // that happen through typos or other mistakes such as deletion.
  "functionArity" should "return correct arity for each function" in {
    val functions = Table(
      ("dialect", "functionName", "expectedArity"), // Header

      // Snowflake specific
      (Snowflake, "IFNULL", Some(FunctionDefinition.standard(2))),
      (Snowflake, "ISNULL", Some(FunctionDefinition.standard(1))),

      // TSql specific
      (TSql, "@@CURSOR_STATUS", Some(FunctionDefinition.notConvertible(0))),
      (TSql, "@@FETCH_STATUS", Some(FunctionDefinition.notConvertible(0))),
      (TSql, "ABS", Some(FunctionDefinition.standard(1))),
      (TSql, "ACOS", Some(FunctionDefinition.standard(1))),
      (TSql, "APP_NAME", Some(FunctionDefinition.standard(0))),
      (TSql, "APPLOCK_MODE", Some(FunctionDefinition.standard(3))),
      (TSql, "APPLOCK_TEST", Some(FunctionDefinition.standard(4))),
      (TSql, "ASCII", Some(FunctionDefinition.standard(1))),
      (TSql, "ASIN", Some(FunctionDefinition.standard(1))),
      (TSql, "ASSEMBLYPROPERTY", Some(FunctionDefinition.standard(2))),
      (TSql, "ATAN", Some(FunctionDefinition.standard(1))),
      (TSql, "ATN2", Some(FunctionDefinition.standard(2))),
      (TSql, "AVG", Some(FunctionDefinition.standard(1))),
      (TSql, "BINARY_CHECKSUM", Some(FunctionDefinition.standard(1, Int.MaxValue))),
      (TSql, "CEILING", Some(FunctionDefinition.standard(1))),
      (TSql, "CERT_ID", Some(FunctionDefinition.standard(1))),
      (TSql, "CERTENCODED", Some(FunctionDefinition.standard(1))),
      (TSql, "CERTPRIVATEKEY", Some(FunctionDefinition.standard(2, 3))),
      (TSql, "CHAR", Some(FunctionDefinition.standard(1))),
      (TSql, "CHARINDEX", Some(FunctionDefinition.standard(2, 3))),
      (TSql, "CHECKSUM", Some(FunctionDefinition.standard(2, Int.MaxValue))),
      (TSql, "CHECKSUM_AGG", Some(FunctionDefinition.standard(1))),
      (TSql, "COALESCE", Some(FunctionDefinition.standard(1, Int.MaxValue))),
      (TSql, "COL_LENGTH", Some(FunctionDefinition.standard(2))),
      (TSql, "COL_NAME", Some(FunctionDefinition.standard(2))),
      (TSql, "COLUMNPROPERTY", Some(FunctionDefinition.standard(3))),
      (TSql, "COMPRESS", Some(FunctionDefinition.standard(1))),
      (TSql, "CHECKSUM_AGG", Some(FunctionDefinition.standard(1))),
      (TSql, "CONCAT", Some(FunctionDefinition.standard(2, Int.MaxValue))),
      (TSql, "CONCAT_WS", Some(FunctionDefinition.standard(3, Int.MaxValue))),
      (TSql, "CONNECTIONPROPERTY", Some(FunctionDefinition.notConvertible(1))),
      (TSql, "CONTEXT_INFO", Some(FunctionDefinition.standard(0))),
      (TSql, "CONVERT", Some(FunctionDefinition.standard(2, 3))),
      (TSql, "COS", Some(FunctionDefinition.standard(1))),
      (TSql, "COT", Some(FunctionDefinition.standard(1))),
      (TSql, "COUNT", Some(FunctionDefinition.standard(1))),
      (TSql, "COUNT_BIG", Some(FunctionDefinition.standard(1))),
      (TSql, "CURRENT_DATE", Some(FunctionDefinition.standard(0))),
      (TSql, "CURRENT_REQUEST_ID", Some(FunctionDefinition.standard(0))),
      (TSql, "CURRENT_TIMESTAMP", Some(FunctionDefinition.standard(0))),
      (TSql, "CURRENT_TIMEZONE", Some(FunctionDefinition.standard(0))),
      (TSql, "CURRENT_TIMEZONE_ID", Some(FunctionDefinition.standard(0))),
      (TSql, "CURRENT_TRANSACTION_ID", Some(FunctionDefinition.standard(0))),
      (TSql, "CURRENT_USER", Some(FunctionDefinition.standard(0))),
      (TSql, "CURSOR_ROWS", Some(FunctionDefinition.standard(0))),
      (TSql, "CUME_DIST", Some(FunctionDefinition.standard(0))),
      (TSql, "CURSOR_STATUS", Some(FunctionDefinition.standard(2))),
      (TSql, "DATABASE_PRINCIPAL_ID", Some(FunctionDefinition.standard(0, 1))),
      (TSql, "DATABASEPROPERTY", Some(FunctionDefinition.standard(2))),
      (TSql, "DATABASEPROPERTYEX", Some(FunctionDefinition.standard(2))),
      (TSql, "DATALENGTH", Some(FunctionDefinition.standard(1))),
      (TSql, "DATE_BUCKET", Some(FunctionDefinition.standard(3, 4))),
      (TSql, "DATE_DIFF_BIG", Some(FunctionDefinition.standard(3))),
      (TSql, "DATEADD", Some(FunctionDefinition.standard(3))),
      (TSql, "DATEDIFF", Some(FunctionDefinition.standard(3))),
      (TSql, "DATEFROMPARTS", Some(FunctionDefinition.standard(3))),
      (TSql, "DATENAME", Some(FunctionDefinition.standard(2))),
      (TSql, "DATEPART", Some(FunctionDefinition.standard(2))),
      (TSql, "DATETIME2FROMPARTS", Some(FunctionDefinition.standard(8))),
      (TSql, "DATETIMEFROMPARTS", Some(FunctionDefinition.standard(7))),
      (TSql, "DATETIMEOFFSETFROMPARTS", Some(FunctionDefinition.standard(10))),
      (TSql, "DATETRUNC", Some(FunctionDefinition.standard(2))),
      (TSql, "DAY", Some(FunctionDefinition.standard(1))),
      (TSql, "DB_ID", Some(FunctionDefinition.standard(0, 1))),
      (TSql, "DB_NAME", Some(FunctionDefinition.standard(0, 1))),
      (TSql, "DECOMPRESS", Some(FunctionDefinition.standard(1))),
      (TSql, "DEGREES", Some(FunctionDefinition.standard(1))),
      (TSql, "DENSE_RANK", Some(FunctionDefinition.standard(0))),
      (TSql, "DIFFERENCE", Some(FunctionDefinition.standard(2))),
      (TSql, "EOMONTH", Some(FunctionDefinition.standard(1, 2))),
      (TSql, "ERROR_LINE", Some(FunctionDefinition.standard(0))),
      (TSql, "ERROR_MESSAGE", Some(FunctionDefinition.standard(0))),
      (TSql, "ERROR_NUMBER", Some(FunctionDefinition.standard(0))),
      (TSql, "ERROR_PROCEDURE", Some(FunctionDefinition.standard(0))),
      (TSql, "ERROR_SEVERITY", Some(FunctionDefinition.standard(0))),
      (TSql, "ERROR_STATE", Some(FunctionDefinition.standard(0))),
      (TSql, "EXIST", Some(FunctionDefinition.xml(1))),
      (TSql, "EXP", Some(FunctionDefinition.standard(1))),
      (TSql, "FILE_ID", Some(FunctionDefinition.standard(1))),
      (TSql, "FILE_IDEX", Some(FunctionDefinition.standard(1))),
      (TSql, "FILE_NAME", Some(FunctionDefinition.standard(1))),
      (TSql, "FILEGROUP_ID", Some(FunctionDefinition.standard(1))),
      (TSql, "FILEGROUP_NAME", Some(FunctionDefinition.standard(1))),
      (TSql, "FILEGROUPPROPERTY", Some(FunctionDefinition.standard(2))),
      (TSql, "FILEPROPERTY", Some(FunctionDefinition.standard(2))),
      (TSql, "FILEPROPERTYEX", Some(FunctionDefinition.standard(2))),
      (TSql, "FIRST_VALUE", Some(FunctionDefinition.standard(1))),
      (TSql, "FLOOR", Some(FunctionDefinition.standard(1))),
      (TSql, "FORMAT", Some(FunctionDefinition.standard(2, 3))),
      (TSql, "FORMATMESSAGE", Some(FunctionDefinition.standard(2, Int.MaxValue))),
      (TSql, "FULLTEXTCATALOGPROPERTY", Some(FunctionDefinition.standard(2))),
      (TSql, "FULLTEXTSERVICEPROPERTY", Some(FunctionDefinition.standard(1))),
      (TSql, "GET_FILESTREAM_TRANSACTION_CONTEXT", Some(FunctionDefinition.standard(0))),
      (TSql, "GETANCESTGOR", Some(FunctionDefinition.standard(1))),
      (TSql, "GETANSINULL", Some(FunctionDefinition.standard(0, 1))),
      (TSql, "GETDATE", Some(FunctionDefinition.standard(0))),
      (TSql, "GETDESCENDANT", Some(FunctionDefinition.standard(2))),
      (TSql, "GETLEVEL", Some(FunctionDefinition.standard(0))),
      (TSql, "GETREPARENTEDVALUE", Some(FunctionDefinition.standard(2))),
      (TSql, "GETUTCDATE", Some(FunctionDefinition.standard(0))),
      (TSql, "GREATEST", Some(FunctionDefinition.standard(1, Int.MaxValue))),
      (TSql, "GROUPING", Some(FunctionDefinition.standard(1))),
      (TSql, "GROUPING_ID", Some(FunctionDefinition.standard(0, Int.MaxValue))),
      (TSql, "HAS_DBACCESS", Some(FunctionDefinition.standard(1))),
      (TSql, "HAS_PERMS_BY_NAME", Some(FunctionDefinition.standard(4, 5))),
      (TSql, "HOST_ID", Some(FunctionDefinition.standard(0))),
      (TSql, "HOST_NAME", Some(FunctionDefinition.standard(0))),
      (TSql, "IDENT_CURRENT", Some(FunctionDefinition.standard(1))),
      (TSql, "IDENT_INCR", Some(FunctionDefinition.standard(1))),
      (TSql, "IDENT_SEED", Some(FunctionDefinition.standard(1))),
      (TSql, "IDENTITY", Some(FunctionDefinition.standard(1, 3))),
      (TSql, "IFF", Some(FunctionDefinition.standard(3))),
      (TSql, "INDEX_COL", Some(FunctionDefinition.standard(3))),
      (TSql, "INDEXKEY_PROPERTY", Some(FunctionDefinition.standard(3))),
      (TSql, "INDEXPROPERTY", Some(FunctionDefinition.standard(3))),
      (TSql, "IS_MEMBER", Some(FunctionDefinition.standard(1))),
      (TSql, "IS_ROLEMEMBER", Some(FunctionDefinition.standard(1, 2))),
      (TSql, "IS_SRVROLEMEMBER", Some(FunctionDefinition.standard(1, 2))),
      (TSql, "ISDATE", Some(FunctionDefinition.standard(1))),
      (TSql, "ISDESCENDANTOF", Some(FunctionDefinition.standard(1))),
      (TSql, "ISJSON", Some(FunctionDefinition.standard(1, 2))),
      (TSql, "ISNULL", Some(FunctionDefinition.standard(2).withConversionStrategy(FunctionConverters.FunctionRename))),
      (TSql, "ISNUMERIC", Some(FunctionDefinition.standard(1))),
      (TSql, "JSON_MODIFY", Some(FunctionDefinition.standard(3))),
      (TSql, "JSON_PATH_EXISTS", Some(FunctionDefinition.standard(2))),
      (TSql, "JSON_QUERY", Some(FunctionDefinition.standard(2))),
      (TSql, "JSON_VALUE", Some(FunctionDefinition.standard(2))),
      (TSql, "LAG", Some(FunctionDefinition.standard(1, 3))),
      (TSql, "LEAD", Some(FunctionDefinition.standard(1, 3))),
      (TSql, "LEAST", Some(FunctionDefinition.standard(1, Int.MaxValue))),
      (TSql, "LEFT", Some(FunctionDefinition.standard(2))),
      (TSql, "LAST_VALUE", Some(FunctionDefinition.standard(1))),
      (TSql, "LEN", Some(FunctionDefinition.standard(1))),
      (TSql, "LOG", Some(FunctionDefinition.standard(1, 2))),
      (TSql, "LOG10", Some(FunctionDefinition.standard(1))),
      (TSql, "LOGINPROPERTY", Some(FunctionDefinition.standard(2))),
      (TSql, "LOWER", Some(FunctionDefinition.standard(1))),
      (TSql, "LTRIM", Some(FunctionDefinition.standard(1))),
      (TSql, "MAX", Some(FunctionDefinition.standard(1))),
      (TSql, "MIN", Some(FunctionDefinition.standard(1))),
      (TSql, "MIN_ACTIVE_ROWVERSION", Some(FunctionDefinition.standard(0))),
      (TSql, "MODIFY", Some(FunctionDefinition.xml(1))),
      (TSql, "MONTH", Some(FunctionDefinition.standard(1))),
      (TSql, "MODIFY", Some(FunctionDefinition.xml(1))),
      (TSql, "NCHAR", Some(FunctionDefinition.standard(1))),
      (TSql, "NEWID", Some(FunctionDefinition.standard(0))),
      (TSql, "NEWSEQUENTIALID", Some(FunctionDefinition.standard(0))),
      (TSql, "NODES", Some(FunctionDefinition.xml(1))),
      (TSql, "NTILE", Some(FunctionDefinition.standard(1))),
      (TSql, "NULLIF", Some(FunctionDefinition.standard(2))),
      (TSql, "OBJECT_DEFINITION", Some(FunctionDefinition.standard(1))),
      (TSql, "OBJECT_ID", Some(FunctionDefinition.standard(1, 2))),
      (TSql, "OBJECT_NAME", Some(FunctionDefinition.standard(1, 2))),
      (TSql, "OBJECT_SCHEMA_NAME", Some(FunctionDefinition.standard(1, 2))),
      (TSql, "OBJECTPROPERTY", Some(FunctionDefinition.standard(2))),
      (TSql, "OBJECTPROPERTYEX", Some(FunctionDefinition.standard(2))),
      (TSql, "ORIGINAL_DB_NAME", Some(FunctionDefinition.standard(0))),
      (TSql, "ORIGINAL_LOGIN", Some(FunctionDefinition.standard(0))),
      (TSql, "PARSE", Some(FunctionDefinition.notConvertible(2, 3))),
      (TSql, "PARSENAME", Some(FunctionDefinition.standard(2))),
      (TSql, "PATINDEX", Some(FunctionDefinition.standard(2))),
      (TSql, "PERMISSIONS", Some(FunctionDefinition.notConvertible(0, 2))),
      (TSql, "PI", Some(FunctionDefinition.standard(0))),
      (TSql, "PERCENTILE_CONT", Some(FunctionDefinition.standard(1))),
      (TSql, "PERCENTILE_DISC", Some(FunctionDefinition.standard(1))),
      (TSql, "POWER", Some(FunctionDefinition.standard(2))),
      (TSql, "PWDCOMPARE", Some(FunctionDefinition.standard(2, 3))),
      (TSql, "PWDENCRYPT", Some(FunctionDefinition.standard(1))),
      (TSql, "QUERY", Some(FunctionDefinition.xml(1))),
      (TSql, "QUOTENAME", Some(FunctionDefinition.standard(1, 2))),
      (TSql, "RADIANS", Some(FunctionDefinition.standard(1))),
      (TSql, "RAND", Some(FunctionDefinition.standard(0, 1))),
      (TSql, "RANK", Some(FunctionDefinition.standard(0))),
      (TSql, "REPLACE", Some(FunctionDefinition.standard(3))),
      (TSql, "REPLICATE", Some(FunctionDefinition.standard(2))),
      (TSql, "REVERSE", Some(FunctionDefinition.standard(1))),
      (TSql, "RIGHT", Some(FunctionDefinition.standard(2))),
      (TSql, "ROUND", Some(FunctionDefinition.standard(2, 3))),
      (TSql, "ROW_NUMBER", Some(FunctionDefinition.standard(0))),
      (TSql, "ROWCOUNT_BIG", Some(FunctionDefinition.standard(0))),
      (TSql, "RTRIM", Some(FunctionDefinition.standard(1))),
      (TSql, "SCHEMA_ID", Some(FunctionDefinition.standard(0, 1))),
      (TSql, "SCHEMA_NAME", Some(FunctionDefinition.standard(0, 1))),
      (TSql, "SCOPE_IDENTITY", Some(FunctionDefinition.standard(0))),
      (TSql, "SERVERPROPERTY", Some(FunctionDefinition.standard(1))),
      (TSql, "SESSION_CONTEXT", Some(FunctionDefinition.standard(1, 2))),
      (TSql, "SESSION_USER", Some(FunctionDefinition.standard(0))),
      (TSql, "SESSIONPROPERTY", Some(FunctionDefinition.standard(1))),
      (TSql, "SIGN", Some(FunctionDefinition.standard(1))),
      (TSql, "SIN", Some(FunctionDefinition.standard(1))),
      (TSql, "SMALLDATETIMEFROMPARTS", Some(FunctionDefinition.standard(5))),
      (TSql, "SOUNDEX", Some(FunctionDefinition.standard(1))),
      (TSql, "SPACE", Some(FunctionDefinition.standard(1))),
      (TSql, "SQL_VARIANT_PROPERTY", Some(FunctionDefinition.standard(2))),
      (TSql, "SQRT", Some(FunctionDefinition.standard(1))),
      (TSql, "SQUARE", Some(FunctionDefinition.standard(1))),
      (TSql, "STATS_DATE", Some(FunctionDefinition.standard(2))),
      (TSql, "STDEV", Some(FunctionDefinition.standard(1))),
      (TSql, "STDEVP", Some(FunctionDefinition.standard(1))),
      (TSql, "STR", Some(FunctionDefinition.standard(1, 3))),
      (TSql, "STRING_AGG", Some(FunctionDefinition.standard(2, 3))),
      (TSql, "STRING_ESCAPE", Some(FunctionDefinition.standard(2))),
      (TSql, "STUFF", Some(FunctionDefinition.standard(4))),
      (TSql, "SUBSTRING", Some(FunctionDefinition.standard(2, 3))),
      (TSql, "SUM", Some(FunctionDefinition.standard(1))),
      (TSql, "SUSER_ID", Some(FunctionDefinition.standard(0, 1))),
      (TSql, "SUSER_NAME", Some(FunctionDefinition.standard(0, 1))),
      (TSql, "SUSER_SID", Some(FunctionDefinition.standard(0, 2))),
      (TSql, "SUSER_SNAME", Some(FunctionDefinition.standard(0, 1))),
      (TSql, "SWITCHOFFSET", Some(FunctionDefinition.standard(2))),
      (TSql, "SYSDATETIME", Some(FunctionDefinition.standard(0))),
      (TSql, "SYSDATETIMEOFFSET", Some(FunctionDefinition.standard(0))),
      (TSql, "SYSTEM_USER", Some(FunctionDefinition.standard(0))),
      (TSql, "SYSUTCDATETIME", Some(FunctionDefinition.standard(0))),
      (TSql, "TAN", Some(FunctionDefinition.standard(1))),
      (TSql, "TIMEFROMPARTS", Some(FunctionDefinition.standard(5))),
      (TSql, "TODATETIMEOFFSET", Some(FunctionDefinition.standard(2))),
      (TSql, "TOSTRING", Some(FunctionDefinition.standard(0))),
      (TSql, "TRANSLATE", Some(FunctionDefinition.standard(3))),
      (TSql, "TRIM", Some(FunctionDefinition.standard(1, 2))),
      (TSql, "TYPE_ID", Some(FunctionDefinition.standard(1))),
      (TSql, "TYPE_NAME", Some(FunctionDefinition.standard(1))),
      (TSql, "TYPEPROPERTY", Some(FunctionDefinition.standard(2))),
      (TSql, "UNICODE", Some(FunctionDefinition.standard(1))),
      (TSql, "UPPER", Some(FunctionDefinition.standard(1))),
      (TSql, "USER", Some(FunctionDefinition.standard(0))),
      (TSql, "USER_ID", Some(FunctionDefinition.standard(0, 1))),
      (TSql, "USER_NAME", Some(FunctionDefinition.standard(0, 1))),
      (TSql, "VALUE", Some(FunctionDefinition.xml(2))),
      (TSql, "VAR", Some(FunctionDefinition.standard(1))),
      (TSql, "VARP", Some(FunctionDefinition.standard(1))),
      (TSql, "XACT_STATE", Some(FunctionDefinition.standard(0))),
      (TSql, "YEAR", Some(FunctionDefinition.standard(1))))

    forAll(functions) { (dialect: SqlDialect, functionName: String, expectedArity: Option[FunctionDefinition]) =>
      FunctionBuilder.functionDefinition(dialect, functionName) shouldEqual expectedArity
    }
  }

  "functionType" should "return correct function type for each function" in {
    val functions = Table(
      ("dialect", "functionName", "expectedFunctionType"), // Header

      // This table needs to maintain an example of all types of functions in Arity and FunctionType
      // However, it is not necessary to test all functions, just one of each type.
      // However, note that there are no XML functions with VariableArity at the moment.
      (TSql, "MODIFY", XmlFunction),
      (TSql, "ABS", StandardFunction),
      (TSql, "VALUE", XmlFunction),
      (TSql, "CONCAT", StandardFunction),
      (TSql, "TRIM", StandardFunction))

    // Test all FunctionType combinations that currently exist
    forAll(functions) { (dialect: SqlDialect, functionName: String, expectedFunctionType: FunctionType) =>
      FunctionBuilder.functionType(dialect, functionName) shouldEqual expectedFunctionType
    }
  }

  "functionType" should "return UnknownFunction for functions that do not exist" in {
    val result = FunctionBuilder.functionType(TSql, "DOES_NOT_EXIST")
    result shouldEqual UnknownFunction
  }

  "isConvertible method in FunctionArity" should "return true by default" in {
    val fixedArity = FunctionDefinition.standard(1)
    fixedArity.functionType should not be NotConvertibleFunction

    val variableArity = FunctionDefinition.standard(1, 2)
    variableArity should not be NotConvertibleFunction

  }

  "buildFunction" should "remove quotes and brackets from function names" in {
    // Test function name with less than 2 characters
    val result1 = FunctionBuilder.buildFunction("a", List.empty, TSql)
    result1 match {
      case f: ir.UnresolvedFunction => f.function_name shouldBe "a"
      case _ => fail("Unexpected function type")
    }

    // Test function name with matching quotes
    val result2 = FunctionBuilder.buildFunction("'quoted'", List.empty, TSql)
    result2 match {
      case f: ir.UnresolvedFunction => f.function_name shouldBe "quoted"
      case _ => fail("Unexpected function type")
    }

    // Test function name with matching brackets
    val result3 = FunctionBuilder.buildFunction("[bracketed]", List.empty, TSql)
    result3 match {
      case f: ir.UnresolvedFunction => f.function_name shouldBe "bracketed"
      case _ => fail("Unexpected function type")
    }

    // Test function name with matching backslashes
    val result4 = FunctionBuilder.buildFunction("\\backslashed\\", List.empty, TSql)
    result4 match {
      case f: ir.UnresolvedFunction => f.function_name shouldBe "backslashed"
      case _ => fail("Unexpected function type")
    }

    // Test function name with non-matching quotes
    val result5 = FunctionBuilder.buildFunction("'nonmatching", List.empty, TSql)
    result5 match {
      case f: ir.UnresolvedFunction => f.function_name shouldBe "'nonmatching"
      case _ => fail("Unexpected function type")
    }
  }

  "buildFunction" should "Apply known TSQL conversion strategies" in {
    val result1 = FunctionBuilder.buildFunction("ISNULL", Seq(ir.Column("x"), ir.Literal(integer = Some(0))), TSql)
    result1 match {
      case f: ir.CallFunction => f.function_name shouldBe "IFNULL"
      case _ => fail("ISNULL TSql conversion failed")
    }
  }

  "buildFunction" should "not resolve IFNULL when input dialect isn't TSql" in {
    val result1 = FunctionBuilder.buildFunction("ISNULL", Seq(ir.Column("x"), ir.Literal(integer = Some(0))), Snowflake)
    result1 shouldBe a[UnresolvedFunction]
  }

  "buildFunction" should "not resolve IFNULL when input dialect isn't Snowflake" in {
    val result1 = FunctionBuilder.buildFunction("IFNULL", Seq(ir.Column("x"), ir.Literal(integer = Some(0))), TSql)
    result1 shouldBe a[UnresolvedFunction]
  }

  "buildFunction" should "Should preserve case if it can" in {
    val result1 = FunctionBuilder.buildFunction("isnull", Seq(ir.Column("x"), ir.Literal(integer = Some(0))), TSql)
    result1 match {
      case f: ir.CallFunction => f.function_name shouldBe "ifnull"
      case _ => fail("ifnull conversion failed")
    }
  }

  "FunctionRename strategy" should "preserve original function if no match is found" in {
    val result1 =
      FunctionConverters.FunctionRename.convert("Abs", Seq(ir.Literal(integer = Some(66))), TSql)
    result1 match {
      case f: ir.CallFunction => f.function_name shouldBe "Abs"
      case _ => fail("UNKNOWN_FUNCTION conversion failed")
    }
  }
}
