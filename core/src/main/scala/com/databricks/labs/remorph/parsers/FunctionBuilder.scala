package com.databricks.labs.remorph.parsers

import com.databricks.labs.remorph.parsers.{intermediate => ir}

sealed trait FunctionType
case object StandardFunction extends FunctionType
case object XmlFunction extends FunctionType
case object UnknownFunction extends FunctionType

sealed trait FunctionArity {
  def isConvertible: Boolean
  def conversionStrategy: Option[ConversionStrategy]
}

case class FixedArity(
    arity: Int,
    functionType: FunctionType = StandardFunction,
    convertible: Boolean = true,
    override val conversionStrategy: Option[ConversionStrategy] = None)
    extends FunctionArity {
  override def isConvertible: Boolean = convertible
}

case class VariableArity(
    argMin: Int,
    argMax: Int,
    functionType: FunctionType = StandardFunction,
    convertible: Boolean = true,
    override val conversionStrategy: Option[ConversionStrategy] = None)
    extends FunctionArity {
  override def isConvertible: Boolean = convertible
}

object FunctionBuilder {

  private val functionArityPf: PartialFunction[(SqlDialect, String), FunctionArity] = {
    case (_, "ABS") => FixedArity(1)
    case (_, "ACOS") => FixedArity(1)
    case (_, "APP_NAME") => FixedArity(0)
    case (_, "APPLOCK_MODE") => FixedArity(3)
    case (_, "APPLOCK_TEST") => FixedArity(4)
    case (_, "ASCII") => FixedArity(1)
    case (_, "ASIN") => FixedArity(1)
    case (_, "ASSEMBLYPROPERTY") => FixedArity(2)
    case (_, "ATAN") => FixedArity(1)
    case (_, "ATN2") => FixedArity(2)
    case (_, "AVG") => FixedArity(1)
    case (_, "CEILING") => FixedArity(1)
    case (_, "CERT_ID") => FixedArity(1)
    case (_, "CERTENCODED") => FixedArity(1)
    case (_, "CERTPRIVATEKEY") => VariableArity(2, 3)
    case (_, "CHAR") => FixedArity(1)
    case (_, "CHARINDEX") => VariableArity(2, 3)
    case (_, "CHECKSUM_AGG") => FixedArity(1)
    case (_, "COALESCE") => VariableArity(1, Int.MaxValue)
    case (_, "COL_LENGTH") => FixedArity(2)
    case (_, "COL_NAME") => FixedArity(2)
    case (_, "COLUMNPROPERTY") => FixedArity(3)
    case (_, "COMPRESS") => FixedArity(1)
    case (_, "CONCAT") => VariableArity(2, Int.MaxValue)
    case (_, "CONCAT_WS") => VariableArity(3, Int.MaxValue)
    case (_, "CONNECTIONPROPERTY") => FixedArity(1, convertible = false)
    case (_, "CONTEXT_INFO") => FixedArity(0)
    case (_, "CONVERT") => VariableArity(2, 3)
    case (_, "COS") => FixedArity(1)
    case (_, "COT") => FixedArity(1)
    case (_, "COUNT") => FixedArity(1)
    case (_, "COUNT_BIG") => FixedArity(1)
    case (_, "CURRENT_DATE") => FixedArity(0)
    case (_, "CURRENT_REQUEST_ID") => FixedArity(0)
    case (_, "CURRENT_TIMESTAMP") => FixedArity(0)
    case (_, "CURRENT_TIMEZONE") => FixedArity(0)
    case (_, "CURRENT_TIMEZONE_ID") => FixedArity(0)
    case (_, "CURRENT_TRANSACTION_ID") => FixedArity(0)
    case (_, "CURRENT_USER") => FixedArity(0)
    case (_, "CURSOR_STATUS") => FixedArity(2)
    case (_, "DATABASE_PRINCIPAL_ID") => VariableArity(0, 1)
    case (_, "DATABASEPROPERTY") => FixedArity(2)
    case (_, "DATABASEPROPERTYEX") => FixedArity(2)
    case (_, "DATALENGTH") => FixedArity(1)
    case (_, "DATE_BUCKET") => VariableArity(3, 4)
    case (_, "DATE_DIFF_BIG") => FixedArity(3)
    case (_, "DATEADD") => FixedArity(3)
    case (_, "DATEDIFF") => FixedArity(3)
    case (_, "DATEFROMPARTS") => FixedArity(3)
    case (_, "DATENAME") => FixedArity(2)
    case (_, "DATEPART") => FixedArity(2)
    case (_, "DATETIME2FROMPARTS") => FixedArity(8)
    case (_, "DATETIMEFROMPARTS") => FixedArity(7)
    case (_, "DATETIMEOFFSETFROMPARTS") => FixedArity(10)
    case (_, "DATETRUNC") => FixedArity(2)
    case (_, "DAY") => FixedArity(1)
    case (_, "DB_ID") => VariableArity(0, 1)
    case (_, "DB_NAME") => VariableArity(0, 1)
    case (_, "DECOMPRESS") => FixedArity(1)
    case (_, "DEGREES") => FixedArity(1)
    case (_, "DENSE_RANK") => FixedArity(0)
    case (_, "DIFFERENCE") => FixedArity(2)
    case (_, "EOMONTH") => VariableArity(1, 2)
    case (_, "ERROR_LINE") => FixedArity(0)
    case (_, "ERROR_MESSAGE") => FixedArity(0)
    case (_, "ERROR_NUMBER") => FixedArity(0)
    case (_, "ERROR_PROCEDURE") => FixedArity(0)
    case (_, "ERROR_SEVERITY") => FixedArity(0)
    case (_, "ERROR_STATE") => FixedArity(0)
    case (_, "EXIST") => FixedArity(1, XmlFunction)
    case (_, "EXP") => FixedArity(1)
    case (_, "FILE_ID") => FixedArity(1)
    case (_, "FILE_IDEX") => FixedArity(1)
    case (_, "FILE_NAME") => FixedArity(1)
    case (_, "FILEGROUP_ID") => FixedArity(1)
    case (_, "FILEGROUP_NAME") => FixedArity(1)
    case (_, "FILEGROUPPROPERTY") => FixedArity(2)
    case (_, "FILEPROPERTY") => FixedArity(2)
    case (_, "FILEPROPERTYEX") => FixedArity(2)
    case (_, "FLOOR") => FixedArity(1)
    case (_, "FORMAT") => VariableArity(2, 3)
    case (_, "FORMATMESSAGE") => VariableArity(2, Int.MaxValue)
    case (_, "FULLTEXTCATALOGPROPERTY") => FixedArity(2)
    case (_, "FULLTEXTSERVICEPROPERTY") => FixedArity(1)
    case (_, "GET_FILESTREAM_TRANSACTION_CONTEXT") => FixedArity(0)
    case (_, "GETANCESTGOR") => FixedArity(1)
    case (_, "GETANSINULL") => VariableArity(0, 1)
    case (_, "GETDATE") => FixedArity(0)
    case (_, "GETDESCENDANT") => FixedArity(2)
    case (_, "GETLEVEL") => FixedArity(0)
    case (_, "GETREPARENTEDVALUE") => FixedArity(2)
    case (_, "GETUTCDATE") => FixedArity(0)
    case (_, "GREATEST") => VariableArity(1, Int.MaxValue)
    case (_, "GROUPING") => FixedArity(1)
    case (_, "GROUPING_ID") => VariableArity(0, Int.MaxValue)
    case (_, "HAS_DBACCESS") => FixedArity(1)
    case (_, "HAS_PERMS_BY_NAME") => VariableArity(4, 5)
    case (_, "HOST_ID") => FixedArity(0)
    case (_, "HOST_NAME") => FixedArity(0)
    case (_, "IDENT_CURRENT") => FixedArity(1)
    case (_, "IDENT_INCR") => FixedArity(1)
    case (_, "IDENT_SEED") => FixedArity(1)
    case (Snowflake, "IFNULL") => FixedArity(2)
    case (_, "IFF") => FixedArity(3)
    case (_, "INDEX_COL") => FixedArity(3)
    case (_, "INDEXKEY_PROPERTY") => FixedArity(3)
    case (_, "INDEXPROPERTY") => FixedArity(3)
    case (_, "IS_MEMBER") => FixedArity(1)
    case (_, "IS_ROLEMEMBER") => VariableArity(1, 2)
    case (_, "IS_SRVROLEMEMBER") => VariableArity(1, 2)
    case (_, "ISDATE") => FixedArity(1)
    case (_, "ISDESCENDANTOF") => FixedArity(1)
    case (_, "ISJSON") => VariableArity(1, 2)
    // The ConversionStrategy is used to rename ISNULL to IFNULL in TSql
    case (TSql, "ISNULL") => VariableArity(1, 2, conversionStrategy = Some(FunctionConverters.FunctionRename))
    case (_, "ISNUMERIC") => FixedArity(1)
    case (_, "JSON_MODIFY") => FixedArity(3)
    case (_, "JSON_PATH_EXISTS") => FixedArity(2)
    case (_, "JSON_QUERY") => FixedArity(2)
    case (_, "JSON_VALUE") => FixedArity(2)
    case (_, "LEAST") => VariableArity(1, Int.MaxValue)
    case (_, "LEFT") => FixedArity(2)
    case (_, "LEN") => FixedArity(1)
    case (_, "LOG") => VariableArity(1, 2)
    case (_, "LOG10") => FixedArity(1)
    case (_, "LOGINPROPERTY") => FixedArity(2)
    case (_, "LOWER") => FixedArity(1)
    case (_, "LTRIM") => FixedArity(1)
    case (_, "MAX") => FixedArity(1)
    case (_, "MIN") => FixedArity(1)
    case (_, "MIN_ACTIVE_ROWVERSION") => FixedArity(0)
    case (_, "MODIFY") => FixedArity(1, XmlFunction)
    case (_, "MONTH") => FixedArity(1)
    case (_, "NCHAR") => FixedArity(1)
    case (_, "NEWID") => FixedArity(0)
    case (_, "NEWSEQUENTIALID") => FixedArity(0)
    case (_, "NODES") => FixedArity(1, XmlFunction)
    case (_, "NTILE") => FixedArity(1)
    case (_, "NULLIF") => FixedArity(2)
    case (_, "OBJECT_DEFINITION") => FixedArity(1)
    case (_, "OBJECT_ID") => VariableArity(1, 2)
    case (_, "OBJECT_NAME") => VariableArity(1, 2)
    case (_, "OBJECT_SCHEMA_NAME") => VariableArity(1, 2)
    case (_, "OBJECTPROPERTY") => FixedArity(2)
    case (_, "OBJECTPROPERTYEX") => FixedArity(2)
    case (_, "ORIGINAL_DB_NAME") => FixedArity(0)
    case (_, "ORIGINAL_LOGIN") => FixedArity(0)
    case (_, "PARSE") => VariableArity(2, 3, convertible = false) // Not in DBSQL
    case (_, "PARSENAME") => FixedArity(2)
    case (_, "PATINDEX") => FixedArity(2)
    case (_, "PERMISSIONS") => VariableArity(0, 2, convertible = false) // not in DBSQL
    case (_, "PI") => FixedArity(0)
    case (_, "POWER") => FixedArity(2)
    case (_, "PWDCOMPARE") => VariableArity(2, 3)
    case (_, "PWDENCRYPT") => FixedArity(1)
    case (_, "QUERY") => FixedArity(1, XmlFunction)
    case (_, "QUOTENAME") => VariableArity(1, 2)
    case (_, "RADIANS") => FixedArity(1)
    case (_, "RAND") => VariableArity(0, 1)
    case (_, "RANK") => FixedArity(0)
    case (_, "REPLACE") => FixedArity(3)
    case (_, "REPLICATE") => FixedArity(2)
    case (_, "REVERSE") => FixedArity(1)
    case (_, "RIGHT") => FixedArity(2)
    case (_, "ROUND") => VariableArity(2, 3)
    case (_, "ROW_NUMBER") => FixedArity(0)
    case (_, "ROWCOUNT_BIG") => FixedArity(0)
    case (_, "RTRIM") => FixedArity(1)
    case (_, "SCHEMA_ID") => VariableArity(0, 1)
    case (_, "SCHEMA_NAME") => VariableArity(0, 1)
    case (_, "SCOPE_IDENTITY") => FixedArity(0)
    case (_, "SERVERPROPERTY") => FixedArity(1)
    case (_, "SESSION_CONTEXT") => VariableArity(1, 2)
    case (_, "SESSIONPROPERTY") => FixedArity(1)
    case (_, "SIGN") => FixedArity(1)
    case (_, "SIN") => FixedArity(1)
    case (_, "SMALLDATETIMEFROMPARTS") => FixedArity(5)
    case (_, "SOUNDEX") => FixedArity(1)
    case (_, "SPACE") => FixedArity(1)
    case (_, "SQL_VARIANT_PROPERTY") => FixedArity(2)
    case (_, "SQRT") => FixedArity(1)
    case (_, "SQUARE") => FixedArity(1)
    case (_, "STATS_DATE") => FixedArity(2)
    case (_, "STDEV") => FixedArity(1)
    case (_, "STDEVP") => FixedArity(1)
    case (_, "STR") => VariableArity(1, 3)
    case (_, "STRING_AGG") => VariableArity(2, 3)
    case (_, "STRING_ESCAPE") => FixedArity(2)
    case (_, "STUFF") => FixedArity(4)
    case (_, "SUBSTRING") => VariableArity(2, 3)
    case (_, "SUM") => FixedArity(1)
    case (_, "SUSER_ID") => VariableArity(0, 1)
    case (_, "SUSER_NAME") => VariableArity(0, 1)
    case (_, "SUSER_SID") => VariableArity(0, 2)
    case (_, "SUSER_SNAME") => VariableArity(0, 1)
    case (_, "SWITCHOFFSET") => FixedArity(2)
    case (_, "SYSDATETIME") => FixedArity(0)
    case (_, "SYSDATETIMEOFFSET") => FixedArity(0)
    case (_, "SYSUTCDATETIME") => FixedArity(0)
    case (_, "TAN") => FixedArity(1)
    case (_, "TIMEFROMPARTS") => FixedArity(5)
    case (_, "TODATETIMEOFFSET") => FixedArity(2)
    case (_, "TOSTRING") => FixedArity(0)
    case (_, "TRANSLATE") => FixedArity(3)
    case (_, "TRIM") => VariableArity(1, 2)
    case (_, "TYPE_ID") => FixedArity(1)
    case (_, "TYPE_NAME") => FixedArity(1)
    case (_, "TYPEPROPERTY") => FixedArity(2)
    case (_, "UNICODE") => FixedArity(1)
    case (_, "UPPER") => FixedArity(1)
    case (_, "USER_ID") => VariableArity(0, 1)
    case (_, "USER_NAME") => VariableArity(0, 1)
    case (_, "VALUE") => FixedArity(2, XmlFunction)
    case (_, "VAR") => FixedArity(1)
    case (_, "VARP") => FixedArity(1)
    case (_, "XACT_STATE") => FixedArity(0)
    case (_, "YEAR") => FixedArity(1)
  }

  def functionArity(dialect: SqlDialect, name: String): Option[FunctionArity] =
    functionArityPf.lift((dialect, name.toUpperCase()))

  def functionType(dialect: SqlDialect, name: String): FunctionType = {
    val defnOption = functionArity(dialect, name)
    defnOption match {
      case Some(fixedArity: FixedArity) => fixedArity.functionType
      case Some(variableArity: VariableArity) => variableArity.functionType
      case _ => UnknownFunction
    }
  }

  def buildFunction(name: String, args: Seq[ir.Expression], dialect: SqlDialect): ir.Expression = {
    val irName = removeQuotesAndBrackets(name)
    val defnOption = functionArity(dialect, irName)

    defnOption match {
      case Some(functionArity) if !functionArity.isConvertible =>
        ir.UnresolvedFunction(name, args, is_distinct = false, is_user_defined_function = false)

      case Some(fixedArity: FixedArity) if args.length == fixedArity.arity =>
        applyConversionStrategy(fixedArity, args, irName, dialect)

      case Some(variableArity: VariableArity)
          if args.length >= variableArity.argMin && args.length <= variableArity.argMax =>
        applyConversionStrategy(variableArity, args, irName, dialect)

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
      functionArity: FunctionArity,
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
