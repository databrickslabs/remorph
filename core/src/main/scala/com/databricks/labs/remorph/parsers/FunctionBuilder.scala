package com.databricks.labs.remorph.parsers

import com.databricks.labs.remorph.parsers.{intermediate => ir}

sealed trait FunctionType
case object StandardFunction extends FunctionType
case object XmlFunction extends FunctionType
case object NotConvertibleFunction extends FunctionType
case object UnknownFunction extends FunctionType

sealed trait FunctionArity

case class FixedArity(arity: Int) extends FunctionArity

case class VariableArity(argMin: Int, argMax: Int) extends FunctionArity
object FunctionArity {
  def verifyArgNumber(arity: FunctionArity, args: Seq[ir.Expression]): Boolean = arity match {
    case FixedArity(n) => args.size == n
    case VariableArity(argMin, argMax) => argMin <= args.size && args.size <= argMax
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

  def xml(fixedArgNumber: Int): FunctionDefinition =
    FunctionDefinition(FixedArity(fixedArgNumber), XmlFunction)

  def notConvertible(fixedArgNumber: Int): FunctionDefinition =
    FunctionDefinition(FixedArity(fixedArgNumber), NotConvertibleFunction)
  def notConvertible(minArg: Int, maxArg: Int): FunctionDefinition =
    FunctionDefinition(VariableArity(minArg, maxArg), NotConvertibleFunction)
}
object FunctionBuilder {

  private val functionDefinitionPf: PartialFunction[(SqlDialect, String), FunctionDefinition] = {
    case (_, "@@CURSOR_STATUS") => FunctionDefinition.notConvertible(0)
    case (_, "@@FETCH_STATUS") => FunctionDefinition.notConvertible(0)
    case (_, "ABS") => FunctionDefinition.standard(1)
    case (_, "ACOS") => FunctionDefinition.standard(1)
    case (_, "APP_NAME") => FunctionDefinition.standard(0)
    case (_, "APPLOCK_MODE") => FunctionDefinition.standard(3)
    case (_, "APPLOCK_TEST") => FunctionDefinition.standard(4)
    case (_, "ASCII") => FunctionDefinition.standard(1)
    case (_, "ASIN") => FunctionDefinition.standard(1)
    case (_, "ASSEMBLYPROPERTY") => FunctionDefinition.standard(2)
    case (_, "ARRAYAGG") => FunctionDefinition.standard(1)
    case (_, "ATAN") => FunctionDefinition.standard(1)
    case (_, "ATN2") => FunctionDefinition.standard(2)
    case (_, "AVG") => FunctionDefinition.standard(1)
    case (_, "CEILING") => FunctionDefinition.standard(1)
    case (_, "CERT_ID") => FunctionDefinition.standard(1)
    case (_, "CERTENCODED") => FunctionDefinition.standard(1)
    case (_, "CERTPRIVATEKEY") => FunctionDefinition.standard(2, 3)
    case (_, "CHAR") => FunctionDefinition.standard(1)
    case (_, "CHARINDEX") => FunctionDefinition.standard(2, 3)
    case (_, "CHECKSUM_AGG") => FunctionDefinition.standard(1)
    case (_, "COALESCE") => FunctionDefinition.standard(1, Int.MaxValue)
    case (_, "CHECKSUM") => FunctionDefinition.standard(1, Int.MaxValue)
    case (_, "COALESCE") => FunctionDefinition.standard(1, Int.MaxValue)
    case (_, "BINARY_CHECKSUM") => FunctionDefinition.standard(1, Int.MaxValue)
    case (_, "COL_LENGTH") => FunctionDefinition.standard(2)
    case (_, "COL_NAME") => FunctionDefinition.standard(2)
    case (_, "COLUMNPROPERTY") => FunctionDefinition.standard(3)
    case (_, "COMPRESS") => FunctionDefinition.standard(1)
    case (_, "CONCAT") => FunctionDefinition.standard(2, Int.MaxValue)
    case (_, "CONCAT_WS") => FunctionDefinition.standard(3, Int.MaxValue)
    case (_, "CONNECTIONPROPERTY") => FunctionDefinition.notConvertible(1)
    case (_, "CONTEXT_INFO") => FunctionDefinition.standard(0)
    case (_, "CONVERT") => FunctionDefinition.standard(2, 3)
    case (_, "COS") => FunctionDefinition.standard(1)
    case (_, "COT") => FunctionDefinition.standard(1)
    case (_, "COUNT") => FunctionDefinition.standard(1)
    case (_, "COUNT_BIG") => FunctionDefinition.standard(1)
    case (_, "CURRENT_DATE") => FunctionDefinition.standard(0)
    case (_, "CURRENT_REQUEST_ID") => FunctionDefinition.standard(0)
    case (_, "CURRENT_TIMESTAMP") => FunctionDefinition.standard(0)
    case (_, "CURRENT_TIMEZONE") => FunctionDefinition.standard(0)
    case (_, "CURRENT_TIMEZONE_ID") => FunctionDefinition.standard(0)
    case (_, "CURRENT_TRANSACTION_ID") => FunctionDefinition.standard(0)
    case (_, "CURRENT_USER") => FunctionDefinition.standard(0)
    case (_, "CURSOR_ROWS") => FunctionDefinition.standard(0)
    case (_, "CUME_DIST") => FunctionDefinition.standard(0)
    case (_, "CURSOR_STATUS") => FunctionDefinition.standard(2)
    case (_, "DATABASE_PRINCIPAL_ID") => FunctionDefinition.standard(0, 1)
    case (_, "DATABASEPROPERTY") => FunctionDefinition.standard(2)
    case (_, "DATABASEPROPERTYEX") => FunctionDefinition.standard(2)
    case (_, "DATALENGTH") => FunctionDefinition.standard(1)
    case (_, "DATE_BUCKET") => FunctionDefinition.standard(3, 4)
    case (_, "DATE_DIFF_BIG") => FunctionDefinition.standard(3)
    case (_, "DATEADD") => FunctionDefinition.standard(3)
    case (_, "DATEDIFF") => FunctionDefinition.standard(3)
    case (_, "DATEFROMPARTS") => FunctionDefinition.standard(3)
    case (_, "DATENAME") => FunctionDefinition.standard(2)
    case (_, "DATEPART") => FunctionDefinition.standard(2)
    case (_, "DATETIME2FROMPARTS") => FunctionDefinition.standard(8)
    case (_, "DATETIMEFROMPARTS") => FunctionDefinition.standard(7)
    case (_, "DATETIMEOFFSETFROMPARTS") => FunctionDefinition.standard(10)
    case (_, "DATETRUNC") => FunctionDefinition.standard(2)
    case (_, "DAY") => FunctionDefinition.standard(1)
    case (_, "DB_ID") => FunctionDefinition.standard(0, 1)
    case (_, "DB_NAME") => FunctionDefinition.standard(0, 1)
    case (_, "DECOMPRESS") => FunctionDefinition.standard(1)
    case (_, "DEGREES") => FunctionDefinition.standard(1)
    case (_, "DENSE_RANK") => FunctionDefinition.standard(0)
    case (_, "DIFFERENCE") => FunctionDefinition.standard(2)
    case (_, "EOMONTH") => FunctionDefinition.standard(1, 2)
    case (_, "ERROR_LINE") => FunctionDefinition.standard(0)
    case (_, "ERROR_MESSAGE") => FunctionDefinition.standard(0)
    case (_, "ERROR_NUMBER") => FunctionDefinition.standard(0)
    case (_, "ERROR_PROCEDURE") => FunctionDefinition.standard(0)
    case (_, "ERROR_SEVERITY") => FunctionDefinition.standard(0)
    case (_, "ERROR_STATE") => FunctionDefinition.standard(0)
    case (_, "EXIST") => FunctionDefinition.xml(1)
    case (_, "EXP") => FunctionDefinition.standard(1)
    case (_, "FILE_ID") => FunctionDefinition.standard(1)
    case (_, "FILE_IDEX") => FunctionDefinition.standard(1)
    case (_, "FILE_NAME") => FunctionDefinition.standard(1)
    case (_, "FILEGROUP_ID") => FunctionDefinition.standard(1)
    case (_, "FILEGROUP_NAME") => FunctionDefinition.standard(1)
    case (_, "FILEGROUPPROPERTY") => FunctionDefinition.standard(2)
    case (_, "FILEPROPERTY") => FunctionDefinition.standard(2)
    case (_, "FILEPROPERTYEX") => FunctionDefinition.standard(2)
    case (_, "FLOOR") => FunctionDefinition.standard(1)
    case (_, "FIRST_VALUE") => FunctionDefinition.standard(1)
    case (_, "FORMAT") => FunctionDefinition.standard(2, 3)
    case (_, "FORMATMESSAGE") => FunctionDefinition.standard(2, Int.MaxValue)
    case (_, "FULLTEXTCATALOGPROPERTY") => FunctionDefinition.standard(2)
    case (_, "FULLTEXTSERVICEPROPERTY") => FunctionDefinition.standard(1)
    case (_, "GET_FILESTREAM_TRANSACTION_CONTEXT") => FunctionDefinition.standard(0)
    case (_, "GETANCESTGOR") => FunctionDefinition.standard(1)
    case (_, "GETANSINULL") => FunctionDefinition.standard(0, 1)
    case (_, "GETDATE") => FunctionDefinition.standard(0)
    case (_, "GETDESCENDANT") => FunctionDefinition.standard(2)
    case (_, "GETLEVEL") => FunctionDefinition.standard(0)
    case (_, "GETREPARENTEDVALUE") => FunctionDefinition.standard(2)
    case (_, "GETUTCDATE") => FunctionDefinition.standard(0)
    case (_, "GREATEST") => FunctionDefinition.standard(1, Int.MaxValue)
    case (_, "GROUPING") => FunctionDefinition.standard(1)
    case (_, "GROUPING_ID") => FunctionDefinition.standard(0, Int.MaxValue)
    case (_, "HAS_DBACCESS") => FunctionDefinition.standard(1)
    case (_, "HAS_PERMS_BY_NAME") => FunctionDefinition.standard(4, 5)
    case (_, "HOST_ID") => FunctionDefinition.standard(0)
    case (_, "HOST_NAME") => FunctionDefinition.standard(0)
    case (_, "IDENT_CURRENT") => FunctionDefinition.standard(1)
    case (_, "IDENT_INCR") => FunctionDefinition.standard(1)
    case (_, "IDENT_SEED") => FunctionDefinition.standard(1)
    case (_, "IDENTITY") => FunctionDefinition.standard(1, 3)
    case (Snowflake, "IFNULL") => FunctionDefinition.standard(2)
    case (_, "IFF") => FunctionDefinition.standard(3)
    case (_, "INDEX_COL") => FunctionDefinition.standard(3)
    case (_, "INDEXKEY_PROPERTY") => FunctionDefinition.standard(3)
    case (_, "INDEXPROPERTY") => FunctionDefinition.standard(3)
    case (_, "IS_MEMBER") => FunctionDefinition.standard(1)
    case (_, "IS_ROLEMEMBER") => FunctionDefinition.standard(1, 2)
    case (_, "IS_SRVROLEMEMBER") => FunctionDefinition.standard(1, 2)
    case (_, "ISDATE") => FunctionDefinition.standard(1)
    case (_, "ISDESCENDANTOF") => FunctionDefinition.standard(1)
    case (_, "ISJSON") => FunctionDefinition.standard(1, 2)
    // The ConversionStrategy is used to rename ISNULL to IFNULL in TSql
    case (TSql, "ISNULL") =>
      FunctionDefinition.standard(1, 2).withConversionStrategy(FunctionConverters.FunctionRename)
    case (_, "ISNUMERIC") => FunctionDefinition.standard(1)
    case (_, "JSON_MODIFY") => FunctionDefinition.standard(3)
    case (_, "JSON_PATH_EXISTS") => FunctionDefinition.standard(2)
    case (_, "JSON_QUERY") => FunctionDefinition.standard(2)
    case (_, "JSON_VALUE") => FunctionDefinition.standard(2)
    case (_, "LAG") => FunctionDefinition.standard(1, 3)
    case (_, "LAST_VALUE") => FunctionDefinition.standard(1)
    case (_, "LEAD") => FunctionDefinition.standard(1)
    case (_, "LEAST") => FunctionDefinition.standard(1, Int.MaxValue)
    case (_, "LEFT") => FunctionDefinition.standard(2)
    case (_, "LEN") => FunctionDefinition.standard(1)
    case (_, "LISTAGG") => FunctionDefinition.standard(1, 2)
    case (_, "LOG") => FunctionDefinition.standard(1, 2)
    case (_, "LOG10") => FunctionDefinition.standard(1)
    case (_, "LOGINPROPERTY") => FunctionDefinition.standard(2)
    case (_, "LOWER") => FunctionDefinition.standard(1)
    case (_, "LTRIM") => FunctionDefinition.standard(1)
    case (_, "MAX") => FunctionDefinition.standard(1)
    case (_, "MIN") => FunctionDefinition.standard(1)
    case (_, "MIN_ACTIVE_ROWVERSION") => FunctionDefinition.standard(0)
    case (_, "MODIFY") => FunctionDefinition.xml(1)
    case (_, "MONTH") => FunctionDefinition.standard(1)
    case (_, "NCHAR") => FunctionDefinition.standard(1)
    case (_, "NEWID") => FunctionDefinition.standard(0)
    case (_, "NEWSEQUENTIALID") => FunctionDefinition.standard(0)
    case (_, "NODES") => FunctionDefinition.xml(1)
    case (_, "NTILE") => FunctionDefinition.standard(1)
    case (_, "NULLIF") => FunctionDefinition.standard(2)
    case (_, "OBJECT_DEFINITION") => FunctionDefinition.standard(1)
    case (_, "OBJECT_ID") => FunctionDefinition.standard(1, 2)
    case (_, "OBJECT_NAME") => FunctionDefinition.standard(1, 2)
    case (_, "OBJECT_SCHEMA_NAME") => FunctionDefinition.standard(1, 2)
    case (_, "OBJECTPROPERTY") => FunctionDefinition.standard(2)
    case (_, "OBJECTPROPERTYEX") => FunctionDefinition.standard(2)
    case (_, "ORIGINAL_DB_NAME") => FunctionDefinition.standard(0)
    case (_, "ORIGINAL_LOGIN") => FunctionDefinition.standard(0)
    case (_, "PARSE") => FunctionDefinition.notConvertible(2, 3) // Not in DBSQL
    case (_, "PARSENAME") => FunctionDefinition.standard(2)
    case (_, "PATINDEX") => FunctionDefinition.standard(2)
    case (_, "PERMISSIONS") => FunctionDefinition.notConvertible(0, 2) // not in DBSQL
    case (_, "PERCENTILE_CONT") => FunctionDefinition.standard(1)
    case (_, "PERCENT_RANK") => FunctionDefinition.standard(0)
    case (_, "PERCENT_DISC") => FunctionDefinition.standard(0)
    case (_, "PI") => FunctionDefinition.standard(0)
    case (_, "POWER") => FunctionDefinition.standard(2)
    case (_, "PWDCOMPARE") => FunctionDefinition.standard(2, 3)
    case (_, "PWDENCRYPT") => FunctionDefinition.standard(1)
    case (_, "QUERY") => FunctionDefinition.xml(1)
    case (_, "QUOTENAME") => FunctionDefinition.standard(1, 2)
    case (_, "RADIANS") => FunctionDefinition.standard(1)
    case (_, "RAND") => FunctionDefinition.standard(0, 1)
    case (_, "RANK") => FunctionDefinition.standard(0)
    case (_, "REPLACE") => FunctionDefinition.standard(3)
    case (_, "REPLICATE") => FunctionDefinition.standard(2)
    case (_, "REVERSE") => FunctionDefinition.standard(1)
    case (_, "RIGHT") => FunctionDefinition.standard(2)
    case (_, "ROUND") => FunctionDefinition.standard(2, 3)
    case (_, "ROW_NUMBER") => FunctionDefinition.standard(0)
    case (_, "ROWCOUNT_BIG") => FunctionDefinition.standard(0)
    case (_, "RTRIM") => FunctionDefinition.standard(1)
    case (_, "SCHEMA_ID") => FunctionDefinition.standard(0, 1)
    case (_, "SCHEMA_NAME") => FunctionDefinition.standard(0, 1)
    case (_, "SCOPE_IDENTITY") => FunctionDefinition.standard(0)
    case (_, "SESSION_USER") => FunctionDefinition.standard(0)
    case (_, "SERVERPROPERTY") => FunctionDefinition.standard(1)
    case (_, "SESSION_CONTEXT") => FunctionDefinition.standard(1, 2)
    case (_, "SESSIONPROPERTY") => FunctionDefinition.standard(1)
    case (_, "SIGN") => FunctionDefinition.standard(1)
    case (_, "SIN") => FunctionDefinition.standard(1)
    case (_, "SMALLDATETIMEFROMPARTS") => FunctionDefinition.standard(5)
    case (_, "SOUNDEX") => FunctionDefinition.standard(1)
    case (_, "SPACE") => FunctionDefinition.standard(1)
    case (_, "SQL_VARIANT_PROPERTY") => FunctionDefinition.standard(2)
    case (_, "SQRT") => FunctionDefinition.standard(1)
    case (_, "SQUARE") => FunctionDefinition.standard(1)
    case (_, "STATS_DATE") => FunctionDefinition.standard(2)
    case (_, "STDEV") => FunctionDefinition.standard(1)
    case (_, "STDEVP") => FunctionDefinition.standard(1)
    case (_, "STR") => FunctionDefinition.standard(1, 3)
    case (_, "STRING_AGG") => FunctionDefinition.standard(2, 3)
    case (_, "STRING_ESCAPE") => FunctionDefinition.standard(2)
    case (_, "STUFF") => FunctionDefinition.standard(4)
    case (_, "SUBSTRING") => FunctionDefinition.standard(2, 3)
    case (_, "SUM") => FunctionDefinition.standard(1)
    case (_, "SUSER_ID") => FunctionDefinition.standard(0, 1)
    case (_, "SUSER_NAME") => FunctionDefinition.standard(0, 1)
    case (_, "SUSER_SID") => FunctionDefinition.standard(0, 2)
    case (_, "SUSER_SNAME") => FunctionDefinition.standard(0, 1)
    case (_, "SWITCHOFFSET") => FunctionDefinition.standard(2)
    case (_, "SYSDATETIME") => FunctionDefinition.standard(0)
    case (_, "SYSTEM_USER") => FunctionDefinition.standard(0)
    case (_, "SYSDATETIMEOFFSET") => FunctionDefinition.standard(0)
    case (_, "SYSUTCDATETIME") => FunctionDefinition.standard(0)
    case (_, "TAN") => FunctionDefinition.standard(1)
    case (_, "TIMEFROMPARTS") => FunctionDefinition.standard(5)
    case (_, "TODATETIMEOFFSET") => FunctionDefinition.standard(2)
    case (_, "TOSTRING") => FunctionDefinition.standard(0)
    case (_, "USER") => FunctionDefinition.standard(0)
    case (_, "TRANSLATE") => FunctionDefinition.standard(3)
    case (_, "TRIM") => FunctionDefinition.standard(1, 2)
    case (_, "TYPE_ID") => FunctionDefinition.standard(1)
    case (_, "TYPE_NAME") => FunctionDefinition.standard(1)
    case (_, "TYPEPROPERTY") => FunctionDefinition.standard(2)
    case (_, "UNICODE") => FunctionDefinition.standard(1)
    case (_, "UPPER") => FunctionDefinition.standard(1)
    case (_, "USER_ID") => FunctionDefinition.standard(0, 1)
    case (_, "USER_NAME") => FunctionDefinition.standard(0, 1)
    case (_, "VALUE") => FunctionDefinition.xml(2)
    case (_, "VAR") => FunctionDefinition.standard(1)
    case (_, "VARP") => FunctionDefinition.standard(1)
    case (_, "XACT_STATE") => FunctionDefinition.standard(0)
    case (_, "YEAR") => FunctionDefinition.standard(1)
  }

  def functionDefinition(dialect: SqlDialect, name: String): Option[FunctionDefinition] =
    functionDefinitionPf.lift((dialect, name.toUpperCase()))

  def functionType(dialect: SqlDialect, name: String): FunctionType = {
    functionDefinition(dialect, name).map(_.functionType).getOrElse(UnknownFunction)
  }

  def buildFunction(name: String, args: Seq[ir.Expression], dialect: SqlDialect): ir.Expression = {
    val irName = removeQuotesAndBrackets(name)
    val defnOption = functionDefinition(dialect, irName)

    defnOption match {
      case Some(functionDef) if functionDef.functionType == NotConvertibleFunction =>
        ir.UnresolvedFunction(name, args, is_distinct = false, is_user_defined_function = false)

      case Some(funDef) if FunctionArity.verifyArgNumber(funDef.arity, args) =>
        applyConversionStrategy(funDef, args, irName, dialect)

      // Found the function but the arg count is incorrect
      case Some(_) =>
        ir.UnresolvedFunction(
          irName,
          args,
          is_distinct = false,
          is_user_defined_function = false,
          has_incorrect_argc = true)

      // Unsupported function
      case None =>
        ir.UnresolvedFunction(irName, args, is_distinct = false, is_user_defined_function = false)
    }
  }

  private def applyConversionStrategy(
      functionArity: FunctionDefinition,
      args: Seq[ir.Expression],
      irName: String,
      dialect: SqlDialect): ir.Expression = {
    functionArity.conversionStrategy match {
      case Some(strategy) => strategy.convert(irName, args, dialect)
      case _ => ir.CallFunction(irName, args)
    }
  }

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
