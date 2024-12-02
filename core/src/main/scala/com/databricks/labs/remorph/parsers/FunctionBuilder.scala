package com.databricks.labs.remorph.parsers

import com.databricks.labs.remorph.parsers.snowflake.NamedArgumentExpression
import com.databricks.labs.remorph.parsers.snowflake.SnowflakeFunctionConverters.SynonymOf
import com.databricks.labs.remorph.{intermediate => ir}

sealed trait FunctionType
case object StandardFunction extends FunctionType
case object XmlFunction extends FunctionType
case object NotConvertibleFunction extends FunctionType
case object UnknownFunction extends FunctionType

sealed trait FunctionArity

// For functions with a fixed number of arguments (ie. all arguments are required)
case class FixedArity(arity: Int) extends FunctionArity
// For functions with a varying number of arguments (ie. some arguments are optional)
case class VariableArity(argMin: Int, argMax: Int) extends FunctionArity
// For functions with named arguments (ie. some arguments are optional and arguments may be provided in any order)
case class SymbolicArity(requiredArguments: Set[String], optionalArguments: Set[String]) extends FunctionArity

object FunctionArity {
  def verifyArguments(arity: FunctionArity, args: Seq[ir.Expression]): Boolean = arity match {
    case FixedArity(n) => args.size == n
    case VariableArity(argMin, argMax) => argMin <= args.size && args.size <= argMax
    case SymbolicArity(required, optional) =>
      val namedArguments = args.collect { case n: NamedArgumentExpression => n }
      // all provided arguments are named
      if (namedArguments.size == args.size) {
        // all required arguments are present
        required.forall(r => namedArguments.exists(_.key.toUpperCase() == r.toUpperCase())) &&
        // no unexpected argument was provided
        namedArguments.forall(na => (required ++ optional).map(_.toUpperCase()).contains(na.key.toUpperCase()))
      } else if (namedArguments.isEmpty) {
        // arguments were provided positionally
        args.size >= required.size && args.size <= required.size + optional.size
      } else {
        // a mix of named and positional arguments were provided, which isn't supported
        false
      }
  }
}

case class FunctionDefinition(
    arity: FunctionArity,
    functionType: FunctionType,
    conversionStrategy: Option[ConversionStrategy] = None) {
  def withConversionStrategy(strategy: ConversionStrategy): FunctionDefinition =
    copy(conversionStrategy = Some(strategy))
}

object FunctionDefinition {
  def standard(fixedArgNumber: Int): FunctionDefinition =
    FunctionDefinition(FixedArity(fixedArgNumber), StandardFunction)
  def standard(minArg: Int, maxArg: Int): FunctionDefinition =
    FunctionDefinition(VariableArity(minArg, maxArg), StandardFunction)

  def symbolic(required: Set[String], optional: Set[String]): FunctionDefinition =
    FunctionDefinition(SymbolicArity(required, optional), StandardFunction)

  def xml(fixedArgNumber: Int): FunctionDefinition =
    FunctionDefinition(FixedArity(fixedArgNumber), XmlFunction)

  def notConvertible(fixedArgNumber: Int): FunctionDefinition =
    FunctionDefinition(FixedArity(fixedArgNumber), NotConvertibleFunction)
  def notConvertible(minArg: Int, maxArg: Int): FunctionDefinition =
    FunctionDefinition(VariableArity(minArg, maxArg), NotConvertibleFunction)
}

abstract class FunctionBuilder {

  protected val commonFunctionsPf: PartialFunction[String, FunctionDefinition] = {
    case "ABS" => FunctionDefinition.standard(1)
    case "ACOS" => FunctionDefinition.standard(1)
    case "APP_NAME" => FunctionDefinition.standard(0)
    case "APPLOCK_MODE" => FunctionDefinition.standard(3)
    case "APPLOCK_TEST" => FunctionDefinition.standard(4)
    case "APPROX_COUNT_DISTINCT" => FunctionDefinition.standard(1)
    case "APPROX_PERCENTILE" => FunctionDefinition.standard(2)
    case "APPROX_PERCENTILE_CONT" => FunctionDefinition.standard(1)
    case "APPROX_PERCENTILE_DISC" => FunctionDefinition.standard(1)
    case "ARRAYAGG" => FunctionDefinition.standard(1)
    case "ASCII" => FunctionDefinition.standard(1)
    case "ASIN" => FunctionDefinition.standard(1)
    case "ASSEMBLYPROPERTY" => FunctionDefinition.standard(2)
    case "ATAN" => FunctionDefinition.standard(1)
    case "ATN2" => FunctionDefinition.standard(2)
    case "AVG" => FunctionDefinition.standard(1)
    case "BINARY_CHECKSUM" => FunctionDefinition.standard(1, Int.MaxValue)
    case "BIT_COUNT" => FunctionDefinition.standard(1)
    case "CEILING" => FunctionDefinition.standard(1)
    case "CERT_ID" => FunctionDefinition.standard(1)
    case "CERTENCODED" => FunctionDefinition.standard(1)
    case "CERTPRIVATEKEY" => FunctionDefinition.standard(2, 3)
    case "CHAR" => FunctionDefinition.standard(1)
    case "CHARINDEX" => FunctionDefinition.standard(2, 3)
    case "CHECKSUM" => FunctionDefinition.standard(2, Int.MaxValue)
    case "CHECKSUM_AGG" => FunctionDefinition.standard(1)
    case "COALESCE" => FunctionDefinition.standard(1, Int.MaxValue)
    case "COL_LENGTH" => FunctionDefinition.standard(2)
    case "COL_NAME" => FunctionDefinition.standard(2)
    case "COLUMNPROPERTY" => FunctionDefinition.standard(3)
    case "COMPRESS" => FunctionDefinition.standard(1)
    case "CONCAT" => FunctionDefinition.standard(2, Int.MaxValue)
    case "CONCAT_WS" => FunctionDefinition.standard(3, Int.MaxValue)
    case "CONNECTIONPROPERTY" => FunctionDefinition.notConvertible(1)
    case "CONTEXT_INFO" => FunctionDefinition.standard(0)
    case "CONVERT" => FunctionDefinition.standard(2, 3)
    case "COS" => FunctionDefinition.standard(1)
    case "COT" => FunctionDefinition.standard(1)
    case "COUNT" => FunctionDefinition.standard(1)
    case "COUNT_BIG" => FunctionDefinition.standard(1)
    case "CUME_DIST" => FunctionDefinition.standard(0)
    case "CURRENT_DATE" => FunctionDefinition.standard(0)
    case "CURRENT_REQUEST_ID" => FunctionDefinition.standard(0)
    case "CURRENT_TIMESTAMP" => FunctionDefinition.standard(0)
    case "CURRENT_TIMEZONE" => FunctionDefinition.standard(0)
    case "CURRENT_TIMEZONE_ID" => FunctionDefinition.standard(0)
    case "CURRENT_TRANSACTION_ID" => FunctionDefinition.standard(0)
    case "CURRENT_USER" => FunctionDefinition.standard(0)
    case "CURSOR_ROWS" => FunctionDefinition.standard(0)
    case "CURSOR_STATUS" => FunctionDefinition.standard(2)
    case "DATABASE_PRINCIPAL_ID" => FunctionDefinition.standard(0, 1)
    case "DATABASEPROPERTY" => FunctionDefinition.standard(2)
    case "DATABASEPROPERTYEX" => FunctionDefinition.standard(2)
    case "DATALENGTH" => FunctionDefinition.standard(1)
    case "DATE_BUCKET" => FunctionDefinition.standard(3, 4)
    case "DATE_DIFF_BIG" => FunctionDefinition.standard(3)
    case "DATEADD" => FunctionDefinition.standard(3)
    case "DATEDIFF" => FunctionDefinition.standard(3)
    case "DATEFROMPARTS" => FunctionDefinition.standard(3)
    case "DATE_FORMAT" => FunctionDefinition.standard(2)
    case "DATENAME" => FunctionDefinition.standard(2)
    case "DATEPART" => FunctionDefinition.standard(2)
    case "DATETIME2FROMPARTS" => FunctionDefinition.standard(8)
    case "DATETIMEFROMPARTS" => FunctionDefinition.standard(7)
    case "DATETIMEOFFSETFROMPARTS" => FunctionDefinition.standard(10)
    case "DATETRUNC" => FunctionDefinition.standard(2)
    case "DAY" => FunctionDefinition.standard(1)
    case "DB_ID" => FunctionDefinition.standard(0, 1)
    case "DB_NAME" => FunctionDefinition.standard(0, 1)
    case "DECOMPRESS" => FunctionDefinition.standard(1)
    case "DEGREES" => FunctionDefinition.standard(1)
    case "DENSE_RANK" => FunctionDefinition.standard(0)
    case "DIFFERENCE" => FunctionDefinition.standard(2)
    case "EOMONTH" => FunctionDefinition.standard(1, 2)
    case "ERROR_LINE" => FunctionDefinition.standard(0)
    case "ERROR_MESSAGE" => FunctionDefinition.standard(0)
    case "ERROR_NUMBER" => FunctionDefinition.standard(0)
    case "ERROR_PROCEDURE" => FunctionDefinition.standard(0)
    case "ERROR_SEVERITY" => FunctionDefinition.standard(0)
    case "ERROR_STATE" => FunctionDefinition.standard(0)
    case "EXIST" => FunctionDefinition.xml(1)
    case "EXP" => FunctionDefinition.standard(1)
    case "FILE_ID" => FunctionDefinition.standard(1)
    case "FILE_IDEX" => FunctionDefinition.standard(1)
    case "FILE_NAME" => FunctionDefinition.standard(1)
    case "FILEGROUP_ID" => FunctionDefinition.standard(1)
    case "FILEGROUP_NAME" => FunctionDefinition.standard(1)
    case "FILEGROUPPROPERTY" => FunctionDefinition.standard(2)
    case "FILEPROPERTY" => FunctionDefinition.standard(2)
    case "FILEPROPERTYEX" => FunctionDefinition.standard(2)
    case "FIRST_VALUE" => FunctionDefinition.standard(1)
    case "FLOOR" => FunctionDefinition.standard(1)
    case "FORMAT" => FunctionDefinition.standard(2, 3)
    case "FORMATMESSAGE" => FunctionDefinition.standard(2, Int.MaxValue)
    case "FULLTEXTCATALOGPROPERTY" => FunctionDefinition.standard(2)
    case "FULLTEXTSERVICEPROPERTY" => FunctionDefinition.standard(1)
    case "GET_FILESTREAM_TRANSACTION_CONTEXT" => FunctionDefinition.standard(0)
    case "GETANCESTGOR" => FunctionDefinition.standard(1)
    case "GETANSINULL" => FunctionDefinition.standard(0, 1)
    case "GETDATE" => FunctionDefinition.standard(0)
    case "GETDESCENDANT" => FunctionDefinition.standard(2)
    case "GETLEVEL" => FunctionDefinition.standard(0)
    case "GETREPARENTEDVALUE" => FunctionDefinition.standard(2)
    case "GETUTCDATE" => FunctionDefinition.standard(0)
    case "GREATEST" => FunctionDefinition.standard(1, Int.MaxValue)
    case "GROUPING" => FunctionDefinition.standard(1)
    case "GROUPING_ID" => FunctionDefinition.standard(0, Int.MaxValue)
    case "HAS_DBACCESS" => FunctionDefinition.standard(1)
    case "HAS_PERMS_BY_NAME" => FunctionDefinition.standard(4, 5)
    case "HOST_ID" => FunctionDefinition.standard(0)
    case "HOST_NAME" => FunctionDefinition.standard(0)
    case "IDENT_CURRENT" => FunctionDefinition.standard(1)
    case "IDENT_INCR" => FunctionDefinition.standard(1)
    case "IDENT_SEED" => FunctionDefinition.standard(1)
    case "IDENTITY" => FunctionDefinition.standard(1, 3)
    case "IFF" => FunctionDefinition.standard(3)
    case "INDEX_COL" => FunctionDefinition.standard(3)
    case "INDEXKEY_PROPERTY" => FunctionDefinition.standard(3)
    case "INDEXPROPERTY" => FunctionDefinition.standard(3)
    case "IS_MEMBER" => FunctionDefinition.standard(1)
    case "IS_ROLEMEMBER" => FunctionDefinition.standard(1, 2)
    case "IS_SRVROLEMEMBER" => FunctionDefinition.standard(1, 2)
    case "ISDATE" => FunctionDefinition.standard(1)
    case "ISDESCENDANTOF" => FunctionDefinition.standard(1)
    case "ISJSON" => FunctionDefinition.standard(1, 2)
    case "ISNUMERIC" => FunctionDefinition.standard(1)
    case "JSON_MODIFY" => FunctionDefinition.standard(3)
    case "JSON_PATH_EXISTS" => FunctionDefinition.standard(2)
    case "JSON_QUERY" => FunctionDefinition.standard(2)
    case "JSON_VALUE" => FunctionDefinition.standard(2)
    case "LAG" => FunctionDefinition.standard(1, 3)
    case "LAST_VALUE" => FunctionDefinition.standard(1)
    case "LEAD" => FunctionDefinition.standard(1, 3)
    case "LEAST" => FunctionDefinition.standard(1, Int.MaxValue)
    case "LEFT" => FunctionDefinition.standard(2)
    case "LEN" => FunctionDefinition.standard(1)
    case "LISTAGG" => FunctionDefinition.standard(1, 2)
    case "LN" => FunctionDefinition.standard(1)
    case "LOG" => FunctionDefinition.standard(1, 2)
    case "LOG10" => FunctionDefinition.standard(1)
    case "LOGINPROPERTY" => FunctionDefinition.standard(2)
    case "LOWER" => FunctionDefinition.standard(1)
    case "LTRIM" => FunctionDefinition.standard(1)
    case "MAX" => FunctionDefinition.standard(1)
    case "MIN" => FunctionDefinition.standard(1)
    case "MIN_ACTIVE_ROWVERSION" => FunctionDefinition.standard(0)
    case "MONTH" => FunctionDefinition.standard(1)
    case "NCHAR" => FunctionDefinition.standard(1)
    case "NEWID" => FunctionDefinition.standard(0)
    case "NEWSEQUENTIALID" => FunctionDefinition.standard(0)
    case "NODES" => FunctionDefinition.xml(1)
    case "NTILE" => FunctionDefinition.standard(1)
    case "NULLIF" => FunctionDefinition.standard(2)
    case "OBJECT_DEFINITION" => FunctionDefinition.standard(1)
    case "OBJECT_ID" => FunctionDefinition.standard(1, 2)
    case "OBJECT_NAME" => FunctionDefinition.standard(1, 2)
    case "OBJECT_SCHEMA_NAME" => FunctionDefinition.standard(1, 2)
    case "OBJECTPROPERTY" => FunctionDefinition.standard(2)
    case "OBJECTPROPERTYEX" => FunctionDefinition.standard(2)
    case "ORIGINAL_DB_NAME" => FunctionDefinition.standard(0)
    case "ORIGINAL_LOGIN" => FunctionDefinition.standard(0)
    case "PARSE" => FunctionDefinition.notConvertible(2, 3) // Not in DBSQL
    case "PARSENAME" => FunctionDefinition.standard(2)
    case "PATINDEX" => FunctionDefinition.standard(2)
    case "PERCENT_RANK" => FunctionDefinition.standard(0)
    case "PERCENTILE_CONT" => FunctionDefinition.standard(1)
    case "PERCENTILE_DISC" => FunctionDefinition.standard(1)
    case "PERMISSIONS" => FunctionDefinition.notConvertible(0, 2) // not in DBSQL
    case "PI" => FunctionDefinition.standard(0)
    case "POWER" => FunctionDefinition.standard(2)
    case "PWDCOMPARE" => FunctionDefinition.standard(2, 3)
    case "PWDENCRYPT" => FunctionDefinition.standard(1)
    case "QUERY" => FunctionDefinition.xml(1)
    case "QUOTENAME" => FunctionDefinition.standard(1, 2)
    case "RADIANS" => FunctionDefinition.standard(1)
    case "RAND" => FunctionDefinition.standard(0, 1)
    case "RANK" => FunctionDefinition.standard(0)
    case "REPLACE" => FunctionDefinition.standard(3)
    case "REPLICATE" => FunctionDefinition.standard(2)
    case "REVERSE" => FunctionDefinition.standard(1)
    case "RIGHT" => FunctionDefinition.standard(2)
    case "ROUND" => FunctionDefinition.standard(1, 3)
    case "ROW_NUMBER" => FunctionDefinition.standard(0)
    case "ROWCOUNT_BIG" => FunctionDefinition.standard(0)
    case "RTRIM" => FunctionDefinition.standard(1)
    case "SCHEMA_ID" => FunctionDefinition.standard(0, 1)
    case "SCHEMA_NAME" => FunctionDefinition.standard(0, 1)
    case "SCOPE_IDENTITY" => FunctionDefinition.standard(0)
    case "SERVERPROPERTY" => FunctionDefinition.standard(1)
    case "SESSION_CONTEXT" => FunctionDefinition.standard(1, 2)
    case "SESSION_USER" => FunctionDefinition.standard(0)
    case "SESSIONPROPERTY" => FunctionDefinition.standard(1)
    case "SIGN" => FunctionDefinition.standard(1)
    case "SIN" => FunctionDefinition.standard(1)
    case "SMALLDATETIMEFROMPARTS" => FunctionDefinition.standard(5)
    case "SOUNDEX" => FunctionDefinition.standard(1)
    case "SPACE" => FunctionDefinition.standard(1)
    case "SQL_VARIANT_PROPERTY" => FunctionDefinition.standard(2)
    case "SQRT" => FunctionDefinition.standard(1)
    case "SQUARE" => FunctionDefinition.standard(1)
    case "STATS_DATE" => FunctionDefinition.standard(2)
    case "STDEV" => FunctionDefinition.standard(1)
    case "STDEVP" => FunctionDefinition.standard(1)
    case "STR" => FunctionDefinition.standard(1, 3)
    case "STRING_AGG" => FunctionDefinition.standard(2, 3)
    case "STRING_ESCAPE" => FunctionDefinition.standard(2)
    case "STUFF" => FunctionDefinition.standard(4)
    case "SUBSTR" => FunctionDefinition.standard(2, 3)
    case "SUBSTRING" => FunctionDefinition.standard(2, 3).withConversionStrategy(SynonymOf("SUBSTR"))
    case "SUM" => FunctionDefinition.standard(1)
    case "SUSER_ID" => FunctionDefinition.standard(0, 1)
    case "SUSER_NAME" => FunctionDefinition.standard(0, 1)
    case "SUSER_SID" => FunctionDefinition.standard(0, 2)
    case "SUSER_SNAME" => FunctionDefinition.standard(0, 1)
    case "SWITCHOFFSET" => FunctionDefinition.standard(2)
    case "SYSDATETIME" => FunctionDefinition.standard(0)
    case "SYSDATETIMEOFFSET" => FunctionDefinition.standard(0)
    case "SYSTEM_USER" => FunctionDefinition.standard(0)
    case "SYSUTCDATETIME" => FunctionDefinition.standard(0)
    case "TAN" => FunctionDefinition.standard(1)
    case "TIMEFROMPARTS" => FunctionDefinition.standard(5)
    case "TODATETIMEOFFSET" => FunctionDefinition.standard(2)
    case "TOSTRING" => FunctionDefinition.standard(0)
    case "TRANSLATE" => FunctionDefinition.standard(3)
    case "TRIM" => FunctionDefinition.standard(1, 2)
    case "TYPE_ID" => FunctionDefinition.standard(1)
    case "TYPE_NAME" => FunctionDefinition.standard(1)
    case "TYPEPROPERTY" => FunctionDefinition.standard(2)
    case "UNICODE" => FunctionDefinition.standard(1)
    case "UPPER" => FunctionDefinition.standard(1)
    case "USER" => FunctionDefinition.standard(0)
    case "USER_ID" => FunctionDefinition.standard(0, 1)
    case "USER_NAME" => FunctionDefinition.standard(0, 1)
    case "VALUE" => FunctionDefinition.xml(2)
    case "VAR" => FunctionDefinition.standard(1)
    case "VARP" => FunctionDefinition.standard(1)
    case "XACT_STATE" => FunctionDefinition.standard(0)
    case "YEAR" => FunctionDefinition.standard(1)
  }

  def functionDefinition(name: String): Option[FunctionDefinition] =
    commonFunctionsPf.lift(name.toUpperCase())

  def functionType(name: String): FunctionType = {
    functionDefinition(name).map(_.functionType).getOrElse(UnknownFunction)
  }

  def buildFunction(id: ir.Id, args: Seq[ir.Expression]): ir.Expression = {
    val name = if (id.caseSensitive) id.id else id.id.toUpperCase()
    buildFunction(name, args)
  }

  def buildFunction(name: String, args: Seq[ir.Expression]): ir.Expression = {
    val irName = removeQuotesAndBrackets(name)
    val defnOption = functionDefinition(irName)

    defnOption match {
      case Some(functionDef) if functionDef.functionType == NotConvertibleFunction =>
        ir.UnresolvedFunction(
          name,
          args,
          is_distinct = false,
          is_user_defined_function = false,
          ruleText = s"$irName(...)",
          message = s"Function $irName is not convertible to Databricks SQL",
          ruleName = "N/A",
          tokenName = Some("N/A"))

      case Some(funDef) if FunctionArity.verifyArguments(funDef.arity, args) =>
        applyConversionStrategy(funDef, args, irName)

      // Found the function but the arg count is incorrect
      case Some(_) =>
        ir.UnresolvedFunction(
          irName,
          args,
          is_distinct = false,
          is_user_defined_function = false,
          has_incorrect_argc = true,
          ruleText = s"$irName(...)",
          message = s"Invocation of $irName has incorrect argument count",
          ruleName = "N/A",
          tokenName = Some("N/A"))

      // Unsupported function
      case None =>
        ir.UnresolvedFunction(
          irName,
          args,
          is_distinct = false,
          is_user_defined_function = false,
          ruleText = s"$irName(...)",
          message = s"Function $irName is not convertible to Databricks SQL",
          ruleName = "N/A",
          tokenName = Some("N/A"))
    }
  }

  def applyConversionStrategy(
      functionArity: FunctionDefinition,
      args: Seq[ir.Expression],
      irName: String): ir.Expression

  /**
   * Functions can be called even if they are quoted or bracketed. This function removes the quotes and brackets.
   * @param str
   *   the possibly quoted function name
   * @return
   *   function name for use in lookup/matching
   */
  private def removeQuotesAndBrackets(str: String): String = {
    val quotations = Map('\'' -> "'", '"' -> "\"", '[' -> "]", '\\' -> "\\")
    str match {
      case s if s.length < 2 => s
      case s =>
        quotations.get(s.head).fold(s) { closingQuote =>
          if (s.endsWith(closingQuote)) {
            s.substring(1, s.length - 1)
          } else {
            s
          }
        }
    }
  }
}
