package com.databricks.labs.remorph.parsers.snowflake.rules

import com.databricks.labs.remorph.parsers.{intermediate => ir}
import com.databricks.labs.remorph.transpilers.TranspileException

class SnowflakeCallMapper extends ir.CallMapper with ir.IRHelpers {

  override def convert(call: ir.Fn): ir.Expression = {
    withNormalizedName(call) match {
      // keep all the names in alphabetical order
      case ir.CallFunction("ARRAY_CAT", args) => ir.Concat(args)
      case ir.CallFunction("ARRAY_CONSTRUCT", args) => ir.CreateArray(args)
      case ir.CallFunction("BASE64_DECODE_STRING", args) => ir.UnBase64(args.head)
      case ir.CallFunction("BASE64_ENCODE", args) => ir.Base64(args.head)
      case ir.CallFunction("BOOLAND_AGG", args) => ir.BoolAnd(args.head)
      case ir.CallFunction("DATEADD", args) => ir.DateAdd(args.head, args(1))
      case ir.CallFunction("EDITDISTANCE", args) => ir.Levenshtein(args.head, args(1))
      case ir.CallFunction("IFNULL", args) => ir.Coalesce(args)
      case ir.CallFunction("JSON_EXTRACT_PATH_TEXT", args) => getJsonObject(args)
      case ir.CallFunction("LEN", args) => ir.Length(args.head)
      case ir.CallFunction("LISTAGG", args) => ir.ArrayJoin(args.head, ir.CollectList(args(1), None), None)
      case ir.CallFunction("MONTHNAME", args) => ir.DateFormatClass(args.head, ir.Literal("MMM"))
      case ir.CallFunction("OBJECT_KEYS", args) => ir.JsonObjectKeys(args.head)
      case ir.CallFunction("POSITION", args) => ir.CallFunction("LOCATE", args)
      case ir.CallFunction("REGEXP_LIKE", args) => ir.RLike(args.head, args(1))
      case ir.CallFunction("SPLIT_PART", args) => splitPart(args)
      case ir.CallFunction("SQUARE", args) => ir.Pow(args.head, ir.Literal(2))
      case ir.CallFunction("STRTOK_TO_ARRAY", args) => split(args)
      case ir.CallFunction("TO_DOUBLE", args) => ir.CallFunction("DOUBLE", args)
      case ir.CallFunction("TO_NUMBER", args) => toNumber(args)
      case ir.CallFunction("TO_OBJECT", args) => ir.StructsToJson(args.head, args(1))
      case ir.CallFunction("TO_VARCHAR", args) => ir.CallFunction("TO_CHAR", args)
      case ir.CallFunction("TRY_BASE64_DECODE_STRING", args) => ir.UnBase64(args.head)
      case ir.CallFunction("TRY_TO_NUMBER", args) => tryToNumber(args)
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
}
