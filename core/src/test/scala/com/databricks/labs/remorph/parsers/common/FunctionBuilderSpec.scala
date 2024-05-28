package com.databricks.labs.remorph.parsers.common

import com.databricks.labs.remorph.parsers.{FixedArity, FunctionArity, FunctionBuilder, FunctionType, StandardFunction, UnknownFunction, VariableArity, XmlFunction}
import org.scalatest.flatspec.AnyFlatSpec
import org.scalatest.matchers.should.Matchers
import org.scalatest.prop.TableDrivenPropertyChecks

class FunctionBuilderSpec extends AnyFlatSpec with Matchers with TableDrivenPropertyChecks {

  // While this appears to be somewhat redundant, it will catch any changes in the functionArity method
  // that happen through typos or other mistakes such as deletion.
  "functionArity" should "return correct arity for each function" in {
    val functions = Table(
      ("functionName", "expectedArity"), // Header

      ("MODIFY", Some(FixedArity(1, XmlFunction))),
      ("ABS", Some(FixedArity(1))),
      ("ACOS", Some(FixedArity(1))),
      ("APP_NAME", Some(FixedArity(0))),
      ("APPLOCK_MODE", Some(FixedArity(3))),
      ("APPLOCK_TEST", Some(FixedArity(4))),
      ("ASCII", Some(FixedArity(1))),
      ("ASIN", Some(FixedArity(1))),
      ("ASSEMBLYPROPERTY", Some(FixedArity(2))),
      ("ATAN", Some(FixedArity(1))),
      ("ATN2", Some(FixedArity(2))),
      ("CEILING", Some(FixedArity(1))),
      ("CERT_ID", Some(FixedArity(1))),
      ("CERTENCODED", Some(FixedArity(1))),
      ("CERTPRIVATEKEY", Some(VariableArity(2, 3))),
      ("CHAR", Some(FixedArity(1))),
      ("CHARINDEX", Some(VariableArity(2, 3))),
      ("CHECKSUM_AGG", Some(FixedArity(1))),
      ("COALESCE", Some(VariableArity(1, Int.MaxValue))),
      ("COL_LENGTH", Some(FixedArity(2))),
      ("COL_NAME", Some(FixedArity(2))),
      ("COLUMNPROPERTY", Some(FixedArity(3))),
      ("COMPRESS", Some(FixedArity(1))),
      ("CONCAT", Some(VariableArity(2, Int.MaxValue))),
      ("CONCAT_WS", Some(VariableArity(3, Int.MaxValue))),
      ("CONNECTIONPROPERTY", Some(FixedArity(1, convertible = false))),
      ("CONTEXT_INFO", Some(FixedArity(0))),
      ("CONVERT", Some(VariableArity(2, 3))),
      ("COS", Some(FixedArity(1))),
      ("COT", Some(FixedArity(1))),
      ("COUNT", Some(FixedArity(1))),
      ("COUNT_BIG", Some(FixedArity(1))),
      ("CURRENT_DATE", Some(FixedArity(0))),
      ("CURRENT_REQUEST_ID", Some(FixedArity(0))),
      ("CURRENT_TIMESTAMP", Some(FixedArity(0))),
      ("CURRENT_TIMEZONE", Some(FixedArity(0))),
      ("CURRENT_TIMEZONE_ID", Some(FixedArity(0))),
      ("CURRENT_TRANSACTION_ID", Some(FixedArity(0))),
      ("CURRENT_USER", Some(FixedArity(0))),
      ("CURSOR_STATUS", Some(FixedArity(2))),
      ("DATABASE_PRINCIPAL_ID", Some(VariableArity(0, 1))),
      ("DATABASEPROPERTY", Some(FixedArity(2))),
      ("DATABASEPROPERTYEX", Some(FixedArity(2))),
      ("DATALENGTH", Some(FixedArity(1))),
      ("DATE_BUCKET", Some(VariableArity(3, 4))),
      ("DATE_DIFF_BIG", Some(FixedArity(3))),
      ("DATEADD", Some(FixedArity(3))),
      ("DATEDIFF", Some(FixedArity(3))),
      ("DATEFROMPARTS", Some(FixedArity(3))),
      ("DATENAME", Some(FixedArity(2))),
      ("DATEPART", Some(FixedArity(2))),
      ("DATETIME2FROMPARTS", Some(FixedArity(8))),
      ("DATETIMEFROMPARTS", Some(FixedArity(7))),
      ("DATETIMEOFFSETFROMPARTS", Some(FixedArity(10))),
      ("DATETRUNC", Some(FixedArity(2))),
      ("DAY", Some(FixedArity(1))),
      ("DB_ID", Some(VariableArity(0, 1))),
      ("DB_NAME", Some(VariableArity(0, 1))),
      ("DECOMPRESS", Some(FixedArity(1))),
      ("DEGREES", Some(FixedArity(1))),
      ("DENSE_RANK", Some(FixedArity(0))),
      ("DIFFERENCE", Some(FixedArity(2))),
      ("EOMONTH", Some(VariableArity(1, 2))),
      ("ERROR_LINE", Some(FixedArity(0))),
      ("ERROR_MESSAGE", Some(FixedArity(0))),
      ("ERROR_NUMBER", Some(FixedArity(0))),
      ("ERROR_PROCEDURE", Some(FixedArity(0))),
      ("ERROR_SEVERITY", Some(FixedArity(0))),
      ("ERROR_STATE", Some(FixedArity(0))),
      ("EXIST", Some(FixedArity(1, XmlFunction))),
      ("EXP", Some(FixedArity(1))),
      ("FILE_ID", Some(FixedArity(1))),
      ("FILE_IDEX", Some(FixedArity(1))),
      ("FILE_NAME", Some(FixedArity(1))),
      ("FILEGROUP_ID", Some(FixedArity(1))),
      ("FILEGROUP_NAME", Some(FixedArity(1))),
      ("FILEGROUPPROPERTY", Some(FixedArity(2))),
      ("FILEPROPERTY", Some(FixedArity(2))),
      ("FILEPROPERTYEX", Some(FixedArity(2))),
      ("FLOOR", Some(FixedArity(1))),
      ("FORMAT", Some(VariableArity(2, 3))),
      ("FORMATMESSAGE", Some(VariableArity(2, Int.MaxValue))),
      ("FULLTEXTCATALOGPROPERTY", Some(FixedArity(2))),
      ("FULLTEXTSERVICEPROPERTY", Some(FixedArity(1))),
      ("GET_FILESTREAM_TRANSACTION_CONTEXT", Some(FixedArity(0))),
      ("GETANCESTGOR", Some(FixedArity(1))),
      ("GETANSINULL", Some(VariableArity(0, 1))),
      ("GETDATE", Some(FixedArity(0))),
      ("GETDESCENDANT", Some(FixedArity(2))),
      ("GETLEVEL", Some(FixedArity(0))),
      ("GETREPARENTEDVALUE", Some(FixedArity(2))),
      ("GETUTCDATE", Some(FixedArity(0))),
      ("GREATEST", Some(VariableArity(1, Int.MaxValue))),
      ("GROUPING", Some(FixedArity(1))),
      ("GROUPING_ID", Some(VariableArity(0, Int.MaxValue))),
      ("HAS_DBACCESS", Some(FixedArity(1))),
      ("HAS_PERMS_BY_NAME", Some(VariableArity(4, 5))),
      ("HOST_ID", Some(FixedArity(0))),
      ("HOST_NAME", Some(FixedArity(0))),
      ("IDENT_CURRENT", Some(FixedArity(1))),
      ("IDENT_INCR", Some(FixedArity(1))),
      ("IDENT_SEED", Some(FixedArity(1))),
      ("IFF", Some(FixedArity(3))),
      ("INDEX_COL", Some(FixedArity(3))),
      ("INDEXKEY_PROPERTY", Some(FixedArity(3))),
      ("INDEXPROPERTY", Some(FixedArity(3))),
      ("IS_MEMBER", Some(FixedArity(1))),
      ("IS_ROLEMEMBER", Some(VariableArity(1, 2))),
      ("IS_SRVROLEMEMBER", Some(VariableArity(1, 2))),
      ("ISDATE", Some(FixedArity(1))),
      ("ISDESCENDANTOF", Some(FixedArity(1))),
      ("ISJSON", Some(VariableArity(1, 2))),
      ("ISNULL", Some(FixedArity(2))),
      ("ISNUMERIC", Some(FixedArity(1))),
      ("JSON_MODIFY", Some(FixedArity(3))),
      ("JSON_PATH_EXISTS", Some(FixedArity(2))),
      ("JSON_QUERY", Some(FixedArity(2))),
      ("JSON_VALUE", Some(FixedArity(2))),
      ("LEAST", Some(VariableArity(1, Int.MaxValue))),
      ("LEFT", Some(FixedArity(2))),
      ("LEN", Some(FixedArity(1))),
      ("LOG", Some(VariableArity(1, 2))),
      ("LOG10", Some(FixedArity(1))),
      ("LOGINPROPERTY", Some(FixedArity(2))),
      ("LOWER", Some(FixedArity(1))),
      ("LTRIM", Some(FixedArity(1))),
      ("MAX", Some(FixedArity(1))),
      ("MIN", Some(FixedArity(1))),
      ("MIN_ACTIVE_ROWVERSION", Some(FixedArity(0))),
      ("MONTH", Some(FixedArity(1))),
      ("NCHAR", Some(FixedArity(1))),
      ("NEWID", Some(FixedArity(0))),
      ("NEWSEQUENTIALID", Some(FixedArity(0))),
      ("NODES", Some(FixedArity(1, XmlFunction))),
      ("NTILE", Some(FixedArity(1))),
      ("NULLIF", Some(FixedArity(2))),
      ("OBJECT_DEFINITION", Some(FixedArity(1))),
      ("OBJECT_ID", Some(VariableArity(1, 2))),
      ("OBJECT_NAME", Some(VariableArity(1, 2))),
      ("OBJECT_SCHEMA_NAME", Some(VariableArity(1, 2))),
      ("OBJECTPROPERTY", Some(FixedArity(2))),
      ("OBJECTPROPERTYEX", Some(FixedArity(2))),
      ("ORIGINAL_DB_NAME", Some(FixedArity(0))),
      ("ORIGINAL_LOGIN", Some(FixedArity(0))),
      ("PARSE", Some(VariableArity(2, 3, convertible = false))),
      ("PARSENAME", Some(FixedArity(2))),
      ("PATINDEX", Some(FixedArity(2))),
      ("PERMISSIONS", Some(VariableArity(0, 2, convertible = false))),
      ("PI", Some(FixedArity(0))),
      ("POWER", Some(FixedArity(2))),
      ("PWDCOMPARE", Some(VariableArity(2, 3))),
      ("PWDENCRYPT", Some(FixedArity(1))),
      ("QUERY", Some(FixedArity(1, XmlFunction))),
      ("QUOTENAME", Some(VariableArity(1, 2))),
      ("RADIANS", Some(FixedArity(1))),
      ("RAND", Some(VariableArity(0, 1))),
      ("RANK", Some(FixedArity(0))),
      ("REPLACE", Some(FixedArity(3))),
      ("REPLICATE", Some(FixedArity(2))),
      ("REVERSE", Some(FixedArity(1))),
      ("RIGHT", Some(FixedArity(2))),
      ("ROUND", Some(VariableArity(2, 3))),
      ("ROWCOUNT_BIG", Some(FixedArity(0))),
      ("RTRIM", Some(FixedArity(1))),
      ("SCHEMA_ID", Some(VariableArity(0, 1))),
      ("SCHEMA_NAME", Some(VariableArity(0, 1))),
      ("SCOPE_IDENTITY", Some(FixedArity(0))),
      ("SERVERPROPERTY", Some(FixedArity(1))),
      ("SESSION_CONTEXT", Some(VariableArity(1, 2))),
      ("SESSIONPROPERTY", Some(FixedArity(1))),
      ("SIGN", Some(FixedArity(1))),
      ("SIN", Some(FixedArity(1))),
      ("SMALLDATETIMEFROMPARTS", Some(FixedArity(5))),
      ("SOUNDEX", Some(FixedArity(1))),
      ("SPACE", Some(FixedArity(1))),
      ("SQL_VARIANT_PROPERTY", Some(FixedArity(2))),
      ("SQRT", Some(FixedArity(1))),
      ("SQUARE", Some(FixedArity(1))),
      ("STATS_DATE", Some(FixedArity(2))),
      ("STDEV", Some(FixedArity(1))),
      ("STDEVP", Some(FixedArity(1))),
      ("STR", Some(VariableArity(1, 3))),
      ("STRING_AGG", Some(VariableArity(2, 3))),
      ("STRING_ESCAPE", Some(FixedArity(2))),
      ("STUFF", Some(FixedArity(4))),
      ("SUBSTRING", Some(VariableArity(2, 3))),
      ("SUSER_ID", Some(VariableArity(0, 1))),
      ("SUSER_NAME", Some(VariableArity(0, 1))),
      ("SUSER_SID", Some(VariableArity(0, 2))),
      ("SUSER_SNAME", Some(VariableArity(0, 1))),
      ("SWITCHOFFSET", Some(FixedArity(2))),
      ("SYSDATETIME", Some(FixedArity(0))),
      ("SYSDATETIMEOFFSET", Some(FixedArity(0))),
      ("SYSUTCDATETIME", Some(FixedArity(0))),
      ("TAN", Some(FixedArity(1))),
      ("TIMEFROMPARTS", Some(FixedArity(5))),
      ("TODATETIMEOFFSET", Some(FixedArity(2))),
      ("TOSTRING", Some(FixedArity(0))),
      ("TRANSLATE", Some(FixedArity(3))),
      ("TRIM", Some(VariableArity(1, 2))),
      ("TYPE_ID", Some(FixedArity(1))),
      ("TYPE_NAME", Some(FixedArity(1))),
      ("TYPEPROPERTY", Some(FixedArity(2))),
      ("UNICODE", Some(FixedArity(1))),
      ("UPPER", Some(FixedArity(1))),
      ("USER_ID", Some(VariableArity(0, 1))),
      ("USER_NAME", Some(VariableArity(0, 1))),
      ("VAR", Some(FixedArity(1))),
      ("VARP", Some(FixedArity(1))),
      ("XACT_STATE", Some(FixedArity(0))),
      ("YEAR", Some(FixedArity(1))))

    forAll(functions) { (functionName: String, expectedArity: Option[FunctionArity]) =>
      FunctionBuilder.functionArity(functionName) shouldEqual expectedArity
    }
  }

  "functionType" should "return correct function type for each function" in {
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
    forAll(functions) { (functionName: String, expectedFunctionType: FunctionType) =>
      FunctionBuilder.functionType(functionName) shouldEqual expectedFunctionType
    }
  }

  "functionType" should "return UnknownFunction for functions that do not exist" in {
    val result = FunctionBuilder.functionType("DOES_NOT_EXIST")
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

}
