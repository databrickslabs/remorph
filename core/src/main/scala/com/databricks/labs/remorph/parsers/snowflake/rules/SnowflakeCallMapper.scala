package com.databricks.labs.remorph.parsers.snowflake.rules

import com.databricks.labs.remorph.parsers.{intermediate => ir}
import com.databricks.labs.remorph.transpilers.TranspileException

import java.time.format.DateTimeFormatter
import scala.util.Try

class SnowflakeCallMapper extends ir.CallMapper with ir.IRHelpers {
  private val zeroLiteral: ir.Literal = ir.IntLiteral(0)
  private val oneLiteral: ir.Literal = ir.IntLiteral(1)

  override def convert(call: ir.Fn): ir.Expression = {
    withNormalizedName(call) match {
      // keep all the names in alphabetical order
      case ir.CallFunction("ARRAY_CAT", args) => ir.Concat(args)
      case ir.CallFunction("ARRAY_CONSTRUCT", args) => ir.CreateArray(args)
      case ir.CallFunction("ARRAY_CONSTRUCT_COMPACT", args) =>
        ir.ArrayExcept(ir.CreateArray(args), ir.CreateArray(Seq(ir.Literal.Null)))
      case ir.CallFunction("ARRAY_CONTAINS", args) => ir.ArrayContains(args(1), args.head)
      case ir.CallFunction("ARRAY_INTERSECTION", args) => ir.ArrayIntersect(args.head, args(1))
      case ir.CallFunction("ARRAY_SIZE", args) => ir.Size(args.head)
      case ir.CallFunction("ARRAY_SLICE", args) =>
        // @see https://docs.snowflake.com/en/sql-reference/functions/array_slice
        // @see https://docs.databricks.com/en/sql/language-manual/functions/slice.html
        // TODO: optimize constants: ir.Add(ir.Literal(2), ir.Literal(2)) => ir.Literal(4)
        ir.Slice(args.head, zeroIndexedToOneIndexed(args(1)), args.lift(2).getOrElse(oneLiteral))
      case ir.CallFunction("ARRAY_TO_STRING", args) => ir.ArrayJoin(args.head, args(1), None)
      case ir.CallFunction("BASE64_DECODE_STRING", args) => ir.UnBase64(args.head)
      case ir.CallFunction("BASE64_DECODE_BINARY", args) => ir.UnBase64(args.head)
      case ir.CallFunction("BASE64_ENCODE", args) => ir.Base64(args.head)
      case ir.CallFunction("BITOR_AGG", args) => ir.BitOrAgg(args.head)
      case ir.CallFunction("BOOLAND_AGG", args) => ir.BoolAnd(args.head)
      case ir.CallFunction("CURRENT_TIMESTAMP", _) => ir.CurrentTimestamp()
      case ir.CallFunction("DATEADD", args) => dateAdd(args)
      case ir.CallFunction("DATEDIFF", args) => dateDiff(args)
      case ir.CallFunction("DATE_FROM_PARTS", args) => ir.MakeDate(args.head, args(1), args(2))
      case ir.CallFunction("DATE_PART", args) => datePart(args)
      case ir.CallFunction("DATE_TRUNC", args) => dateTrunc(args)
      case ir.CallFunction("DAYNAME", args) => dayname(args)
      case ir.CallFunction("DECODE", args) => decode(args)
      case ir.CallFunction("DIV0", args) => div0(args)
      case ir.CallFunction("DIV0NULL", args) => div0null(args)
      case ir.CallFunction("EDITDISTANCE", args) => ir.Levenshtein(args.head, args(1), args.lift(2))
      case ir.CallFunction("FLATTEN", args) =>
        // @see https://docs.snowflake.com/en/sql-reference/functions/flatten
        ir.Explode(args.head)
      case ir.CallFunction("IFNULL", args) => ir.Coalesce(args)
      case ir.CallFunction("IS_INTEGER", args) => isInteger(args)
      case ir.CallFunction("JSON_EXTRACT_PATH_TEXT", args) => getJsonObject(args)
      case ir.CallFunction("LEN", args) => ir.Length(args.head)
      case ir.CallFunction("LISTAGG", args) =>
        ir.ArrayJoin(ir.CollectList(args.head, None), args.lift(1).getOrElse(ir.Literal("")), None)
      case ir.CallFunction("MONTHNAME", args) => ir.DateFormatClass(args.head, ir.Literal("MMM"))
      case ir.CallFunction("NULLIFZERO", args) => nullIfZero(args.head)
      case ir.CallFunction("OBJECT_KEYS", args) => ir.JsonObjectKeys(args.head)
      case ir.CallFunction("OBJECT_CONSTRUCT", args) => objectConstruct(args)
      case ir.CallFunction("PARSE_JSON", args) => fromJson(args)
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
      case ir.CallFunction("TO_ARRAY", args) => toArray(args)
      case ir.CallFunction("TO_BOOLEAN", args) => toBoolean(args)
      case ir.CallFunction("TO_DATE", args) => toDate(args)
      case ir.CallFunction("TO_DOUBLE", args) => ir.CallFunction("DOUBLE", args)
      case ir.CallFunction("TO_NUMBER", args) => toNumber(args)
      case ir.CallFunction("TO_OBJECT", args) => ir.StructsToJson(args.head, args.lift(1))
      case ir.CallFunction("TO_VARCHAR", args) => ir.CallFunction("TO_CHAR", args)
      case ir.CallFunction("TO_VARIANT", args) => ir.StructsToJson(args.head, None)
      case ir.CallFunction("TO_TIME", args) => toTime(args)
      case ir.CallFunction("TO_TIMESTAMP", args) => toTimestamp(args)
      case ir.CallFunction("TRY_BASE64_DECODE_STRING", args) => ir.UnBase64(args.head)
      case ir.CallFunction("TRY_BASE64_DECODE_BINARY", args) => ir.UnBase64(args.head)
      case ir.CallFunction("TRY_PARSE_JSON", args) => fromJson(args)
      case ir.CallFunction("TRY_TO_BOOLEAN", args) => tryToBoolean(args)
      case ir.CallFunction("TRY_TO_DATE", args) => tryToDate(args)
      case ir.CallFunction("TRY_TO_NUMBER", args) => tryToNumber(args)
      case ir.CallFunction("UUID_STRING", _) => ir.Uuid()
      case ir.CallFunction("ZEROIFNULL", args) => ir.If(ir.IsNull(args.head), ir.Literal(0), args.head)
      case x => super.convert(x)
    }
  }

  private def objectConstruct(args: Seq[ir.Expression]): ir.Expression = args match {
    case Seq(s @ ir.Star(_)) => ir.StructExpr(Seq(s))
    case pairs: Seq[ir.Expression] =>
      ir.StructExpr(
        pairs
          .sliding(2, 2)
          .collect {
            case Seq(ir.StringLiteral(key), v) => ir.Alias(v, ir.Id(key))
            case Seq(a, b) => throw TranspileException(s"Unsupported arguments to OBJECT_CONSTRUCT: $a, $b")
            case Seq(a) => throw TranspileException(s"Unsupported argument to OBJECT_CONSTRUCT: $a")
          }
          .toList)
  }

  private def nullIfZero(expr: ir.Expression): ir.Expression =
    ir.If(ir.Equals(expr, zeroLiteral), ir.Literal.Null, expr)

  private def div0null(args: Seq[ir.Expression]): ir.Expression = args match {
    case Seq(left, right) =>
      ir.If(ir.Or(ir.Equals(right, zeroLiteral), ir.IsNull(right)), zeroLiteral, ir.Divide(left, right))
  }

  private def div0(args: Seq[ir.Expression]): ir.Expression = args match {
    case Seq(left, right) =>
      ir.If(ir.Equals(right, zeroLiteral), zeroLiteral, ir.Divide(left, right))
  }

  private def zeroIndexedToOneIndexed(expr: ir.Expression): ir.Expression = expr match {
    case ir.IntLiteral(num) => ir.IntLiteral(num + 1)
    case neg: ir.UMinus => neg
    case x => ir.If(ir.GreaterThanOrEqual(x, zeroLiteral), ir.Add(x, oneLiteral), x)
  }

  private def getJsonObject(args: Seq[ir.Expression]): ir.Expression = {
    val translatedFmt = args match {
      case Seq(_, ir.StringLiteral(path)) => ir.Literal("$." + path)
      case Seq(_, id: ir.Id) => ir.Concat(Seq(ir.Literal("$."), id))

      // As well as CallFunctions, we can receive concrete functions, which are already resolved,
      // and don't need to be converted
      case x: ir.Fn => x

      case a => throw TranspileException(s"Unsupported arguments to GET_JSON_OBJECT: ${a.mkString("(", ", ", ")")}")
    }
    ir.GetJsonObject(args.head, translatedFmt)
  }

  private def split(args: Seq[ir.Expression]): ir.Expression = {
    val delim = args.lift(1) match {
      case None => ir.StringLiteral("[ ]")
      case Some(ir.StringLiteral(d)) => ir.StringLiteral(s"[$d]")
      case Some(e) => ir.Concat(Seq(ir.StringLiteral("["), e, ir.StringLiteral("]")))
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
      val fmt = getArg(1).collect { case f @ ir.StringLiteral(_) =>
        f
      }
      val precPos = fmt.fold(1)(_ => 2)
      val prec = getArg(precPos).collect { case ir.IntLiteral(p) =>
        p
      }
      val scale = getArg(precPos + 1).collect { case ir.IntLiteral(s) =>
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
      val fmt = getArg(1).collect { case f @ ir.StringLiteral(_) =>
        f
      }
      val precPos = fmt.fold(1)(_ => 2)
      val prec = getArg(precPos)
        .collect { case ir.IntLiteral(p) =>
          p
        }
        .orElse(Some(38))
      val scale = getArg(precPos + 1)
        .collect { case ir.IntLiteral(s) =>
          s
        }
        .orElse(Some(0))
      val castedExpr = fmt.fold(args.head)(f => ir.TryToNumber(args.head, f))
      ir.Cast(castedExpr, ir.DecimalType(prec, scale))
    }
  }

  private def strtok(args: Seq[ir.Expression]): ir.Expression = {
    if (args.size == 1) {
      splitPart(Seq(args.head, ir.Literal(" "), oneLiteral))
    } else if (args.size == 2) {
      splitPart(Seq(args.head, args(1), oneLiteral))
    } else splitPart(args)
  }

  /**
   * Snowflake and DB SQL differ in the `partNumber` argument: in Snowflake, a value of 0 is interpreted as "get the
   * first part" while it raises an error in DB SQL.
   */
  private def splitPart(args: Seq[ir.Expression]): ir.Expression = args match {
    case Seq(str, delim, ir.IntLiteral(0)) => ir.StringSplitPart(str, delim, oneLiteral)
    case Seq(str, delim, ir.IntLiteral(p)) => ir.StringSplitPart(str, delim, ir.Literal(p))
    case Seq(str, delim, expr) =>
      ir.StringSplitPart(str, delim, ir.If(ir.Equals(expr, zeroLiteral), oneLiteral, expr))
    case other =>
      throw TranspileException(
        s"Wrong number of arguments to SPLIT_PART, expected 3, got ${other.size}: ${other.mkString(", ")}")
  }

  private def regexpExtract(args: Seq[ir.Expression]): ir.Expression = {
    if (args.size == 2) {
      ir.RegExpExtract(args.head, args(1), oneLiteral)
    } else if (args.size == 3) {
      ir.RegExpExtract(args.head, args(1), args(2))
    } else {
      throw TranspileException(s"WRONG number of arguments to REGEXP_EXTRACT, expected 2 or 3, got ${args.size}")
    }
  }

  private def dateDiff(args: Seq[ir.Expression]): ir.Expression = {
    val datePart = SnowflakeTimeUnits.translateDateOrTimePart(args.head)
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
    val dateOrTimePart = SnowflakeTimeUnits.translateDateOrTimePart(args.head)
    ir.TimestampAdd(dateOrTimePart, args(1), args(2))
  }

  private def datePart(args: Seq[ir.Expression]): ir.Expression = {
    val part = SnowflakeTimeUnits.translateDateOrTimePart(args.head)
    ir.Extract(ir.Id(part), args(1))
  }

  private def dateTrunc(args: Seq[ir.Expression]): ir.Expression = {
    val part = SnowflakeTimeUnits.translateDateOrTimePart(args.head)
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
        case ir.IntLiteral(_) =>
          // We ignore that last parameter as DB SQL doesn't handle nanoseconds
          // TODO warn the user about this
          ir.MakeTimestamp(args.head, args(1), args(2), args(3), args(4), args(5), None)
        case timezone @ ir.StringLiteral(_) =>
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

  private def toTime(args: Seq[ir.Expression]): ir.Expression = args match {
    case Seq(a) => ir.ParseToTimestamp(a, inferTimeFormat(a))
    case Seq(a, b) => ir.ParseToTimestamp(a, b)
    case _ => throw TranspileException(s"wrong number of arguments to TO_TIMESTAMP, expected 1 or 2, got ${args.size}")
  }

  private val timestampFormats = Seq("yyyy-MM-dd HH:mm:ss")

  private def inferTimeFormat(expression: ir.Expression): ir.Expression = expression match {
    case ir.StringLiteral(timeStr) =>
      ir.StringLiteral(timestampFormats.find(fmt => Try(DateTimeFormatter.ofPattern(fmt).parse(timeStr)).isSuccess).get)
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

  private def isInteger(args: Seq[ir.Expression]): ir.Expression = {
    ir.Case(
      None,
      Seq(
        ir.WhenBranch(ir.IsNull(args.head), ir.Literal.Null),
        ir.WhenBranch(
          ir.And(ir.RLike(args.head, ir.Literal("^-?[0-9]+$")), ir.IsNotNull(ir.TryCast(args.head, ir.IntegerType))),
          ir.Literal(true))),
      Some(ir.Literal(false)))
  }

  private def toArray(args: Seq[ir.Expression]): ir.Expression = {
    ir.If(ir.IsNull(args.head), ir.Literal.Null, ir.CreateArray(Seq(args.head)))
  }

  private def toBoolean(args: Seq[ir.Expression]): ir.Expression = {
    toBooleanLike(args.head, ir.RaiseError(ir.Literal("Invalid parameter type for TO_BOOLEAN")))
  }

  private def tryToBoolean(args: Seq[ir.Expression]): ir.Expression = {
    toBooleanLike(args.head, ir.Literal.Null)
  }

  private def toBooleanLike(arg: ir.Expression, otherwise: ir.Expression): ir.Expression = {
    val castArgAsDouble = ir.Cast(arg, ir.DoubleType)
    ir.Case(
      None,
      Seq(
        ir.WhenBranch(ir.IsNull(arg), ir.Literal.Null),
        ir.WhenBranch(ir.Equals(ir.TypeOf(arg), ir.Literal("boolean")), ir.CallFunction("BOOLEAN", Seq(arg))),
        ir.WhenBranch(
          ir.Equals(ir.TypeOf(arg), ir.Literal("string")),
          ir.Case(
            None,
            Seq(
              ir.WhenBranch(
                ir.In(
                  ir.Lower(arg),
                  Seq(
                    ir.Literal("true"),
                    ir.Literal("t"),
                    ir.Literal("yes"),
                    ir.Literal("y"),
                    ir.Literal("on"),
                    ir.Literal("1"))),
                ir.Literal(true)),
              ir.WhenBranch(
                ir.In(
                  ir.Lower(arg),
                  Seq(
                    ir.Literal("false"),
                    ir.Literal("f"),
                    ir.Literal("no"),
                    ir.Literal("n"),
                    ir.Literal("off"),
                    ir.Literal("0"))),
                ir.Literal(false))),
            Some(ir.RaiseError(ir.Literal(s"Boolean value of x is not recognized by TO_BOOLEAN"))))),
        ir.WhenBranch(
          ir.IsNotNull(ir.TryCast(arg, ir.DoubleType)),
          ir.Case(
            None,
            Seq(
              ir.WhenBranch(
                ir.Or(
                  ir.IsNaN(castArgAsDouble),
                  ir.Equals(castArgAsDouble, ir.CallFunction("DOUBLE", Seq(ir.Literal("infinity"))))),
                ir.RaiseError(ir.Literal("Invalid parameter type for TO_BOOLEAN")))),
            Some(ir.NotEquals(castArgAsDouble, ir.DoubleLiteral(0.0d)))))),
      Some(otherwise))
  }

  private def decode(args: Seq[ir.Expression]): ir.Expression = {
    if (args.size >= 3) {
      val expr = args.head
      val groupedArgs = args.tail.sliding(2, 2).toList
      ir.Case(
        None,
        groupedArgs.takeWhile(_.size == 2).map(l => makeWhenBranch(expr, l.head, l.last)),
        groupedArgs.find(_.size == 1).map(_.head))
    } else {
      throw TranspileException(s"wrong number of arguments to DECODE, expected at least 3, got ${args.size}")
    }
  }

  private def makeWhenBranch(expr: ir.Expression, cond: ir.Expression, out: ir.Expression): ir.WhenBranch = {
    cond match {
      case ir.Literal.Null => ir.WhenBranch(ir.IsNull(expr), out)
      case any => ir.WhenBranch(ir.Equals(expr, any), out)
    }
  }

  private def fromJson(args: Seq[ir.Expression]): ir.Expression = {
    val schema = args.lift(1) match {
      case None => ir.SchemaReference(args.head)
      case Some(e) => e
    }
    ir.JsonToStructs(args.head, schema, None)
  }
}
