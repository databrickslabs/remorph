package com.databricks.labs.remorph.parsers.common

import com.databricks.labs.remorph.parsers.intermediate.UnresolvedFunction
import com.databricks.labs.remorph.parsers.snowflake.SnowflakeFunctionBuilder
import com.databricks.labs.remorph.parsers.tsql.{TSqlFunctionBuilder, TSqlFunctionConverters}
import com.databricks.labs.remorph.parsers.{intermediate => ir, _}
import org.scalatest.flatspec.AnyFlatSpec
import org.scalatest.matchers.should.Matchers
import org.scalatest.prop.TableDrivenPropertyChecks

class FunctionBuilderSpec extends AnyFlatSpec with Matchers with TableDrivenPropertyChecks {

  "SnowFlakeFunctionBuilder" should "return correct arity for each function" in {
    val functions = Table(
      ("functionName", "expectedArity"), // Header

      // Snowflake specific
      ("IFNULL", Some(FunctionDefinition.standard(2))),
      ("ISNULL", Some(FunctionDefinition.standard(1))))

    val functionBuilder = new SnowflakeFunctionBuilder
    forAll(functions) { (functionName: String, expectedArity: Option[FunctionDefinition]) =>
      functionBuilder.functionDefinition(functionName) shouldEqual expectedArity
    }
  }
  // While this appears to be somewhat redundant, it will catch any changes in the functionArity method
  // that happen through typos or other mistakes such as deletion.
  "TSqlFunctionBuilder" should "return correct arity for each function" in {
    val functions = Table(
      ("functionName", "expectedArity"), // Header

      // TSql specific
      ("@@CURSOR_STATUS", Some(FunctionDefinition.notConvertible(0))),
      ("@@FETCH_STATUS", Some(FunctionDefinition.notConvertible(0))),
      ("ISNULL", Some(FunctionDefinition.standard(2).withConversionStrategy(TSqlFunctionConverters.FunctionRename))),
      ("MODIFY", Some(FunctionDefinition.xml(1))))
    val functionBuilder = new TSqlFunctionBuilder

    forAll(functions) { (functionName: String, expectedArity: Option[FunctionDefinition]) =>
      functionBuilder.functionDefinition(functionName) shouldEqual expectedArity
    }
  }

  "FunctionBuilder" should "return correct arity for each function" in {

    val functions = Table(
      ("functionName", "expectedArity"), // Header

      ("ABS", Some(FunctionDefinition.standard(1))),
      ("ACOS", Some(FunctionDefinition.standard(1))),
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

    // Test function name with less than 2 characters
    val result1 = functionBuilder.buildFunction("a", List.empty)
    result1 match {
      case f: ir.UnresolvedFunction => f.function_name shouldBe "a"
      case _ => fail("Unexpected function type")
    }

    // Test function name with matching quotes
    val result2 = functionBuilder.buildFunction("'quoted'", List.empty)
    result2 match {
      case f: ir.UnresolvedFunction => f.function_name shouldBe "quoted"
      case _ => fail("Unexpected function type")
    }

    // Test function name with matching brackets
    val result3 = functionBuilder.buildFunction("[bracketed]", List.empty)
    result3 match {
      case f: ir.UnresolvedFunction => f.function_name shouldBe "bracketed"
      case _ => fail("Unexpected function type")
    }

    // Test function name with matching backslashes
    val result4 = functionBuilder.buildFunction("\\backslashed\\", List.empty)
    result4 match {
      case f: ir.UnresolvedFunction => f.function_name shouldBe "backslashed"
      case _ => fail("Unexpected function type")
    }

    // Test function name with non-matching quotes
    val result5 = functionBuilder.buildFunction("'nonmatching", List.empty)
    result5 match {
      case f: ir.UnresolvedFunction => f.function_name shouldBe "'nonmatching"
      case _ => fail("Unexpected function type")
    }
  }

  "buildFunction" should "Apply known TSql conversion strategies" in {
    val functionBuilder = new TSqlFunctionBuilder

    val result1 = functionBuilder.buildFunction("ISNULL", Seq(ir.Column("x"), ir.Literal(integer = Some(0))))
    result1 match {
      case f: ir.CallFunction => f.function_name shouldBe "IFNULL"
      case _ => fail("ISNULL TSql conversion failed")
    }
  }

  "buildFunction" should "not resolve IFNULL when input dialect isn't TSql" in {
    val functionBuilder = new SnowflakeFunctionBuilder

    val result1 = functionBuilder.buildFunction("ISNULL", Seq(ir.Column("x"), ir.Literal(integer = Some(0))))
    result1 shouldBe a[UnresolvedFunction]
  }

  "buildFunction" should "not resolve IFNULL when input dialect isn't Snowflake" in {
    val functionBuilder = new TSqlFunctionBuilder

    val result1 = functionBuilder.buildFunction("IFNULL", Seq(ir.Column("x"), ir.Literal(integer = Some(0))))
    result1 shouldBe a[UnresolvedFunction]
  }

  "buildFunction" should "Should preserve case if it can" in {
    val functionBuilder = new TSqlFunctionBuilder
    val result1 = functionBuilder.buildFunction("isnull", Seq(ir.Column("x"), ir.Literal(integer = Some(0))))
    result1 match {
      case f: ir.CallFunction => f.function_name shouldBe "ifnull"
      case _ => fail("ifnull conversion failed")
    }
  }

  "FunctionRename strategy" should "preserve original function if no match is found" in {
    val result1 =
      TSqlFunctionConverters.FunctionRename.convert("Abs", Seq(ir.Literal(integer = Some(66))))
    result1 match {
      case f: ir.CallFunction => f.function_name shouldBe "Abs"
      case _ => fail("UNKNOWN_FUNCTION conversion failed")
    }
  }
}
