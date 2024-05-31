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

      (TSql, "MODIFY", Some(FixedArity(1, XmlFunction))),
      (TSql, "ABS", Some(FixedArity(1))),
      (TSql, "ACOS", Some(FixedArity(1))),
      (TSql, "APP_NAME", Some(FixedArity(0))),
      (TSql, "APPLOCK_MODE", Some(FixedArity(3))),
      (TSql, "APPLOCK_TEST", Some(FixedArity(4))),
      (TSql, "ASCII", Some(FixedArity(1))),
      (TSql, "ASIN", Some(FixedArity(1))),
      (TSql, "ASSEMBLYPROPERTY", Some(FixedArity(2))),
      (TSql, "ATAN", Some(FixedArity(1))),
      (TSql, "ATN2", Some(FixedArity(2))),
      (TSql, "CEILING", Some(FixedArity(1))),
      (TSql, "CERT_ID", Some(FixedArity(1))),
      (TSql, "CERTENCODED", Some(FixedArity(1))),
      (TSql, "CERTPRIVATEKEY", Some(VariableArity(2, 3))),
      (TSql, "CHAR", Some(FixedArity(1))),
      (TSql, "CHARINDEX", Some(VariableArity(2, 3))),
      (TSql, "CHECKSUM_AGG", Some(FixedArity(1))),
      (TSql, "COALESCE", Some(VariableArity(1, Int.MaxValue))),
      (TSql, "COL_LENGTH", Some(FixedArity(2))),
      (TSql, "COL_NAME", Some(FixedArity(2))),
      (TSql, "COLUMNPROPERTY", Some(FixedArity(3))),
      (TSql, "COMPRESS", Some(FixedArity(1))),
      (TSql, "CONCAT", Some(VariableArity(2, Int.MaxValue))),
      (TSql, "CONCAT_WS", Some(VariableArity(3, Int.MaxValue))),
      (TSql, "CONNECTIONPROPERTY", Some(FixedArity(1, convertible = false))),
      (TSql, "CONTEXT_INFO", Some(FixedArity(0))),
      (TSql, "CONVERT", Some(VariableArity(2, 3))),
      (TSql, "COS", Some(FixedArity(1))),
      (TSql, "COT", Some(FixedArity(1))),
      (TSql, "COUNT", Some(FixedArity(1))),
      (TSql, "COUNT_BIG", Some(FixedArity(1))),
      (TSql, "CURRENT_DATE", Some(FixedArity(0))),
      (TSql, "CURRENT_REQUEST_ID", Some(FixedArity(0))),
      (TSql, "CURRENT_TIMESTAMP", Some(FixedArity(0))),
      (TSql, "CURRENT_TIMEZONE", Some(FixedArity(0))),
      (TSql, "CURRENT_TIMEZONE_ID", Some(FixedArity(0))),
      (TSql, "CURRENT_TRANSACTION_ID", Some(FixedArity(0))),
      (TSql, "CURRENT_USER", Some(FixedArity(0))),
      (TSql, "CURSOR_STATUS", Some(FixedArity(2))),
      (TSql, "DATABASE_PRINCIPAL_ID", Some(VariableArity(0, 1))),
      (TSql, "DATABASEPROPERTY", Some(FixedArity(2))),
      (TSql, "DATABASEPROPERTYEX", Some(FixedArity(2))),
      (TSql, "DATALENGTH", Some(FixedArity(1))),
      (TSql, "DATE_BUCKET", Some(VariableArity(3, 4))),
      (TSql, "DATE_DIFF_BIG", Some(FixedArity(3))),
      (TSql, "DATEADD", Some(FixedArity(3))),
      (TSql, "DATEDIFF", Some(FixedArity(3))),
      (TSql, "DATEFROMPARTS", Some(FixedArity(3))),
      (TSql, "DATENAME", Some(FixedArity(2))),
      (TSql, "DATEPART", Some(FixedArity(2))),
      (TSql, "DATETIME2FROMPARTS", Some(FixedArity(8))),
      (TSql, "DATETIMEFROMPARTS", Some(FixedArity(7))),
      (TSql, "DATETIMEOFFSETFROMPARTS", Some(FixedArity(10))),
      (TSql, "DATETRUNC", Some(FixedArity(2))),
      (TSql, "DAY", Some(FixedArity(1))),
      (TSql, "DB_ID", Some(VariableArity(0, 1))),
      (TSql, "DB_NAME", Some(VariableArity(0, 1))),
      (TSql, "DECOMPRESS", Some(FixedArity(1))),
      (TSql, "DEGREES", Some(FixedArity(1))),
      (TSql, "DENSE_RANK", Some(FixedArity(0))),
      (TSql, "DIFFERENCE", Some(FixedArity(2))),
      (TSql, "EOMONTH", Some(VariableArity(1, 2))),
      (TSql, "ERROR_LINE", Some(FixedArity(0))),
      (TSql, "ERROR_MESSAGE", Some(FixedArity(0))),
      (TSql, "ERROR_NUMBER", Some(FixedArity(0))),
      (TSql, "ERROR_PROCEDURE", Some(FixedArity(0))),
      (TSql, "ERROR_SEVERITY", Some(FixedArity(0))),
      (TSql, "ERROR_STATE", Some(FixedArity(0))),
      (TSql, "EXIST", Some(FixedArity(1, XmlFunction))),
      (TSql, "EXP", Some(FixedArity(1))),
      (TSql, "FILE_ID", Some(FixedArity(1))),
      (TSql, "FILE_IDEX", Some(FixedArity(1))),
      (TSql, "FILE_NAME", Some(FixedArity(1))),
      (TSql, "FILEGROUP_ID", Some(FixedArity(1))),
      (TSql, "FILEGROUP_NAME", Some(FixedArity(1))),
      (TSql, "FILEGROUPPROPERTY", Some(FixedArity(2))),
      (TSql, "FILEPROPERTY", Some(FixedArity(2))),
      (TSql, "FILEPROPERTYEX", Some(FixedArity(2))),
      (TSql, "FLOOR", Some(FixedArity(1))),
      (TSql, "FORMAT", Some(VariableArity(2, 3))),
      (TSql, "FORMATMESSAGE", Some(VariableArity(2, Int.MaxValue))),
      (TSql, "FULLTEXTCATALOGPROPERTY", Some(FixedArity(2))),
      (TSql, "FULLTEXTSERVICEPROPERTY", Some(FixedArity(1))),
      (TSql, "GET_FILESTREAM_TRANSACTION_CONTEXT", Some(FixedArity(0))),
      (TSql, "GETANCESTGOR", Some(FixedArity(1))),
      (TSql, "GETANSINULL", Some(VariableArity(0, 1))),
      (TSql, "GETDATE", Some(FixedArity(0))),
      (TSql, "GETDESCENDANT", Some(FixedArity(2))),
      (TSql, "GETLEVEL", Some(FixedArity(0))),
      (TSql, "GETREPARENTEDVALUE", Some(FixedArity(2))),
      (TSql, "GETUTCDATE", Some(FixedArity(0))),
      (TSql, "GREATEST", Some(VariableArity(1, Int.MaxValue))),
      (TSql, "GROUPING", Some(FixedArity(1))),
      (TSql, "GROUPING_ID", Some(VariableArity(0, Int.MaxValue))),
      (TSql, "HAS_DBACCESS", Some(FixedArity(1))),
      (TSql, "HAS_PERMS_BY_NAME", Some(VariableArity(4, 5))),
      (TSql, "HOST_ID", Some(FixedArity(0))),
      (TSql, "HOST_NAME", Some(FixedArity(0))),
      (TSql, "IDENT_CURRENT", Some(FixedArity(1))),
      (TSql, "IDENT_INCR", Some(FixedArity(1))),
      (TSql, "IDENT_SEED", Some(FixedArity(1))),
      (TSql, "IFF", Some(FixedArity(3))),
      (Snowflake, "IFNULL", Some(FixedArity(2))),
      (TSql, "INDEX_COL", Some(FixedArity(3))),
      (TSql, "INDEXKEY_PROPERTY", Some(FixedArity(3))),
      (TSql, "INDEXPROPERTY", Some(FixedArity(3))),
      (TSql, "IS_MEMBER", Some(FixedArity(1))),
      (TSql, "IS_ROLEMEMBER", Some(VariableArity(1, 2))),
      (TSql, "IS_SRVROLEMEMBER", Some(VariableArity(1, 2))),
      (TSql, "ISDATE", Some(FixedArity(1))),
      (TSql, "ISDESCENDANTOF", Some(FixedArity(1))),
      (TSql, "ISJSON", Some(VariableArity(1, 2))),
      (TSql, "ISNULL", Some(VariableArity(1, 2, conversionStrategy = Some(FunctionConverters.FunctionRename)))),
      (TSql, "ISNUMERIC", Some(FixedArity(1))),
      (TSql, "JSON_MODIFY", Some(FixedArity(3))),
      (TSql, "JSON_PATH_EXISTS", Some(FixedArity(2))),
      (TSql, "JSON_QUERY", Some(FixedArity(2))),
      (TSql, "JSON_VALUE", Some(FixedArity(2))),
      (TSql, "LEAST", Some(VariableArity(1, Int.MaxValue))),
      (TSql, "LEFT", Some(FixedArity(2))),
      (TSql, "LEN", Some(FixedArity(1))),
      (TSql, "LOG", Some(VariableArity(1, 2))),
      (TSql, "LOG10", Some(FixedArity(1))),
      (TSql, "LOGINPROPERTY", Some(FixedArity(2))),
      (TSql, "LOWER", Some(FixedArity(1))),
      (TSql, "LTRIM", Some(FixedArity(1))),
      (TSql, "MAX", Some(FixedArity(1))),
      (TSql, "MIN", Some(FixedArity(1))),
      (TSql, "MIN_ACTIVE_ROWVERSION", Some(FixedArity(0))),
      (TSql, "MONTH", Some(FixedArity(1))),
      (TSql, "NCHAR", Some(FixedArity(1))),
      (TSql, "NEWID", Some(FixedArity(0))),
      (TSql, "NEWSEQUENTIALID", Some(FixedArity(0))),
      (TSql, "NODES", Some(FixedArity(1, XmlFunction))),
      (TSql, "NTILE", Some(FixedArity(1))),
      (TSql, "NULLIF", Some(FixedArity(2))),
      (TSql, "OBJECT_DEFINITION", Some(FixedArity(1))),
      (TSql, "OBJECT_ID", Some(VariableArity(1, 2))),
      (TSql, "OBJECT_NAME", Some(VariableArity(1, 2))),
      (TSql, "OBJECT_SCHEMA_NAME", Some(VariableArity(1, 2))),
      (TSql, "OBJECTPROPERTY", Some(FixedArity(2))),
      (TSql, "OBJECTPROPERTYEX", Some(FixedArity(2))),
      (TSql, "ORIGINAL_DB_NAME", Some(FixedArity(0))),
      (TSql, "ORIGINAL_LOGIN", Some(FixedArity(0))),
      (TSql, "PARSE", Some(VariableArity(2, 3, convertible = false))),
      (TSql, "PARSENAME", Some(FixedArity(2))),
      (TSql, "PATINDEX", Some(FixedArity(2))),
      (TSql, "PERMISSIONS", Some(VariableArity(0, 2, convertible = false))),
      (TSql, "PI", Some(FixedArity(0))),
      (TSql, "POWER", Some(FixedArity(2))),
      (TSql, "PWDCOMPARE", Some(VariableArity(2, 3))),
      (TSql, "PWDENCRYPT", Some(FixedArity(1))),
      (TSql, "QUERY", Some(FixedArity(1, XmlFunction))),
      (TSql, "QUOTENAME", Some(VariableArity(1, 2))),
      (TSql, "RADIANS", Some(FixedArity(1))),
      (TSql, "RAND", Some(VariableArity(0, 1))),
      (TSql, "RANK", Some(FixedArity(0))),
      (TSql, "REPLACE", Some(FixedArity(3))),
      (TSql, "REPLICATE", Some(FixedArity(2))),
      (TSql, "REVERSE", Some(FixedArity(1))),
      (TSql, "RIGHT", Some(FixedArity(2))),
      (TSql, "ROUND", Some(VariableArity(2, 3))),
      (TSql, "ROWCOUNT_BIG", Some(FixedArity(0))),
      (TSql, "RTRIM", Some(FixedArity(1))),
      (TSql, "SCHEMA_ID", Some(VariableArity(0, 1))),
      (TSql, "SCHEMA_NAME", Some(VariableArity(0, 1))),
      (TSql, "SCOPE_IDENTITY", Some(FixedArity(0))),
      (TSql, "SERVERPROPERTY", Some(FixedArity(1))),
      (TSql, "SESSION_CONTEXT", Some(VariableArity(1, 2))),
      (TSql, "SESSIONPROPERTY", Some(FixedArity(1))),
      (TSql, "SIGN", Some(FixedArity(1))),
      (TSql, "SIN", Some(FixedArity(1))),
      (TSql, "SMALLDATETIMEFROMPARTS", Some(FixedArity(5))),
      (TSql, "SOUNDEX", Some(FixedArity(1))),
      (TSql, "SPACE", Some(FixedArity(1))),
      (TSql, "SQL_VARIANT_PROPERTY", Some(FixedArity(2))),
      (TSql, "SQRT", Some(FixedArity(1))),
      (TSql, "SQUARE", Some(FixedArity(1))),
      (TSql, "STATS_DATE", Some(FixedArity(2))),
      (TSql, "STDEV", Some(FixedArity(1))),
      (TSql, "STDEVP", Some(FixedArity(1))),
      (TSql, "STR", Some(VariableArity(1, 3))),
      (TSql, "STRING_AGG", Some(VariableArity(2, 3))),
      (TSql, "STRING_ESCAPE", Some(FixedArity(2))),
      (TSql, "STUFF", Some(FixedArity(4))),
      (TSql, "SUBSTRING", Some(VariableArity(2, 3))),
      (TSql, "SUSER_ID", Some(VariableArity(0, 1))),
      (TSql, "SUSER_NAME", Some(VariableArity(0, 1))),
      (TSql, "SUSER_SID", Some(VariableArity(0, 2))),
      (TSql, "SUSER_SNAME", Some(VariableArity(0, 1))),
      (TSql, "SWITCHOFFSET", Some(FixedArity(2))),
      (TSql, "SYSDATETIME", Some(FixedArity(0))),
      (TSql, "SYSDATETIMEOFFSET", Some(FixedArity(0))),
      (TSql, "SYSUTCDATETIME", Some(FixedArity(0))),
      (TSql, "TAN", Some(FixedArity(1))),
      (TSql, "TIMEFROMPARTS", Some(FixedArity(5))),
      (TSql, "TODATETIMEOFFSET", Some(FixedArity(2))),
      (TSql, "TOSTRING", Some(FixedArity(0))),
      (TSql, "TRANSLATE", Some(FixedArity(3))),
      (TSql, "TRIM", Some(VariableArity(1, 2))),
      (TSql, "TYPE_ID", Some(FixedArity(1))),
      (TSql, "TYPE_NAME", Some(FixedArity(1))),
      (TSql, "TYPEPROPERTY", Some(FixedArity(2))),
      (TSql, "UNICODE", Some(FixedArity(1))),
      (TSql, "UPPER", Some(FixedArity(1))),
      (TSql, "USER_ID", Some(VariableArity(0, 1))),
      (TSql, "USER_NAME", Some(VariableArity(0, 1))),
      (TSql, "VAR", Some(FixedArity(1))),
      (TSql, "VARP", Some(FixedArity(1))),
      (TSql, "XACT_STATE", Some(FixedArity(0))),
      (TSql, "YEAR", Some(FixedArity(1))))

    forAll(functions) { (dialect: SqlDialect, functionName: String, expectedArity: Option[FunctionArity]) =>
      FunctionBuilder.functionArity(dialect, functionName) shouldEqual expectedArity
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

  "functionArity" should "build with all possible parameter combinations" in {
    val functionTypes = List(StandardFunction, XmlFunction)

    val fixedArityInstances = for {
      convertible <- List(true, false)
      functionType <- functionTypes
    } yield FixedArity(1, functionType, convertible)

    val variableArityInstances = for {
      convertible <- List(true, false)
      functionType <- functionTypes
    } yield VariableArity(1, 2, functionType, convertible)

    val allInstances = fixedArityInstances ++ variableArityInstances
    assert(allInstances.size == 8)
  }

  "isConvertible method in FunctionArity" should "return true by default" in {
    val fixedArity = FixedArity(arity = 1)
    fixedArity.isConvertible should be(true)

    val variableArity = VariableArity(argMin = 1, argMax = 2)
    variableArity.isConvertible should be(true)

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
