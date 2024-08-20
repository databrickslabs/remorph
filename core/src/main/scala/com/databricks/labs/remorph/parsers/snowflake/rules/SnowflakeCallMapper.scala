package com.databricks.labs.remorph.parsers.snowflake.rules

import com.databricks.labs.remorph.parsers.{intermediate => ir}
import com.databricks.labs.remorph.transpilers.TranspileException

class SnowflakeCallMapper extends ir.CallMapper with ir.IRHelpers {

  override def convert(call: ir.Fn): ir.Expression = {
    withNormalizedName(call) match {
      // keep all the names in alphabetical order
      case ir.CallFunction("ARRAY_CAT", args) => ir.Concat(args)
      case ir.CallFunction("ARRAY_CONSTRUCT", args) => ir.CreateArray(args)
      case ir.CallFunction("ARRAY_SLICE", args) => ir.Slice(args.head, args(1), args(2))
      case ir.CallFunction("BASE64_DECODE_STRING", args) => ir.UnBase64(args.head)
      case ir.CallFunction("BASE64_DECODE_BINARY", args) => ir.UnBase64(args.head)
      case ir.CallFunction("BASE64_ENCODE", args) => ir.Base64(args.head)
      case ir.CallFunction("BOOLAND_AGG", args) => ir.BoolAnd(args.head)
      case ir.CallFunction("CURRENT_TIMESTAMP", _) => ir.CurrentTimestamp()
      case ir.CallFunction("DATEADD", args) => dateAdd(args)
      case ir.CallFunction("DATEDIFF", args) => dateDiff(args)
      case ir.CallFunction("DATE_FROM_PARTS", args) => ir.MakeDate(args.head, args(1), args(2))
      case ir.CallFunction("DATE_PART", args) => datePart(args)
      case ir.CallFunction("DATE_TRUNC", args) => dateTrunc(args)
      case ir.CallFunction("DAYNAME", args) => dayname(args)
      case ir.CallFunction("EDITDISTANCE", args) => ir.Levenshtein(args.head, args(1))
      case ir.CallFunction("IFNULL", args) => ir.Coalesce(args)
      case ir.CallFunction("JSON_EXTRACT_PATH_TEXT", args) => getJsonObject(args)
      case ir.CallFunction("LEN", args) => ir.Length(args.head)
      case ir.CallFunction("LISTAGG", args) => ir.ArrayJoin(args.head, ir.CollectList(args(1), None), None)
      case ir.CallFunction("MONTHNAME", args) => ir.DateFormatClass(args.head, ir.Literal("MMM"))
      case ir.CallFunction("OBJECT_KEYS", args) => ir.JsonObjectKeys(args.head)
      case ir.CallFunction("POSITION", args) => ir.CallFunction("LOCATE", args)
      case ir.CallFunction("REGEXP_LIKE", args) => ir.RLike(args.head, args(1))
      case ir.CallFunction("REGEXP_SUBSTR", args) => regexpExtract(args)
      case ir.CallFunction("SPLIT_PART", args) => splitPart(args)
      case ir.CallFunction("SQUARE", args) => ir.Pow(args.head, ir.Literal(2))
      case ir.CallFunction("STRTOK", args) => strtok(args)
      case ir.CallFunction("STRTOK_TO_ARRAY", args) => split(args)
      case ir.CallFunction("SYSDATE", _) => ir.CurrentTimestamp()
      case ir.CallFunction("TIMESTAMPADD", args) => timestampAdd(args)
      case ir.CallFunction("TIMESTAMP_FROM_PARTS", args) => makeTimestamp(args)
      case ir.CallFunction("TO_DATE", args) => toDate(args)
      case ir.CallFunction("TO_DOUBLE", args) => ir.CallFunction("DOUBLE", args)
      case ir.CallFunction("TO_NUMBER", args) => toNumber(args)
      case ir.CallFunction("TO_OBJECT", args) => ir.StructsToJson(args.head, args(1))
      case ir.CallFunction("TO_VARCHAR", args) => ir.CallFunction("TO_CHAR", args)
      case ir.CallFunction("TO_TIMESTAMP", args) => toTimestamp(args)
      case ir.CallFunction("TRY_TO_DATE", args) => tryToDate(args)
      case ir.CallFunction("TRY_TO_NUMBER", args) => tryToNumber(args)
      case ir.CallFunction("TRY_BASE64_DECODE_STRING", args) => ir.UnBase64(args.head)
      case ir.CallFunction("TRY_BASE64_DECODE_BINARY", args) => ir.UnBase64(args.head)
      case x => super.convert(x)
    }
  }

  private def getJsonObject(args: Seq[ir.Expression]): ir.Expression = {
    val translatedFmt = args match {
      case Seq(_, StringLiteral(path)) => ir.Literal("$." + path)
      case Seq(_, id: ir.Id) => ir.Concat(Seq(ir.Literal("$."), id))

      // As well as CallFunctions, we can receive concrete functions, which are already resolved,
      // and don't need to be converted
      case x: ir.Fn => x

      case a => throw TranspileException(s"Unsupported arguments to GET_JSON_OBJECT: ${a.mkString("(", ", ", ")")}")
    }
    ir.GetJsonObject(args.head, translatedFmt)
  }

  private def split(args: Seq[ir.Expression]): ir.Expression = {

    val delim = args(1) match {
      case StringLiteral(d) => ir.Literal(s"[$d]")
      case e => ir.Concat(Seq(ir.Literal("["), e, ir.Literal("]")))
    }
    ir.StringSplit(args.head, delim, None)
  }

  private def toNumber(args: Seq[ir.Expression]): ir.Expression = {
    val getArg: Int => Option[ir.Expression] = args.lift
    if (args.size < 2) {
      throw TranspileException("not enough arguments to TO_NUMBER")
    } else if (args.size == 2) {
      ir.ToNumber(args.head, args(1))
    } else {
      val fmt = getArg(1).collect { case f @ StringLiteral(_) =>
        f
      }
      val precPos = fmt.fold(1)(_ => 2)
      val prec = getArg(precPos).collect { case IntLiteral(p) =>
        p
      }
      val scale = getArg(precPos + 1).collect { case IntLiteral(s) =>
        s
      }
      val castedExpr = fmt.fold(args.head)(_ => ir.ToNumber(args.head, args(1)))
      ir.Cast(castedExpr, ir.DecimalType(prec, scale))
    }
  }

  private def tryToNumber(args: Seq[ir.Expression]): ir.Expression = {
    val getArg: Int => Option[ir.Expression] = args.lift
    if (args.size == 1) {
      ir.Cast(args.head, ir.DecimalType(Some(38), Some(0)))
    } else {
      val fmt = getArg(1).collect { case f @ StringLiteral(_) =>
        f
      }
      val precPos = fmt.fold(1)(_ => 2)
      val prec = getArg(precPos)
        .collect { case IntLiteral(p) =>
          p
        }
        .orElse(Some(38))
      val scale = getArg(precPos + 1)
        .collect { case IntLiteral(s) =>
          s
        }
        .orElse(Some(0))
      val castedExpr = fmt.fold(args.head)(f => ir.TryToNumber(args.head, f))
      ir.Cast(castedExpr, ir.DecimalType(prec, scale))
    }
  }

  private def strtok(args: Seq[ir.Expression]): ir.Expression = {
    if (args.size == 1) {
      splitPart(Seq(args.head, ir.Literal(" "), ir.Literal(1)))
    } else if (args.size == 2) {
      splitPart(Seq(args.head, args(1), ir.Literal(1)))
    } else splitPart(args)
  }

  /**
   * Snowflake and DB SQL differ in the `partNumber` argument: in Snowflake, a value of 0 is interpreted as "get the
   * first part" while it raises an error in DB SQL.
   */
  private def splitPart(args: Seq[ir.Expression]): ir.Expression = args match {
    case Seq(str, delim, IntLiteral(0)) => ir.StringSplitPart(str, delim, ir.Literal(1))
    case Seq(str, delim, IntLiteral(p)) => ir.StringSplitPart(str, delim, ir.Literal(p))
    case Seq(str, delim, expr) =>
      ir.StringSplitPart(str, delim, ir.If(ir.Equals(expr, ir.Literal(0)), ir.Literal(1), expr))
    case other =>
      throw TranspileException(
        s"Wrong number of arguments to SPLIT_PART, expected 3, got ${other.size}: ${other.mkString(", ")}")
  }

  private def regexpExtract(args: Seq[ir.Expression]): ir.Expression = {
    if (args.size == 2) {
      ir.RegExpExtract(args.head, args(1), ir.Literal(1))
    } else if (args.size == 3) {
      ir.RegExpExtract(args.head, args(1), args(2))
    } else {
      throw TranspileException(s"WRONG number of arguments to REGEXP_EXTRACT, expected 2 or 3, got ${args.size}")
    }
  }

  private def translateDateOrTimePart(input: ir.Expression): String = input match {
    case ir.Id(part, _) if SnowflakeTimeUnits.findDateOrTimePart(part).nonEmpty =>
      SnowflakeTimeUnits.findDateOrTimePart(part).get
    case StringLiteral(part) if SnowflakeTimeUnits.findDateOrTimePart(part).nonEmpty =>
      SnowflakeTimeUnits.findDateOrTimePart(part).get
    case x => throw TranspileException(s"unknown date part $x")
  }

  private def dateDiff(args: Seq[ir.Expression]): ir.Expression = {
    val datePart = translateDateOrTimePart(args.head)
    ir.TimestampDiff(datePart, args(1), args(2))
  }

  private def tryToDate(args: Seq[ir.Expression]): ir.Expression = {
    val format = if (args.size < 2) {
      ir.Literal("yyyy-MM-dd")
    } else {
      args(1)
    }
    ir.CallFunction("DATE", Seq(ir.TryToTimestamp(args.head, format)))
  }

  private def dateAdd(args: Seq[ir.Expression]): ir.Expression = {
    if (args.size == 2) {
      ir.DateAdd(args.head, args(1))
    } else if (args.size == 3) {
      timestampAdd(args)
    } else {
      throw TranspileException(s"wrong number of arguments to DATEADD, expected 2 or 3, got ${args.size}")
    }
  }

  private def timestampAdd(args: Seq[ir.Expression]): ir.Expression = {
    val dateOrTimePart = translateDateOrTimePart(args.head)
    ir.TimestampAdd(dateOrTimePart, args(1), args(2))
  }

  private def datePart(args: Seq[ir.Expression]): ir.Expression = {
    val part = translateDateOrTimePart(args.head)
    ir.Extract(ir.Id(part), args(1))
  }

  private def dateTrunc(args: Seq[ir.Expression]): ir.Expression = {
    val part = translateDateOrTimePart(args.head)
    ir.TruncTimestamp(ir.Literal(part.toUpperCase()), args(1))
  }

  private def makeTimestamp(args: Seq[ir.Expression]): ir.Expression = {
    if (args.size == 2) {
      // Snowflake's TIMESTAMP_FROM_PARTS can be invoked with only two arguments
      // that, in this case, represent a date and a time. In such case, we need to
      // extract the components of both date and time and feed them to MAKE_TIMESTAMP
      // accordingly
      val year = ir.DatePart(ir.Id("year"), args.head)
      val month = ir.DatePart(ir.Id("month"), args.head)
      val day = ir.DatePart(ir.Id("day"), args.head)
      val hour = ir.Hour(args(1))
      val minute = ir.Minute(args(1))
      val second = ir.Second(args(1))
      ir.MakeTimestamp(year, month, day, hour, minute, second, None)
    } else if (args.size == 6) {
      ir.MakeTimestamp(args.head, args(1), args(2), args(3), args(4), args(5), None)
    } else if (args.size == 7) {
      // When call with individual parts (as opposed to the two-arguments scenario above)
      // Snowflake allows for two additional optional parameters: an amount of nanoseconds
      // and/or a timezone. So when we get 7 arguments, we need to inspect the last one to
      // determine whether it's an amount of nanoseconds (ie. a number) or a timezone reference
      // (ie. a string)
      args(6) match {
        case IntLiteral(_) =>
          // We ignore that last parameter as DB SQL doesn't handle nanoseconds
          // TODO warn the user about this
          ir.MakeTimestamp(args.head, args(1), args(2), args(3), args(4), args(5), None)
        case timezone @ StringLiteral(_) =>
          ir.MakeTimestamp(args.head, args(1), args(2), args(3), args(4), args(5), Some(timezone))
        case _ => throw TranspileException("could not interpret the last argument to TIMESTAMP_FROM_PARTS")
      }
    } else if (args.size == 8) {
      // Here the situation is simpler, we just ignore the 7th argument (nanoseconds)
      ir.MakeTimestamp(args.head, args(1), args(2), args(3), args(4), args(5), Some(args(7)))
    } else {
      throw TranspileException(
        s"wrong number of arguments to TIMESTAMP_FROM_PART, expected either 2, 6, 7 or 8, got ${args.size} ")
    }
  }

  private def toTimestamp(args: Seq[ir.Expression]): ir.Expression = {
    if (args.size == 1) {
      ir.Cast(args.head, ir.TimestampType)
    } else if (args.size == 2) {
      ir.ParseToTimestamp(args.head, args(1))
    } else {
      throw TranspileException(s"wrong number of arguments to TO_TIMESTAMP, expected 1 or 2, got ${args.size}")
    }
  }

  private def dayname(args: Seq[ir.Expression]): ir.Expression = {
    ir.DateFormatClass(args.head, ir.Literal("E"))
  }

  private def toDate(args: Seq[ir.Expression]): ir.Expression = {
    if (args.size == 1) {
      ir.Cast(args.head, ir.DateType)
    } else if (args.size == 2) {
      ir.ParseToDate(args.head, Some(args(1)))
    } else {
      throw TranspileException(s"wrong number of arguments to TO_DATE, expected 1 or 2, got ${args.size}")
    }
  }
}
