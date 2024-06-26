package com.databricks.labs.remorph.parsers.snowflake

import com.databricks.labs.remorph.parsers.snowflake.SnowflakeFunctionConverters.SnowflakeSynonyms
import com.databricks.labs.remorph.parsers.{ConversionStrategy, FunctionBuilder, FunctionDefinition, intermediate => ir}

class SnowflakeFunctionBuilder extends FunctionBuilder {

  private val SnowflakeFunctionDefinitionPf: PartialFunction[String, FunctionDefinition] = {
    case "ADD_MONTHS" => FunctionDefinition.standard(2)
    case "ANY_VALUE" => FunctionDefinition.standard(1)
    case "APPROX_TOP_K" => FunctionDefinition.standard(1, 3)
//    case "ARRAY" => ???
    case "ARRAYS_OVERLAP" => FunctionDefinition.standard(2)
    case "ARRAY_AGG" => FunctionDefinition.standard(1)
    case "ARRAY_APPEND" => FunctionDefinition.standard(2)
    case "ARRAY_CAT" => FunctionDefinition.standard(2)
    case "ARRAY_COMPACT" => FunctionDefinition.standard(1)
    case "ARRAY_CONSTRUCT" => FunctionDefinition.standard(0, Int.MaxValue)
    case "ARRAY_CONSTRUCT_COMPACT" => FunctionDefinition.standard(0, Int.MaxValue)
    case "ARRAY_CONTAINS" => FunctionDefinition.standard(2)
    case "ARRAY_DISTINCT" => FunctionDefinition.standard(1)
    case "ARRAY_EXCEPT" => FunctionDefinition.standard(2)
    case "ARRAY_INSERT" => FunctionDefinition.standard(3)
    case "ARRAY_INTERSECTION" => FunctionDefinition.standard(2)
    case "ARRAY_POSITION" => FunctionDefinition.standard(2)
    case "ARRAY_PREPEND" => FunctionDefinition.standard(2)
    case "ARRAY_REMOVE" => FunctionDefinition.standard(2)
    case "ARRAY_SIZE" => FunctionDefinition.standard(1)
    case "ARRAY_SLICE" => FunctionDefinition.standard(3)
    case "ARRAY_TO_STRING" => FunctionDefinition.standard(2)
    case "ATAN2" => FunctionDefinition.standard(2)
    case "BASE64_DECODE_STRING" => FunctionDefinition.standard(1, 2)
    case "BASE64_ENCODE" => FunctionDefinition.standard(1, 3)
    case "BITOR_AGG" => FunctionDefinition.standard(1)
    case "BOOLAND_AGG" => FunctionDefinition.standard(1)
    case "CEIL" => FunctionDefinition.standard(1, 2)
    case "COLLATE" => FunctionDefinition.standard(2)
    case "COLLATION" => FunctionDefinition.standard(1)
    case "CONTAINS" => FunctionDefinition.standard(2)
    case "CONVERT_TIMEZONE" => FunctionDefinition.standard(2, 3)
    case "CORR" => FunctionDefinition.standard(2)
    case "COUNT_IF" => FunctionDefinition.standard(1)
    case "CURRENT_DATABASE" => FunctionDefinition.standard(0)
    case "CURRENT_TIMESTAMP" => FunctionDefinition.standard(0, 1)
    case "DATE" => FunctionDefinition.standard(1, 2).withConversionStrategy(SnowflakeSynonyms)
    case "DATEDIFF" => FunctionDefinition.standard(3)
    case "DATE_FROM_PARTS" => FunctionDefinition.standard(3)
    case "DATE_PART" => FunctionDefinition.standard(2)
    case "DATE_TRUNC" => FunctionDefinition.standard(2)
    case "DAYNAME" => FunctionDefinition.standard(1)
    case "DECODE" => FunctionDefinition.standard(3, Int.MaxValue)
    case "DENSE_RANK" => FunctionDefinition.standard(0)
    case "DIV0" => FunctionDefinition.standard(2)
    case "DIV0NULL" => FunctionDefinition.standard(2)
    case "ENDSWITH" => FunctionDefinition.standard(2)
    case "EQUAL_NULL" => FunctionDefinition.standard(2)
    // TODO: support named arguments
    case "FLATTEN" => FunctionDefinition.standard(1, 5)
    case "GET" => FunctionDefinition.standard(2)
    case "HASH" => FunctionDefinition.standard(1, Int.MaxValue)
    case "IFNULL" => FunctionDefinition.standard(1, 2)
    case "INITCAP" => FunctionDefinition.standard(1, 2)
    case "ISNULL" => FunctionDefinition.standard(1)
    case "IS_INTEGER" => FunctionDefinition.standard(1)
    case "JSON_EXTRACT_PATH_TEXT" => FunctionDefinition.standard(2)
    case "LAST_DAY" => FunctionDefinition.standard(1, 2)
    case "LPAD" => FunctionDefinition.standard(2, 3)
    case "LTRIM" => FunctionDefinition.standard(1, 2)
    case "MEDIAN" => FunctionDefinition.standard(1)
    case "MOD" => FunctionDefinition.standard(2)
    case "MODE" => FunctionDefinition.standard(1)
    case "MONTHNAME" => FunctionDefinition.standard(1)
//    case "MONTH_NAME" => ???
    case "NEXT_DAY" => FunctionDefinition.standard(2)
//    case "NTH_VALUE" =>
    case "NULLIFZERO" => FunctionDefinition.standard(1)
    case "NVL" => FunctionDefinition.standard(2)
    case "NVL2" => FunctionDefinition.standard(3)
    case "OBJECT_CONSTRUCT" => FunctionDefinition.standard(1, Int.MaxValue)
    case "OBJECT_KEYS" => FunctionDefinition.standard(1)
    case "PARSE_JSON" => FunctionDefinition.standard(1)
    case "PARSE_URL" => FunctionDefinition.standard(1, 2)
    case "POSITION" => FunctionDefinition.standard(2, 3)
    case "RANDOM" => FunctionDefinition.standard(0, 1)
    case "RANK" => FunctionDefinition.standard(0)
    case "REGEXP_COUNT" => FunctionDefinition.standard(2, 4)
    case "REGEXP_INSTR" => FunctionDefinition.standard(2, 7)
    case "REGEXP_LIKE" => FunctionDefinition.standard(2, 3)
    case "REGEXP_REPLACE" => FunctionDefinition.standard(2, 6)
    case "REGEXP_SUBSTR" => FunctionDefinition.standard(2, 6)
    case "REGR_INTERCEPT" => FunctionDefinition.standard(2)
    case "REGR_R2" => FunctionDefinition.standard(2)
    case "REGR_SLOPE" => FunctionDefinition.standard(2)
    case "REPEAT" => FunctionDefinition.standard(2)
    case "RLIKE" => FunctionDefinition.standard(2, 3)
    case "ROUND" => FunctionDefinition.standard(1, 3)
    case "RPAD" => FunctionDefinition.standard(2, 3)
    case "RTRIM" => FunctionDefinition.standard(1, 2)
    case "SPLIT_PART" => FunctionDefinition.standard(3)
    case "SQUARE" => FunctionDefinition.standard(1)
    case "STARTSWITH" => FunctionDefinition.standard(2)
    case "STDDEV" => FunctionDefinition.standard(1)
    case "STDDEV_POP" => FunctionDefinition.standard(1)
    case "STDDEV_SAMP" => FunctionDefinition.standard(1)
    case "STRIP_NULL_VALUE" => FunctionDefinition.standard(1)
    case "STRTOK" => FunctionDefinition.standard(1, 3)
    case "STRTOK_TO_ARRAY" => FunctionDefinition.standard(1, 2)
    case "SYSDATE" => FunctionDefinition.standard(0)
    case "TIME" => FunctionDefinition.standard(1, 2).withConversionStrategy(SnowflakeSynonyms)
    case "TIMEADD" => FunctionDefinition.standard(3)
    case "TIMESTAMPADD" => FunctionDefinition.standard(3)
    case "TIMESTAMPDIFF" => FunctionDefinition.standard(3)
    case "TIMESTAMP_FROM_PARTS" => FunctionDefinition.standard(2, 8)
    case "TO_ARRAY" => FunctionDefinition.standard(1)
    case "TO_BOOLEAN" => FunctionDefinition.standard(1)
    case "TO_CHAR" => FunctionDefinition.standard(1, 2).withConversionStrategy(SnowflakeSynonyms)
    case "TO_DATE" => FunctionDefinition.standard(1, 2)
    case "TO_DECIMAL" => FunctionDefinition.standard(1, 4)
    case "TO_DOUBLE" => FunctionDefinition.standard(1, 2)
    case "TO_JSON" => FunctionDefinition.standard(1)
    case "TO_NUMBER" => FunctionDefinition.standard(1, 4)
    case "TO_NUMERIC" => FunctionDefinition.standard(1, 4)
    case "TO_OBJECT" => FunctionDefinition.standard(1)
    case "TO_TIME" => FunctionDefinition.standard(1, 2)
    case "TO_TIMESTAMP" => FunctionDefinition.standard(1, 2)
    case "TO_TIMESTAMP_LTZ" => FunctionDefinition.standard(1, 2)
    case "TO_TIMESTAMP_NTZ" => FunctionDefinition.standard(1, 2)
    case "TO_TIMESTAMP_TZ" => FunctionDefinition.standard(1, 2)
    case "TO_VARCHAR" => FunctionDefinition.standard(1, 2)
    case "TO_VARIANT" => FunctionDefinition.standard(1)
    case "TRIM" => FunctionDefinition.standard(1, 2)
    case "TRUNC" => FunctionDefinition.standard(2)
    case "TRY_BASE64_DECODE_STRING" => FunctionDefinition.standard(1, 2)
    case "TRY_PARSE_JSON" => FunctionDefinition.standard(1)
    case "TRY_TO_BINARY" => FunctionDefinition.standard(1, 2)
    case "TRY_TO_BOOLEAN" => FunctionDefinition.standard(1)
    case "TRY_TO_DATE" => FunctionDefinition.standard(1, 2)
    case "TRY_TO_DECIMAL" => FunctionDefinition.standard(1, 4)
    case "TRY_TO_DOUBLE" => FunctionDefinition.standard(1, 2)
    case "TRY_TO_NUMBER" => FunctionDefinition.standard(1, 4)
    case "TRY_TO_NUMERIC" => FunctionDefinition.standard(1, 4)
    case "TRY_TO_TIME" => FunctionDefinition.standard(1, 2)
    case "TRY_TO_TIMESTAMP" => FunctionDefinition.standard(1, 2)
    case "TRY_TO_TIMESTAMP_LTZ" => FunctionDefinition.standard(1, 2)
    case "TRY_TO_TIMESTAMP_NTZ" => FunctionDefinition.standard(1, 2)
    case "TRY_TO_TIMESTAMP_TZ" => FunctionDefinition.standard(1, 2)
    case "TYPEOF" => FunctionDefinition.standard(1)
    case "UUID_STRING" => FunctionDefinition.standard(0, 2)
    case "ZEROIFNULL" => FunctionDefinition.standard(1)

  }

  override def functionDefinition(name: String): Option[FunctionDefinition] =
    // If not found, check common functions
    SnowflakeFunctionDefinitionPf.orElse(commonFunctionsPf).lift(name.toUpperCase())

  def applyConversionStrategy(
      functionArity: FunctionDefinition,
      args: Seq[ir.Expression],
      irName: String): ir.Expression = {
    functionArity.conversionStrategy match {
      case Some(strategy) => strategy.convert(irName, args)
      case _ => ir.CallFunction(irName, args)
    }
  }
}

object SnowflakeFunctionConverters {

  object SnowflakeSynonyms extends ConversionStrategy {
    override def convert(irName: String, args: Seq[ir.Expression]): ir.Expression = {
      irName.toUpperCase() match {
        case "DATE" => ir.CallFunction("TO_DATE", args)
        case "TIME" => ir.CallFunction("TO_TIME", args)
        case "TO_CHAR" => ir.CallFunction("TO_VARCHAR", args)
        case _ => ir.CallFunction(irName, args)
      }
    }
  }
}
