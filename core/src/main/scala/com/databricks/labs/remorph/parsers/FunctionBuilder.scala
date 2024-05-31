package com.databricks.labs.remorph.parsers

import com.databricks.labs.remorph.parsers.{intermediate => ir}

import java.util.Locale

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

  def functionArity(dialect: SqlDialect, functionName: String): Option[FunctionArity] = (dialect, functionName) match {
    case (_, "ABS") => Some(FixedArity(1))
    case (_, "ACOS") => Some(FixedArity(1))
    case (_, "APP_NAME") => Some(FixedArity(0))
    case (_, "APPLOCK_MODE") => Some(FixedArity(3))
    case (_, "APPLOCK_TEST") => Some(FixedArity(4))
    case (_, "ASCII") => Some(FixedArity(1))
    case (_, "ASIN") => Some(FixedArity(1))
    case (_, "ASSEMBLYPROPERTY") => Some(FixedArity(2))
    case (_, "ATAN") => Some(FixedArity(1))
    case (_, "ATN2") => Some(FixedArity(2))
    case (_, "AVG") => Some(FixedArity(1))
    case (_, "CEILING") => Some(FixedArity(1))
    case (_, "CERT_ID") => Some(FixedArity(1))
    case (_, "CERTENCODED") => Some(FixedArity(1))
    case (_, "CERTPRIVATEKEY") => Some(VariableArity(2, 3))
    case (_, "CHAR") => Some(FixedArity(1))
    case (_, "CHARINDEX") => Some(VariableArity(2, 3))
    case (_, "CHECKSUM_AGG") => Some(FixedArity(1))
    case (_, "COALESCE") => Some(VariableArity(1, Int.MaxValue))
    case (_, "COL_LENGTH") => Some(FixedArity(2))
    case (_, "COL_NAME") => Some(FixedArity(2))
    case (_, "COLUMNPROPERTY") => Some(FixedArity(3))
    case (_, "COMPRESS") => Some(FixedArity(1))
    case (_, "CONCAT") => Some(VariableArity(2, Int.MaxValue))
    case (_, "CONCAT_WS") => Some(VariableArity(3, Int.MaxValue))
    case (_, "CONNECTIONPROPERTY") => Some(FixedArity(1, convertible = false))
    case (_, "CONTEXT_INFO") => Some(FixedArity(0))
    case (_, "CONVERT") => Some(VariableArity(2, 3))
    case (_, "COS") => Some(FixedArity(1))
    case (_, "COT") => Some(FixedArity(1))
    case (_, "COUNT") => Some(FixedArity(1))
    case (_, "COUNT_BIG") => Some(FixedArity(1))
    case (_, "CURRENT_DATE") => Some(FixedArity(0))
    case (_, "CURRENT_REQUEST_ID") => Some(FixedArity(0))
    case (_, "CURRENT_TIMESTAMP") => Some(FixedArity(0))
    case (_, "CURRENT_TIMEZONE") => Some(FixedArity(0))
    case (_, "CURRENT_TIMEZONE_ID") => Some(FixedArity(0))
    case (_, "CURRENT_TRANSACTION_ID") => Some(FixedArity(0))
    case (_, "CURRENT_USER") => Some(FixedArity(0))
    case (_, "CURSOR_STATUS") => Some(FixedArity(2))
    case (_, "DATABASE_PRINCIPAL_ID") => Some(VariableArity(0, 1))
    case (_, "DATABASEPROPERTY") => Some(FixedArity(2))
    case (_, "DATABASEPROPERTYEX") => Some(FixedArity(2))
    case (_, "DATALENGTH") => Some(FixedArity(1))
    case (_, "DATE_BUCKET") => Some(VariableArity(3, 4))
    case (_, "DATE_DIFF_BIG") => Some(FixedArity(3))
    case (_, "DATEADD") => Some(FixedArity(3))
    case (_, "DATEDIFF") => Some(FixedArity(3))
    case (_, "DATEFROMPARTS") => Some(FixedArity(3))
    case (_, "DATENAME") => Some(FixedArity(2))
    case (_, "DATEPART") => Some(FixedArity(2))
    case (_, "DATETIME2FROMPARTS") => Some(FixedArity(8))
    case (_, "DATETIMEFROMPARTS") => Some(FixedArity(7))
    case (_, "DATETIMEOFFSETFROMPARTS") => Some(FixedArity(10))
    case (_, "DATETRUNC") => Some(FixedArity(2))
    case (_, "DAY") => Some(FixedArity(1))
    case (_, "DB_ID") => Some(VariableArity(0, 1))
    case (_, "DB_NAME") => Some(VariableArity(0, 1))
    case (_, "DECOMPRESS") => Some(FixedArity(1))
    case (_, "DEGREES") => Some(FixedArity(1))
    case (_, "DENSE_RANK") => Some(FixedArity(0))
    case (_, "DIFFERENCE") => Some(FixedArity(2))
    case (_, "EOMONTH") => Some(VariableArity(1, 2))
    case (_, "ERROR_LINE") => Some(FixedArity(0))
    case (_, "ERROR_MESSAGE") => Some(FixedArity(0))
    case (_, "ERROR_NUMBER") => Some(FixedArity(0))
    case (_, "ERROR_PROCEDURE") => Some(FixedArity(0))
    case (_, "ERROR_SEVERITY") => Some(FixedArity(0))
    case (_, "ERROR_STATE") => Some(FixedArity(0))
    case (_, "EXIST") => Some(FixedArity(1, XmlFunction))
    case (_, "EXP") => Some(FixedArity(1))
    case (_, "FILE_ID") => Some(FixedArity(1))
    case (_, "FILE_IDEX") => Some(FixedArity(1))
    case (_, "FILE_NAME") => Some(FixedArity(1))
    case (_, "FILEGROUP_ID") => Some(FixedArity(1))
    case (_, "FILEGROUP_NAME") => Some(FixedArity(1))
    case (_, "FILEGROUPPROPERTY") => Some(FixedArity(2))
    case (_, "FILEPROPERTY") => Some(FixedArity(2))
    case (_, "FILEPROPERTYEX") => Some(FixedArity(2))
    case (_, "FLOOR") => Some(FixedArity(1))
    case (_, "FORMAT") => Some(VariableArity(2, 3))
    case (_, "FORMATMESSAGE") => Some(VariableArity(2, Int.MaxValue))
    case (_, "FULLTEXTCATALOGPROPERTY") => Some(FixedArity(2))
    case (_, "FULLTEXTSERVICEPROPERTY") => Some(FixedArity(1))
    case (_, "GET_FILESTREAM_TRANSACTION_CONTEXT") => Some(FixedArity(0))
    case (_, "GETANCESTGOR") => Some(FixedArity(1))
    case (_, "GETANSINULL") => Some(VariableArity(0, 1))
    case (_, "GETDATE") => Some(FixedArity(0))
    case (_, "GETDESCENDANT") => Some(FixedArity(2))
    case (_, "GETLEVEL") => Some(FixedArity(0))
    case (_, "GETREPARENTEDVALUE") => Some(FixedArity(2))
    case (_, "GETUTCDATE") => Some(FixedArity(0))
    case (_, "GREATEST") => Some(VariableArity(1, Int.MaxValue))
    case (_, "GROUPING") => Some(FixedArity(1))
    case (_, "GROUPING_ID") => Some(VariableArity(0, Int.MaxValue))
    case (_, "HAS_DBACCESS") => Some(FixedArity(1))
    case (_, "HAS_PERMS_BY_NAME") => Some(VariableArity(4, 5))
    case (_, "HOST_ID") => Some(FixedArity(0))
    case (_, "HOST_NAME") => Some(FixedArity(0))
    case (_, "IDENT_CURRENT") => Some(FixedArity(1))
    case (_, "IDENT_INCR") => Some(FixedArity(1))
    case (_, "IDENT_SEED") => Some(FixedArity(1))
    case (Snowflake, "IFNULL") => Some(FixedArity(2))
    case (_, "IFF") => Some(FixedArity(3))
    case (_, "INDEX_COL") => Some(FixedArity(3))
    case (_, "INDEXKEY_PROPERTY") => Some(FixedArity(3))
    case (_, "INDEXPROPERTY") => Some(FixedArity(3))
    case (_, "IS_MEMBER") => Some(FixedArity(1))
    case (_, "IS_ROLEMEMBER") => Some(VariableArity(1, 2))
    case (_, "IS_SRVROLEMEMBER") => Some(VariableArity(1, 2))
    case (_, "ISDATE") => Some(FixedArity(1))
    case (_, "ISDESCENDANTOF") => Some(FixedArity(1))
    case (_, "ISJSON") => Some(VariableArity(1, 2))
    // The ConversionStrategy is used to rename ISNULL to IFNULL in TSql
    case (TSql, "ISNULL") => Some(VariableArity(1, 2, conversionStrategy = Some(FunctionConverters.FunctionRename)))
    case (_, "ISNUMERIC") => Some(FixedArity(1))
    case (_, "JSON_MODIFY") => Some(FixedArity(3))
    case (_, "JSON_PATH_EXISTS") => Some(FixedArity(2))
    case (_, "JSON_QUERY") => Some(FixedArity(2))
    case (_, "JSON_VALUE") => Some(FixedArity(2))
    case (_, "LEAST") => Some(VariableArity(1, Int.MaxValue))
    case (_, "LEFT") => Some(FixedArity(2))
    case (_, "LEN") => Some(FixedArity(1))
    case (_, "LOG") => Some(VariableArity(1, 2))
    case (_, "LOG10") => Some(FixedArity(1))
    case (_, "LOGINPROPERTY") => Some(FixedArity(2))
    case (_, "LOWER") => Some(FixedArity(1))
    case (_, "LTRIM") => Some(FixedArity(1))
    case (_, "MAX") => Some(FixedArity(1))
    case (_, "MIN") => Some(FixedArity(1))
    case (_, "MIN_ACTIVE_ROWVERSION") => Some(FixedArity(0))
    case (_, "MODIFY") => Some(FixedArity(1, XmlFunction))
    case (_, "MONTH") => Some(FixedArity(1))
    case (_, "NCHAR") => Some(FixedArity(1))
    case (_, "NEWID") => Some(FixedArity(0))
    case (_, "NEWSEQUENTIALID") => Some(FixedArity(0))
    case (_, "NODES") => Some(FixedArity(1, XmlFunction))
    case (_, "NTILE") => Some(FixedArity(1))
    case (_, "NULLIF") => Some(FixedArity(2))
    case (_, "OBJECT_DEFINITION") => Some(FixedArity(1))
    case (_, "OBJECT_ID") => Some(VariableArity(1, 2))
    case (_, "OBJECT_NAME") => Some(VariableArity(1, 2))
    case (_, "OBJECT_SCHEMA_NAME") => Some(VariableArity(1, 2))
    case (_, "OBJECTPROPERTY") => Some(FixedArity(2))
    case (_, "OBJECTPROPERTYEX") => Some(FixedArity(2))
    case (_, "ORIGINAL_DB_NAME") => Some(FixedArity(0))
    case (_, "ORIGINAL_LOGIN") => Some(FixedArity(0))
    case (_, "PARSE") => Some(VariableArity(2, 3, convertible = false)) // Not in DBSQL
    case (_, "PARSENAME") => Some(FixedArity(2))
    case (_, "PATINDEX") => Some(FixedArity(2))
    case (_, "PERMISSIONS") => Some(VariableArity(0, 2, convertible = false)) // not in DBSQL
    case (_, "PI") => Some(FixedArity(0))
    case (_, "POWER") => Some(FixedArity(2))
    case (_, "PWDCOMPARE") => Some(VariableArity(2, 3))
    case (_, "PWDENCRYPT") => Some(FixedArity(1))
    case (_, "QUERY") => Some(FixedArity(1, XmlFunction))
    case (_, "QUOTENAME") => Some(VariableArity(1, 2))
    case (_, "RADIANS") => Some(FixedArity(1))
    case (_, "RAND") => Some(VariableArity(0, 1))
    case (_, "RANK") => Some(FixedArity(0))
    case (_, "REPLACE") => Some(FixedArity(3))
    case (_, "REPLICATE") => Some(FixedArity(2))
    case (_, "REVERSE") => Some(FixedArity(1))
    case (_, "RIGHT") => Some(FixedArity(2))
    case (_, "ROUND") => Some(VariableArity(2, 3))
    case (_, "ROW_NUMBER") => Some(FixedArity(0))
    case (_, "ROWCOUNT_BIG") => Some(FixedArity(0))
    case (_, "RTRIM") => Some(FixedArity(1))
    case (_, "SCHEMA_ID") => Some(VariableArity(0, 1))
    case (_, "SCHEMA_NAME") => Some(VariableArity(0, 1))
    case (_, "SCOPE_IDENTITY") => Some(FixedArity(0))
    case (_, "SERVERPROPERTY") => Some(FixedArity(1))
    case (_, "SESSION_CONTEXT") => Some(VariableArity(1, 2))
    case (_, "SESSIONPROPERTY") => Some(FixedArity(1))
    case (_, "SIGN") => Some(FixedArity(1))
    case (_, "SIN") => Some(FixedArity(1))
    case (_, "SMALLDATETIMEFROMPARTS") => Some(FixedArity(5))
    case (_, "SOUNDEX") => Some(FixedArity(1))
    case (_, "SPACE") => Some(FixedArity(1))
    case (_, "SQL_VARIANT_PROPERTY") => Some(FixedArity(2))
    case (_, "SQRT") => Some(FixedArity(1))
    case (_, "SQUARE") => Some(FixedArity(1))
    case (_, "STATS_DATE") => Some(FixedArity(2))
    case (_, "STDEV") => Some(FixedArity(1))
    case (_, "STDEVP") => Some(FixedArity(1))
    case (_, "STR") => Some(VariableArity(1, 3))
    case (_, "STRING_AGG") => Some(VariableArity(2, 3))
    case (_, "STRING_ESCAPE") => Some(FixedArity(2))
    case (_, "STUFF") => Some(FixedArity(4))
    case (_, "SUBSTRING") => Some(VariableArity(2, 3))
    case (_, "SUM") => Some(FixedArity(1))
    case (_, "SUSER_ID") => Some(VariableArity(0, 1))
    case (_, "SUSER_NAME") => Some(VariableArity(0, 1))
    case (_, "SUSER_SID") => Some(VariableArity(0, 2))
    case (_, "SUSER_SNAME") => Some(VariableArity(0, 1))
    case (_, "SWITCHOFFSET") => Some(FixedArity(2))
    case (_, "SYSDATETIME") => Some(FixedArity(0))
    case (_, "SYSDATETIMEOFFSET") => Some(FixedArity(0))
    case (_, "SYSUTCDATETIME") => Some(FixedArity(0))
    case (_, "TAN") => Some(FixedArity(1))
    case (_, "TIMEFROMPARTS") => Some(FixedArity(5))
    case (_, "TODATETIMEOFFSET") => Some(FixedArity(2))
    case (_, "TOSTRING") => Some(FixedArity(0))
    case (_, "TRANSLATE") => Some(FixedArity(3))
    case (_, "TRIM") => Some(VariableArity(1, 2))
    case (_, "TYPE_ID") => Some(FixedArity(1))
    case (_, "TYPE_NAME") => Some(FixedArity(1))
    case (_, "TYPEPROPERTY") => Some(FixedArity(2))
    case (_, "UNICODE") => Some(FixedArity(1))
    case (_, "UPPER") => Some(FixedArity(1))
    case (_, "USER_ID") => Some(VariableArity(0, 1))
    case (_, "USER_NAME") => Some(VariableArity(0, 1))
    case (_, "VALUE") => Some(FixedArity(2, XmlFunction))
    case (_, "VAR") => Some(FixedArity(1))
    case (_, "VARP") => Some(FixedArity(1))
    case (_, "XACT_STATE") => Some(FixedArity(0))
    case (_, "YEAR") => Some(FixedArity(1))
    case _ => None
  }

  def functionType(dialect: SqlDialect, name: String): FunctionType = {
    val uName = name.toUpperCase(Locale.getDefault())
    val defnOption = functionArity(dialect, uName)
    defnOption match {
      case Some(fixedArity: FixedArity) => fixedArity.functionType
      case Some(variableArity: VariableArity) => variableArity.functionType
      case _ => UnknownFunction
    }
  }

  def buildFunction(name: String, args: Seq[ir.Expression], dialect: SqlDialect): ir.Expression = {
    val irName = removeQuotesAndBrackets(name)
    val uName = irName.toUpperCase(Locale.getDefault())
    val defnOption = functionArity(dialect, uName)

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
