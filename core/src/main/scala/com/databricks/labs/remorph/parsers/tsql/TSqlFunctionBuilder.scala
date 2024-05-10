package com.databricks.labs.remorph.parsers.tsql

import com.databricks.labs.remorph.parsers.tsql.TSqlParser.{ExpressionListContext, StandardFunctionContext}
import com.databricks.labs.remorph.parsers.{intermediate => ir}

import java.util.Locale
import scala.collection.convert.ImplicitConversions.`collection AsScalaIterable`

case class FunDef(argMin: Int, argMax: Int = Int.MaxValue, convertible: Boolean = true)

class TSqlFunctionBuilder extends TSqlExpressionBuilder {

  // TODO: Add more functions as we find them
  val functions: Map[String, FunDef] = Map(
    "APP_NAME" -> FunDef(0, 0),
    "APPLOCK_MODE" -> FunDef(3, 3),
    "APPLOCK_TEST" -> FunDef(4, 4),
    "ASSEMBLYPROPERTY" -> FunDef(2, 2),
    "COL_LENGTH" -> FunDef(2, 2),
    "COL_NAME" -> FunDef(2, 2),
    "COLUMNPROPERTY" -> FunDef(3, 3),
    "DATABASEPROPERTY" -> FunDef(2, 2),
    "DATABASEPROPERTYEX" -> FunDef(2, 2),
    "DB_ID" -> FunDef(0, 1),
    "DB_NAME" -> FunDef(0, 1),
    "FILE_ID" -> FunDef(1, 1),
    "FILE_IDEX" -> FunDef(1, 1),
    "FILE_NAME" -> FunDef(1, 1),
    "FILEGROUP_ID" -> FunDef(1, 1),
    "FILEGROUP_NAME" -> FunDef(1, 1),
    "FILEGROUPPROPERTY" -> FunDef(2, 2),
    "FILEPROPERTY" -> FunDef(2, 2),
    "FILEPROPERTYEX" -> FunDef(2, 2),
    "FULLTEXTCATALOGPROPERTY" -> FunDef(2, 2),
    "FULLTEXTSERVICEPROPERTY" -> FunDef(1, 1),
    "INDEX_COL" -> FunDef(3, 3),
    "INDEXKEY_PROPERTY" -> FunDef(3, 3),
    "INDEXPROPERTY" -> FunDef(3, 3),
    "OBJECT_DEFINITION" -> FunDef(1, 1),
    "OBJECT_ID" -> FunDef(1, 2),
    "OBJECT_NAME" -> FunDef(1, 2),
    "OBJECT_SCHEMA_NAME" -> FunDef(1, 2),
    "OBJECTPROPERTY" -> FunDef(2, 2),
    "OBJECTPROPERTYEX" -> FunDef(2, 2),
    "ORIGINAL_DB_NAME" -> FunDef(0, 0),
    "PARSENAME" -> FunDef(2, 2),
    "SCHEMA_ID" -> FunDef(0, 1),
    "SCHEMA_NAME" -> FunDef(0, 1),
    "SCOPE_IDENTITY" -> FunDef(0, 0),
    "SERVERPROPERTY" -> FunDef(1, 1),
    "STATS_DATE" -> FunDef(2, 2),
    "TYPE_ID" -> FunDef(1, 1),
    "TYPE_NAME" -> FunDef(1, 1),
    "TYPEPROPERTY" -> FunDef(2, 2),
    "ASCII" -> FunDef(1, 1),
    "CHAR" -> FunDef(1, 1),
    "CHARINDEX" -> FunDef(2, 3),
    "CONCAT" -> FunDef(2, Int.MaxValue),
    "CONCAT_WS" -> FunDef(3, Int.MaxValue),
    "DIFFERENCE" -> FunDef(2, 2),
    "FORMAT" -> FunDef(2, 3),
    "LEFT" -> FunDef(2, 2),
    "LEN" -> FunDef(1, 1),
    "LOWER" -> FunDef(1, 1),
    "LTRIM" -> FunDef(1, 1),
    "NCHAR" -> FunDef(1, 1),
    "PATINDEX" -> FunDef(2, 2),
    "QUOTENAME" -> FunDef(1, 2),
    "REPLACE" -> FunDef(3, 3),
    "REPLICATE" -> FunDef(2, 2),
    "REVERSE" -> FunDef(1, 1),
    "RIGHT" -> FunDef(2, 2),
    "RTRIM" -> FunDef(1, 1),
    "SOUNDEX" -> FunDef(1, 1),
    "SPACE" -> FunDef(1, 1),
    "STR" -> FunDef(1, 3),
    "STRING_AGG" -> FunDef(2, 3),
    "STRING_ESCAPE" -> FunDef(2, 2),
    "STUFF" -> FunDef(4, 4),
    "SUBSTRING" -> FunDef(2, 3),
    "TRANSLATE" -> FunDef(3, 3),
    "TRIM" -> FunDef(1, 2),
    "UNICODE" -> FunDef(1, 1),
    "UPPER" -> FunDef(1, 1),
    "COMPRESS" -> FunDef(1, 1),
    "CONNECTIONPROPERTY" -> FunDef(1, 1),
    "CONTEXT_INFO" -> FunDef(0, 0),
    "CURRENT_REQUEST_ID" -> FunDef(0, 0),
    "CURRENT_TRANSACTION_ID" -> FunDef(0, 0),
    "DECOMPRESS" -> FunDef(1, 1),
    "ERROR_LINE" -> FunDef(0, 0),
    "ERROR_MESSAGE" -> FunDef(0, 0),
    "ERROR_NUMBER" -> FunDef(0, 0),
    "ERROR_PROCEDURE" -> FunDef(0, 0),
    "ERROR_SEVERITY" -> FunDef(0, 0),
    "ERROR_STATE" -> FunDef(0, 0),
    "FORMATMESSAGE" -> FunDef(2, Int.MaxValue),
    "GET_FILESTREAM_TRANSACTION_CONTEXT" -> FunDef(0, 0),
    "GETANSINULL" -> FunDef(0, 1),
    "HOST_ID" -> FunDef(0, 0),
    "HOST_NAME" -> FunDef(0, 0),
    "ISNULL" -> FunDef(2, 2),
    "ISNUMERIC" -> FunDef(1, 1),
    "MIN_ACTIVE_ROWVERSION" -> FunDef(0, 0),
    "NEWID" -> FunDef(0, 0),
    "NEWSEQUENTIALID" -> FunDef(0, 0),
    "ROWCOUNT_BIG" -> FunDef(0, 0),
    "SESSION_CONTEXT" -> FunDef(1, 2),
    "XACT_STATE" -> FunDef(0, 0),
    "CONVERT" -> FunDef(2, 3),
    "COALESCE" -> FunDef(1, Int.MaxValue),
    "CURSOR_STATUS" -> FunDef(2, 2),
    "CERT_ID" -> FunDef(1, 1),
    "DATALENGTH" -> FunDef(1, 1),
    "IDENT_CURRENT" -> FunDef(1, 1),
    "IDENT_INCR" -> FunDef(1, 1),
    "IDENT_SEED" -> FunDef(1, 1),
    "SQL_VARIANT_PROPERTY" -> FunDef(2, 2),
    "CURRENT_DATE" -> FunDef(0, 0),
    "CURRENT_TIMESTAMP" -> FunDef(0, 0),
    "CURRENT_TIMEZONE" -> FunDef(0, 0),
    "CURRENT_TIMEZONE_ID" -> FunDef(0, 0),
    "DATE_BUCKET" -> FunDef(3, 4),
    "DATEADD" -> FunDef(3, 3),
    "DATEDIFF" -> FunDef(3, 3),
    "DATE_DIFF_BIG" -> FunDef(3, 3),
    "DATEFROMPARTS" -> FunDef(3, 3),
    "DATENAME" -> FunDef(2, 2),
    "DATEPART" -> FunDef(2, 2),
    "DATETIME2FROMPARTS" -> FunDef(8, 8),
    "DATETIMEFROMPARTS" -> FunDef(7, 7),
    "DATETIMEOFFSETFROMPARTS" -> FunDef(10, 10),
    "DATETRUNC" -> FunDef(2, 2),
    "DAY" -> FunDef(1, 1),
    "EOMONTH" -> FunDef(1, 2),
    "GETDATE" -> FunDef(0, 0),
    "GETUTCDATE" -> FunDef(0, 0),
    "ISDATE" -> FunDef(1, 1),
    "MONTH" -> FunDef(1, 1),
    "SMALLDATETIMEFROMPARTS" -> FunDef(5, 5),
    "SWITCHOFFSET" -> FunDef(2, 2),
    "SYSDATETIME" -> FunDef(0, 0),
    "SYSDATETIMEOFFSET" -> FunDef(0, 0),
    "SYSUTCDATETIME" -> FunDef(0, 0),
    "TIMEFROMPARTS" -> FunDef(5, 5),
    "TODATETIMEOFFSET" -> FunDef(2, 2),
    "YEAR" -> FunDef(1, 1),
    "MIN_ACTIVE_ROWVERSION" -> FunDef(0, 0),
    "NULLIF" -> FunDef(2, 2),
    "PARSE" -> FunDef(2, 3),
    "IFF" -> FunDef(3, 3),
    "ISJSON" -> FunDef(1, 2),
    "JSON_VALUE" -> FunDef(2, 2),
    "JSON_QUERY" -> FunDef(2, 2),
    "JSON_MODIFY" -> FunDef(3, 3),
    "JSON_PATH_EXISTS" -> FunDef(2, 2),
    "ABS" -> FunDef(1, 1),
    "ACOS" -> FunDef(1, 1),
    "ASIN" -> FunDef(1, 1),
    "ATAN" -> FunDef(1, 1),
    "ATN2" -> FunDef(2, 2),
    "CEILING" -> FunDef(1, 1),
    "COS" -> FunDef(1, 1),
    "COT" -> FunDef(1, 1),
    "DEGREES" -> FunDef(1, 1),
    "EXP" -> FunDef(1, 1),
    "FLOOR" -> FunDef(1, 1),
    "LOG" -> FunDef(1, 2),
    "LOG10" -> FunDef(1, 1),
    "PI" -> FunDef(0, 0),
    "POWER" -> FunDef(2, 2),
    "RADIANS" -> FunDef(1, 1),
    "RAND" -> FunDef(0, 1),
    "ROUND" -> FunDef(2, 3),
    "SIGN" -> FunDef(1, 1),
    "SIN" -> FunDef(1, 1),
    "SQRT" -> FunDef(1, 1),
    "SQUARE" -> FunDef(1, 1),
    "TAN" -> FunDef(1, 1),
    "GREATEST" -> FunDef(1, Int.MaxValue),
    "LEAST" -> FunDef(1, Int.MaxValue),
    "CERTENCODED" -> FunDef(1, 1),
    "CERTPRIVATEKEY" -> FunDef(2, 3),
    "CURRENT_USER" -> FunDef(0, 0),
    "DATABASE_PRINCIPAL_ID" -> FunDef(0, 1),
    "HAS_DBACCESS" -> FunDef(1, 1),
    "HAS_PERMS_BY_NAME" -> FunDef(4, 5),
    "IS_MEMBER" -> FunDef(1, 1),
    "IS_ROLEMEMBER" -> FunDef(1, 2),
    "IS_SRVROLEMEMBER" -> FunDef(1, 2),
    "LOGINPROPERTY" -> FunDef(2, 2),
    "ORIGINAL_LOGIN" -> FunDef(0, 0),
    "PERMISSIONS" -> FunDef(0, 2),
    "PWDENCRYPT" -> FunDef(1, 1),
    "PWDCOMPARE" -> FunDef(2, 3),
    "SESSIONPROPERTY" -> FunDef(1, 1),
    "SUSER_ID" -> FunDef(0, 1),
    "SUSER_NAME" -> FunDef(0, 1),
    "SUSER_SID" -> FunDef(0, 2),
    "SUSER_SNAME" -> FunDef(0, 1),
    "USER_ID" -> FunDef(0, 1),
    "USER_NAME" -> FunDef(0, 1))

  override def visitStandardFunction(ctx: StandardFunctionContext): ir.Expression = {
    val name = ctx.id_.getText.toUpperCase(Locale.getDefault())
    val defnOption = functions.get(name)

    val args = ctx.expressionList() match {
      case null => Seq.empty
      case list =>
        list.accept(this) match {
          case exprList: ir.ExpressionList => exprList.expressions
          case _ => Seq.empty
        }
    }

    defnOption match {
      case None =>
        // We do not know if this is a user defined function or a built-in function that we do not know about
        // Later we can track user defined functions.
        ir.UnresolvedFunction(name, args, is_distinct = false, is_user_defined_function = false)

      case Some(defn) =>
        if (args.size < defn.argMin || args.size > defn.argMax) {
          // TODO: This should be a semantic error
          throw new IllegalArgumentException(
            s"Function $name expects between ${defn.argMin} and ${defn.argMax} arguments")
        }
        ir.CallFunction(name, args)
    }
  }

  override def visitExpressionList(ctx: ExpressionListContext): ir.ExpressionList =
    ir.ExpressionList(ctx.expression().toList.map(_.accept(this).asInstanceOf[ir.Expression]))
}
