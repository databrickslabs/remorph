package com.databricks.labs.remorph.parsers.snowflake.rules

import com.databricks.labs.remorph.intermediate.UnresolvedNamedLambdaVariable
import com.databricks.labs.remorph.{PartialResult, Transformation, TransformationConstructors, intermediate => ir}

import java.time.format.DateTimeFormatter
import scala.util.Try

class SnowflakeCallMapper extends ir.CallMapper with ir.IRHelpers with TransformationConstructors {
  private[this] val zeroLiteral: ir.Literal = ir.IntLiteral(0)
  private[this] val oneLiteral: ir.Literal = ir.IntLiteral(1)

  override def convert(call: ir.Fn): Transformation[ir.Expression] = {
    withNormalizedName(call) match {
      // keep all the names in alphabetical order
      case ir.CallFunction("ARRAY_CAT", args) => ok(ir.Concat(args))
      case ir.CallFunction("ARRAY_CONSTRUCT", args) => ok(ir.CreateArray(args))
      case ir.CallFunction("ARRAY_CONSTRUCT_COMPACT", args) =>
        ok(ir.ArrayExcept(ir.CreateArray(args), ir.CreateArray(Seq(ir.Literal.Null))))
      case ir.CallFunction("ARRAY_CONTAINS", args) => ok(ir.ArrayContains(args(1), args.head))
      case ir.CallFunction("ARRAY_FLATTEN", args) => ok(ir.Flatten(args.head))
      case ir.CallFunction("ARRAY_INTERSECTION", args) => ok(ir.ArrayIntersect(args.head, args(1)))
      case ir.CallFunction("ARRAY_SIZE", args) => ok(ir.Size(args.head))
      case ir.CallFunction("ARRAY_SLICE", args) =>
        // @see https://docs.snowflake.com/en/sql-reference/functions/array_slice
        // @see https://docs.databricks.com/en/sql/language-manual/functions/slice.html
        // TODO: optimize constants: ir.Add(ir.Literal(2), ir.Literal(2)) => ir.Literal(4)
        ok(ir.Slice(args.head, zeroIndexedToOneIndexed(args(1)), args.lift(2).getOrElse(oneLiteral)))
      case ir.CallFunction("ARRAY_SORT", args) => arraySort(args)
      case ir.CallFunction("ARRAY_TO_STRING", args) => ok(ir.ArrayJoin(args.head, args(1), None))
      case ir.CallFunction("BASE64_DECODE_STRING", args) => ok(ir.UnBase64(args.head))
      case ir.CallFunction("BASE64_DECODE_BINARY", args) => ok(ir.UnBase64(args.head))
      case ir.CallFunction("BASE64_ENCODE", args) => ok(ir.Base64(args.head))
      case ir.CallFunction("BITOR_AGG", args) => ok(ir.BitOrAgg(args.head))
      case ir.CallFunction("BOOLAND_AGG", args) => ok(ir.BoolAnd(args.head))
      case da @ ir.CallFunction("DATEADD", args) => dateAdd(da, args)
      case ir.CallFunction("DATEDIFF", args) => dateDiff(args)
      case ir.CallFunction("DATE_FROM_PARTS", args) => ok(ir.MakeDate(args.head, args(1), args(2)))
      case ir.CallFunction("DATE_PART", args) => datePart(args)
      case ir.CallFunction("DATE_TRUNC", args) => dateTrunc(args)
      case ir.CallFunction("DAYNAME", args) => ok(dayname(args))
      case d @ ir.CallFunction("DECODE", args) => decode(d, args)
      case ir.CallFunction("DIV0", args) => ok(div0(args))
      case ir.CallFunction("DIV0NULL", args) => ok(div0null(args))
      case ir.CallFunction("EDITDISTANCE", args) => ok(ir.Levenshtein(args.head, args(1), args.lift(2)))
      case ir.CallFunction("FIRST_VALUE", args) => ok(ir.First(args.head, args.lift(1)))
      case ir.CallFunction("FLATTEN", args) =>
        // @see https://docs.snowflake.com/en/sql-reference/functions/flatten
        ok(ir.Explode(args.head))
      case ir.CallFunction("IFNULL", args) => ok(ir.Coalesce(args))
      case ir.CallFunction("IS_INTEGER", args) => ok(isInteger(args))
      case jept @ ir.CallFunction("JSON_EXTRACT_PATH_TEXT", args) => getJsonObject(jept, args)
      case ir.CallFunction("LAST_DAY", args) => parseLastDay(args)
      case ir.CallFunction("LAST_VALUE", args) => ok(ir.Last(args.head, args.lift(1)))
      case ir.CallFunction("LEN", args) => ok(ir.Length(args.head))
      case ir.CallFunction("LISTAGG", args) =>
        ok(ir.ArrayJoin(ir.CollectList(args.head, None), args.lift(1).getOrElse(ir.Literal("")), None))
      case ir.CallFunction("MONTHNAME", args) => ok(ir.DateFormatClass(args.head, ir.Literal("MMM")))
      case ir.CallFunction("MONTHS_BETWEEN", args) => ok(ir.MonthsBetween(args.head, args(1), ir.Literal.True))
      case ir.CallFunction("NULLIFZERO", args) => ok(nullIfZero(args.head))
      case ir.CallFunction("OBJECT_KEYS", args) => ok(ir.JsonObjectKeys(args.head))
      case ir.CallFunction("OBJECT_CONSTRUCT", args) => objectConstruct(args)
      case ir.CallFunction("PARSE_JSON", args) => ok(ir.ParseJson(args.head))
      case ir.CallFunction("POSITION", args) => ok(ir.CallFunction("LOCATE", args))
      case ir.CallFunction("REGEXP_LIKE", args) => ok(ir.RLike(args.head, args(1)))
      case ir.CallFunction("REGEXP_SUBSTR", args) => ok(regexpExtract(args))
      case ir.CallFunction("SHA2", args) => ok(ir.Sha2(args.head, args.lift(1).getOrElse(ir.Literal(256))))
      case sp @ ir.CallFunction("SPLIT_PART", args) => splitPart(sp, args)
      case ir.CallFunction("SQUARE", args) => ok(ir.Pow(args.head, ir.Literal(2)))
      case st @ ir.CallFunction("STRTOK", args) => strtok(st, args)
      case ir.CallFunction("STRTOK_TO_ARRAY", args) => ok(split(args))
      case ir.CallFunction("SYSDATE", _) => ok(ir.CurrentTimestamp())
      case ir.CallFunction("TIMESTAMPADD", args) => timestampAdd(args)
      case tfp @ ir.CallFunction("TIMESTAMP_FROM_PARTS", args) => makeTimestamp(tfp, args)
      case ir.CallFunction("TO_ARRAY", args) => ok(toArray(args))
      case ir.CallFunction("TO_BOOLEAN", args) => ok(toBoolean(args))
      case td @ ir.CallFunction("TO_DATE", args) => toDate(td, args)
      case ir.CallFunction("TO_DOUBLE", args) => ok(ir.CallFunction("DOUBLE", args))
      case ir.CallFunction("TO_NUMBER", args) => ok(toNumber(args))
      case ir.CallFunction("TO_OBJECT", args) => ok(ir.StructsToJson(args.head, args.lift(1)))
      case ir.CallFunction("TO_VARCHAR", args) => ok(ir.CallFunction("TO_CHAR", args))
      case ir.CallFunction("TO_VARIANT", args) => ok(ir.StructsToJson(args.head, None))
      case tt @ ir.CallFunction("TO_TIME", args) => toTime(tt, args)
      case tt @ ir.CallFunction("TO_TIMESTAMP", args) => toTimestamp(tt, args)
      case ir.CallFunction("TRY_BASE64_DECODE_STRING", args) => ok(ir.UnBase64(args.head))
      case ir.CallFunction("TRY_BASE64_DECODE_BINARY", args) => ok(ir.UnBase64(args.head))
      case ir.CallFunction("TRY_PARSE_JSON", args) => ok(ir.ParseJson(args.head))
      case ir.CallFunction("TRY_TO_BOOLEAN", args) => ok(tryToBoolean(args))
      case ir.CallFunction("TRY_TO_DATE", args) => ok(tryToDate(args))
      case ir.CallFunction("TRY_TO_NUMBER", args) => ok(tryToNumber(args))
      case ir.CallFunction("UUID_STRING", _) => ok(ir.Uuid())
      case ir.CallFunction("ZEROIFNULL", args) => ok(ir.If(ir.IsNull(args.head), ir.Literal(0), args.head))
      case x => super.convert(x)
    }
  }

  private def objectConstruct(args: Seq[ir.Expression]): Transformation[ir.Expression] = args match {
    case Seq(s @ ir.Star(_)) => ok(ir.StructExpr(Seq(s)))
    case pairs: Seq[ir.Expression] =>
      val (validPairs, invalidPairs) = pairs
        .sliding(2, 2)
        .partition {
          case Seq(ir.StringLiteral(_), _) => true
          case _ => false
        }
      val expr = ir.StructExpr(validPairs.map { case Seq(ir.StringLiteral(key), v) => ir.Alias(v, ir.Id(key)) }.toSeq)
      if (invalidPairs.isEmpty) ok(expr)
      else lift(PartialResult(expr, ir.UnsupportedArguments("OBJECT_CONSTRUCT", args)))
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

  private def getJsonObject(functionCall: ir.Expression, args: Seq[ir.Expression]): Transformation[ir.Expression] = {
    (args match {
      case Seq(_, ir.StringLiteral(path)) => ok(ir.Literal("$." + path))
      case Seq(_, id: ir.Id) => ok(ir.Concat(Seq(ir.Literal("$."), id)))

      // As well as CallFunctions, we can receive concrete functions, which are already resolved,
      // and don't need to be converted
      case x: ir.Fn => ok(x)

      case a => lift(PartialResult(functionCall, ir.UnsupportedArguments("GET_JSON_OBJECT", a)))
    }).map { translatedFmt =>
      ir.GetJsonObject(args.head, translatedFmt)
    }
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
      ir.Cast(args.head, ir.DecimalType(38, 0))
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

  private def strtok(functionCall: ir.Expression, args: Seq[ir.Expression]): Transformation[ir.Expression] = {
    if (args.size == 1) {
      splitPart(functionCall, Seq(args.head, ir.Literal(" "), oneLiteral))
    } else if (args.size == 2) {
      splitPart(functionCall, Seq(args.head, args(1), oneLiteral))
    } else splitPart(functionCall, args)
  }

  /**
   * Snowflake and DB SQL differ in the `partNumber` argument: in Snowflake, a value of 0 is interpreted as "get the
   * first part" while it raises an error in DB SQL.
   */
  private def splitPart(functionCall: ir.Expression, args: Seq[ir.Expression]): Transformation[ir.Expression] =
    args match {
      case Seq(str, delim, ir.IntLiteral(0)) => ok(ir.StringSplitPart(str, delim, oneLiteral))
      case Seq(str, delim, ir.IntLiteral(p)) => ok(ir.StringSplitPart(str, delim, ir.Literal(p)))
      case Seq(str, delim, expr) =>
        ok(ir.StringSplitPart(str, delim, ir.If(ir.Equals(expr, zeroLiteral), oneLiteral, expr)))
      case other =>
        lift(PartialResult(functionCall, ir.WrongNumberOfArguments("SPLIT_PART", other.size, "3")))
    }

  // REGEXP_SUBSTR( <subject> , <pattern> [ , <position> [ , <occurrence> [ , <regex_parameters> [ , <group_num> ]]]])
  private def regexpExtract(args: Seq[ir.Expression]): ir.Expression = {
    val subject = if (args.size >= 3) {
      ir.Substring(args.head, args(2))
    } else args.head
    if (args.size <= 3) {
      ir.RegExpExtract(subject, args(1), Some(zeroLiteral))
    } else {
      val occurrence = args(3) match {
        case ir.IntLiteral(o) => ir.Literal(o - 1)
        case o => ir.Subtract(o, oneLiteral)
      }
      val pattern = args.lift(4) match {
        case None => args(1)
        case Some(ir.StringLiteral(regexParams)) => translateLiteralRegexParameters(regexParams, args(1))
        case Some(regexParams) => translateRegexParameters(regexParams, args(1))
      }
      val groupNumber = args.lift(5).orElse(Some(zeroLiteral))
      ir.ArrayAccess(ir.RegExpExtractAll(subject, pattern, groupNumber), occurrence)
    }
  }

  private def translateLiteralRegexParameters(regexParams: String, pattern: ir.Expression): ir.Expression = {
    val filtered = regexParams.foldLeft("") { case (agg, item) =>
      if (item == 'c') agg.filter(_ != 'i')
      else if ("ism".contains(item)) agg + item
      else agg
    }
    pattern match {
      case ir.StringLiteral(pat) => ir.Literal(s"(?$filtered)$pat")
      case e => ir.Concat(Seq(ir.Literal(s"(?$filtered)"), e))
    }
  }

  /**
   * regex_params may be any expression (a literal, but also a column, etc), this changes it to
   *
   * aggregate(
   *   split(regex_params, ''),
   *   cast(array() as array<string>),
   *   (agg, item) ->
   *     case
   *       when item = 'c' then filter(agg, c -> c != 'i')
   *       when item in ('i', 's', 'm') then array_append(agg, item)
   *       else agg
   *     end,
   *   filtered -> '(?' || array_join(array_distinct(filtered), '') || ')'
   * )
   */
  private def translateRegexParameters(regexParameters: ir.Expression, pattern: ir.Expression): ir.Expression = {
    ir.ArrayAggregate(
      ir.StringSplit(regexParameters, ir.Literal(""), None),
      ir.Cast(ir.CreateArray(Seq()), ir.ArrayType(ir.StringType)),
      ir.LambdaFunction(
        ir.Case(
          expression = None,
          branches = Seq(
            ir.WhenBranch(
              ir.Equals(ir.Id("item"), ir.Literal("c")),
              ir.ArrayFilter(
                ir.Id("agg"),
                ir.LambdaFunction(
                  ir.NotEquals(ir.Id("item"), ir.Literal("i")),
                  Seq(ir.UnresolvedNamedLambdaVariable(Seq("item")))))),
            ir.WhenBranch(
              ir.In(ir.Id("item"), Seq(ir.Literal("i"), ir.Literal("s"), ir.Literal("m"))),
              ir.ArrayAppend(ir.Id("agg"), ir.Id("item")))),
          otherwise = Some(ir.Id("agg"))),
        Seq(UnresolvedNamedLambdaVariable(Seq("agg")), UnresolvedNamedLambdaVariable(Seq("item")))),
      ir.LambdaFunction(
        ir.Concat(Seq(ir.Literal("(?"), ir.ArrayJoin(ir.Id("filtered"), ir.Literal("")), ir.Literal(")"), pattern)),
        Seq(UnresolvedNamedLambdaVariable(Seq("filtered")))))
  }

  private def dateDiff(args: Seq[ir.Expression]): Transformation[ir.Expression] = {
    SnowflakeTimeUnits.translateDateOrTimePart(args.head).map { datePart =>
      ir.TimestampDiff(datePart, args(1), args(2))
    }
  }

  private def tryToDate(args: Seq[ir.Expression]): ir.Expression = {
    ir.CallFunction("DATE", Seq(ir.TryToTimestamp(args.head, args.lift(1))))
  }

  private def dateAdd(functionCall: ir.Expression, args: Seq[ir.Expression]): Transformation[ir.Expression] = {
    if (args.size == 2) {
      ok(ir.DateAdd(args.head, args(1)))
    } else if (args.size == 3) {
      timestampAdd(args)
    } else {
      lift(PartialResult(functionCall, ir.WrongNumberOfArguments("DATEADD", args.size, "2 or 3")))
    }
  }

  private def timestampAdd(args: Seq[ir.Expression]): Transformation[ir.Expression] = {
    SnowflakeTimeUnits.translateDateOrTimePart(args.head).map { dateOrTimePart =>
      ir.TimestampAdd(dateOrTimePart, args(1), args(2))
    }
  }

  private def datePart(args: Seq[ir.Expression]): Transformation[ir.Expression] = {
    SnowflakeTimeUnits.translateDateOrTimePart(args.head).map { part =>
      ir.Extract(ir.Id(part), args(1))
    }
  }

  private def dateTrunc(args: Seq[ir.Expression]): Transformation[ir.Expression] = {
    SnowflakeTimeUnits.translateDateOrTimePart(args.head).map { part =>
      ir.TruncTimestamp(ir.Literal(part.toUpperCase()), args(1))
    }
  }

  private def makeTimestamp(functionCall: ir.Expression, args: Seq[ir.Expression]): Transformation[ir.Expression] = {
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
      ok(ir.MakeTimestamp(year, month, day, hour, minute, second, None))
    } else if (args.size == 6) {
      ok(ir.MakeTimestamp(args.head, args(1), args(2), args(3), args(4), args(5), None))
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
          ok(ir.MakeTimestamp(args.head, args(1), args(2), args(3), args(4), args(5), None))
        case timezone @ ir.StringLiteral(_) =>
          ok(ir.MakeTimestamp(args.head, args(1), args(2), args(3), args(4), args(5), Some(timezone)))
        case _ => lift(PartialResult(functionCall, ir.UnsupportedArguments("TIMESTAMP_FROM_PART", Seq(args(6)))))
      }
    } else if (args.size == 8) {
      // Here the situation is simpler, we just ignore the 7th argument (nanoseconds)
      ok(ir.MakeTimestamp(args.head, args(1), args(2), args(3), args(4), args(5), Some(args(7))))
    } else {
      lift(
        PartialResult(functionCall, ir.WrongNumberOfArguments("TIMESTAMP_FROM_PART", args.size, "either 2, 6, 7 or 8")))
    }
  }

  private def toTime(functionCall: ir.Expression, args: Seq[ir.Expression]): Transformation[ir.Expression] = {
    val timeFormat = ir.Literal("HH:mm:ss")
    args match {
      case Seq(a) =>
        ok(
          ir.DateFormatClass(
            inferTemporalFormat(a, unsupportedAutoTimestampFormats ++ unsupportedAutoTimeFormats),
            timeFormat))
      case Seq(a, b) => ok(ir.DateFormatClass(ir.ParseToTimestamp(a, Some(b)), timeFormat))
      case _ => lift(PartialResult(functionCall, ir.WrongNumberOfArguments("TO_TIMESTAMP", args.size, "1 or 2")))
    }
  }

  private def toTimestamp(functionCall: ir.Expression, args: Seq[ir.Expression]): Transformation[ir.Expression] =
    args match {
      case Seq(a) => ok(inferTemporalFormat(a, unsupportedAutoTimestampFormats))
      case Seq(a, lit: ir.Literal) => ok(toTimestampWithLiteralFormat(a, lit))
      case Seq(a, b) => ok(toTimestampWithVariableFormat(a, b))
      case _ => lift(PartialResult(functionCall, ir.WrongNumberOfArguments("TO_TIMESTAMP", args.size, "1 or 2")))
    }

  private def toTimestampWithLiteralFormat(expression: ir.Expression, fmt: ir.Literal): ir.Expression = fmt match {
    case num @ ir.IntLiteral(_) =>
      ir.ParseToTimestamp(expression, Some(ir.Pow(ir.Literal(10), num)))
    case ir.StringLiteral(str) =>
      ir.ParseToTimestamp(
        expression,
        Some(ir.StringLiteral(temporalFormatMapping.foldLeft(str) { case (s, (sf, dbx)) => s.replace(sf, dbx) })))
  }

  private def toTimestampWithVariableFormat(expression: ir.Expression, fmt: ir.Expression): ir.Expression = {
    val translatedFmt = temporalFormatMapping.foldLeft(fmt) { case (s, (sf, dbx)) =>
      ir.StringReplace(s, ir.Literal(sf), ir.Literal(dbx))
    }
    ir.If(
      ir.StartsWith(fmt, ir.Literal("DY")),
      ir.ParseToTimestamp(ir.Substring(expression, ir.Literal(4)), Some(ir.Substring(translatedFmt, ir.Literal(4)))),
      ir.ParseToTimestamp(expression, Some(translatedFmt)))
  }

  // Timestamp formats that can be automatically inferred by Snowflake but not by Databricks
  private[this] val unsupportedAutoTimestampFormats = Seq(
    "yyyy-MM-dd'T'HH:mmXXX",
    "yyyy-MM-dd HH:mmXXX",
    "EEE, dd MMM yyyy HH:mm:ss ZZZ",
    "EEE, dd MMM yyyy HH:mm:ss.SSSSSSSSS ZZZ",
    "EEE, dd MMM yyyy hh:mm:ss a ZZZ",
    "EEE, dd MMM yyyy hh:mm:ss.SSSSSSSSS a ZZZ",
    "EEE, dd MMM yyyy HH:mm:ss",
    "EEE, dd MMM yyyy HH:mm:ss.SSSSSSSSS",
    "EEE, dd MMM yyyy hh:mm:ss a",
    "EEE, dd MMM yyyy hh:mm:ss.SSSSSSSSS a",
    "M/dd/yyyy HH:mm:ss",
    "EEE MMM dd HH:mm:ss ZZZ yyyy")

  private[this] val unsupportedAutoTimeFormats =
    Seq("HH:MM:ss.SSSSSSSSS", "HH:MM:ss", "HH:MM", "hh:MM:ss.SSSSSSSSS a", "hh:MM:ss a", "hh:MM a")

  // In Snowflake, when TO_TIME/TO_TIMESTAMP is called without a specific format, the system is capable of inferring the
  // format from the string being parsed. Databricks has a similar behavior, but the set of formats it's capable of
  // detecting automatically is narrower.
  private def inferTemporalFormat(expression: ir.Expression, unsupportedAutoformats: Seq[String]): ir.Expression =
    expression match {
      // If the expression to be parsed is a Literal, we try the formats supported by Snowflake but not by Databricks
      // and add an explicit parameter with the first that matches, or fallback to no format parameter if none has
      // matched (which could indicate that either the implicit format is one Databricks can automatically infer, or the
      // string to be parsed is malformed).
      case ir.StringLiteral(timeStr) =>
        Try(timeStr.trim.toInt)
          .map(int => ir.ParseToTimestamp(ir.Literal(int)))
          .getOrElse(
            ir.ParseToTimestamp(
              expression,
              unsupportedAutoformats
                .find(fmt => Try(DateTimeFormatter.ofPattern(fmt).parse(timeStr)).isSuccess)
                .map(ir.Literal(_))))
      // If the string to be parsed isn't a Literal, we do something similar but "at runtime".
      case e =>
        ir.Case(
          Some(ir.TypeOf(e)),
          Seq(
            ir.WhenBranch(
              ir.Literal("string"),
              ir.IfNull(
                ir.Coalesce(ir.TryToTimestamp(ir.TryCast(e, ir.IntegerType)) +: unsupportedAutoformats.map(
                  makeAutoFormatExplicit(e, _))),
                ir.ParseToTimestamp(e)))),
          Some(ir.Cast(expression, ir.TimestampType)))
    }

  private def makeAutoFormatExplicit(expr: ir.Expression, javaDateTimeFormatString: String): ir.Expression =
    if (javaDateTimeFormatString.startsWith("EEE")) {
      // Since version 3.0, Spark doesn't support day-of-week field in datetime parsing
      // Considering that this is piece of information is irrelevant for parsing a timestamp
      // we simply ignore it from the input string and the format.
      ir.TryToTimestamp(ir.Substring(expr, ir.Literal(4)), Some(ir.Literal(javaDateTimeFormatString.substring(3))))
    } else {
      ir.TryToTimestamp(expr, Some(ir.Literal(javaDateTimeFormatString)))
    }

  private[this] val temporalFormatMapping = Seq(
    "YYYY" -> "yyyy",
    "YY" -> "yy",
    "MON" -> "MMM",
    "DD" -> "dd",
    "DY" -> "EEE", // will be ignored down the line as it isn't supported anymore since Spark 3.0
    "HH24" -> "HH",
    "HH12" -> "hh",
    "AM" -> "a",
    "PM" -> "a",
    "MI" -> "mm",
    "SS" -> "ss",
    "FF9" -> "SSSSSSSSS",
    "FF8" -> "SSSSSSSS",
    "FF7" -> "SSSSSSS",
    "FF6" -> "SSSSSS",
    "FF5" -> "SSSSS",
    "FF4" -> "SSSS",
    "FF3" -> "SSS",
    "FF2" -> "SS",
    "FF1" -> "S",
    "FF0" -> "",
    "FF" -> "SSSSSSSSS",
    "TZH:TZM" -> "ZZZ",
    "TZHTZM" -> "ZZZ",
    "TZH" -> "ZZZ",
    "UUUU" -> "yyyy",
    "\"" -> "'")

  private def dayname(args: Seq[ir.Expression]): ir.Expression = {
    ir.DateFormatClass(args.head, ir.Literal("E"))
  }

  private def toDate(functionCall: ir.Expression, args: Seq[ir.Expression]): Transformation[ir.Expression] = {
    if (args.size == 1) {
      ok(ir.Cast(args.head, ir.DateType))
    } else if (args.size == 2) {
      ok(ir.ParseToDate(args.head, Some(args(1))))
    } else {
      lift(PartialResult(functionCall, ir.WrongNumberOfArguments("TO_DATE", args.size, "1 or 2")))
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

  private def decode(functionCall: ir.Expression, args: Seq[ir.Expression]): Transformation[ir.Expression] = {
    if (args.size >= 3) {
      val expr = args.head
      val groupedArgs = args.tail.sliding(2, 2).toList
      ok(
        ir.Case(
          None,
          groupedArgs.takeWhile(_.size == 2).map(l => makeWhenBranch(expr, l.head, l.last)),
          groupedArgs.find(_.size == 1).map(_.head)))
    } else {
      lift(PartialResult(functionCall, ir.WrongNumberOfArguments("DECODE", args.size, "at least 3")))
    }
  }

  private def makeWhenBranch(expr: ir.Expression, cond: ir.Expression, out: ir.Expression): ir.WhenBranch = {
    cond match {
      case ir.Literal.Null => ir.WhenBranch(ir.IsNull(expr), out)
      case any => ir.WhenBranch(ir.Equals(expr, any), out)
    }
  }

  private def arraySort(args: Seq[ir.Expression]): Transformation[ir.Expression] = {
    makeArraySort(args.head, args.lift(1), args.lift(2))
  }

  private def makeArraySort(
      arr: ir.Expression,
      sortAscending: Option[ir.Expression],
      nullsFirst: Option[ir.Expression]): Transformation[ir.Expression] = {
    // Currently, only TRUE/FALSE Boolean literals are supported for Boolean parameters.
    val paramSortAsc = sortAscending.getOrElse(ir.Literal.True)
    val paramNullsFirst = nullsFirst.map(ok).getOrElse {
      paramSortAsc match {
        case ir.Literal.True => ok(ir.Literal.False)
        case ir.Literal.False => ok(ir.Literal.True)
        case x => lift(PartialResult(x, ir.UnsupportedArguments("ARRAY_SORT", Seq(paramSortAsc))))
      }
    }

    def handleComparison(
        isNullOrSmallFirst: ir.Expression,
        nullOrSmallAtLeft: Boolean): Transformation[ir.Expression] = {
      isNullOrSmallFirst match {
        case ir.Literal.True => ok(if (nullOrSmallAtLeft) ir.Literal(-1) else oneLiteral)
        case ir.Literal.False => ok(if (nullOrSmallAtLeft) oneLiteral else ir.Literal(-1))
        case x => lift(PartialResult(x, ir.UnsupportedArguments("ARRAY_SORT", Seq(isNullOrSmallFirst))))
      }
    }

    val comparator = {
      for {
        leftCond <- paramNullsFirst.flatMap(handleComparison(_, nullOrSmallAtLeft = true))
        rightCond <- paramNullsFirst.flatMap(handleComparison(_, nullOrSmallAtLeft = false))
        leftSort <- handleComparison(paramSortAsc, nullOrSmallAtLeft = true)
        rightSort <- handleComparison(paramSortAsc, nullOrSmallAtLeft = false)
      } yield ir.LambdaFunction(
        ir.Case(
          None,
          Seq(
            ir.WhenBranch(ir.And(ir.IsNull(ir.Id("left")), ir.IsNull(ir.Id("right"))), zeroLiteral),
            ir.WhenBranch(ir.IsNull(ir.Id("left")), leftCond),
            ir.WhenBranch(ir.IsNull(ir.Id("right")), rightCond),
            ir.WhenBranch(ir.LessThan(ir.Id("left"), ir.Id("right")), leftSort),
            ir.WhenBranch(ir.GreaterThan(ir.Id("left"), ir.Id("right")), rightSort)),
          Some(zeroLiteral)),
        Seq(ir.UnresolvedNamedLambdaVariable(Seq("left")), ir.UnresolvedNamedLambdaVariable(Seq("right"))))
    }

    paramNullsFirst.flatMap { pnf =>
      (paramSortAsc, pnf) match {
        // We can make the IR much simpler for some cases
        // by using DBSQL SORT_ARRAY function without needing a custom comparator
        case (ir.Literal.True, ir.Literal.True) => ok(ir.SortArray(arr, None))
        case (ir.Literal.False, ir.Literal.False) => ok(ir.SortArray(arr, Some(ir.Literal.False)))
        case _ => comparator.map(ir.ArraySort(arr, _))
      }
    }
  }

  private def parseLastDay(args: Seq[ir.Expression]): Transformation[ir.Expression] = {

    def lastDay(datePart: String): ir.Expression =
      ir.DateAdd(ir.TimestampAdd(datePart, oneLiteral, ir.TruncDate(args.head, args(1))), ir.Literal(-1))

    if (args.length == 1) {
      ok(ir.LastDay(args.head))
    } else {
      val validDateParts = Set("YEAR", "QUARTER", "MONTH", "WEEK")
      args(1) match {
        case ir.StringLiteral(part) if validDateParts(part.toUpperCase()) => ok(lastDay(part.toUpperCase()))
        case ir.Column(_, ir.Id(part, _)) if validDateParts(part.toUpperCase()) => ok(lastDay(part.toUpperCase()))
        case ir.Name(part) if validDateParts(part.toUpperCase()) => ok(lastDay(part.toUpperCase()))
        case x => lift(PartialResult(x, ir.UnsupportedDateTimePart(x)))
      }
    }
  }

}
