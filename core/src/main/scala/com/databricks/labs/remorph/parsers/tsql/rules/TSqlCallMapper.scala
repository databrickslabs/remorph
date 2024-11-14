package com.databricks.labs.remorph.parsers.tsql.rules

import com.databricks.labs.remorph.intermediate._

class TSqlCallMapper extends CallMapper {

  override def convert(call: Fn): Expression = {
    call match {
      case CallFunction("DATEADD", args) =>
        processDateAdd(args)
      case CallFunction("GET_BIT", args) => BitwiseGet(args.head, args(1))
      case CallFunction("SET_BIT", args) => genBitSet(args)
      case CallFunction("CHECKSUM_AGG", args) => checksumAgg(args)

      // No special case for TSQl, so we ask the main mapper to look at this one
      case cf: CallFunction => super.convert(cf)

      // As well as CallFunctions, we can receive concrete functions, which are already resolved,
      // and don't need to be converted
      case x: Fn => x
    }
  }

  /**
   * Converts a CHECKSUM_ARG call to a MD5 function call sequence
   * @param args
   * @return
   */
  private def checksumAgg(args: Seq[Expression]): Expression = {
    Md5(ConcatWs(Seq(Literal(","), CollectList(args.head))))
  }

  private def genBitSet(args: Seq[Expression]): Expression = {
    val x = args.head
    val n = args(1)
    val v = if (args.length > 2) { args(2) }
    else { Literal(1) }

    // There is no direct way to achieve a bit set in Databricks SQL, so
    // we use standard bitwise operations to achieve the same effect. If we have
    // literals for the bit the bit Value, we can generate less complicated
    // code, but if we have columns or other expressions, we have to generate a longer sequence
    // as we don't know if we are setting or clearing a bit until runtime.
    v match {
      case lit: Literal if lit == Literal(1) => BitwiseOr(x, ShiftLeft(Literal(1), n))
      case _ =>
        BitwiseOr(BitwiseAnd(x, BitwiseXor(Literal(-1), ShiftLeft(Literal(1), n))), ShiftRight(v, n))
    }
  }

  private def processDateAdd(args: Seq[Expression]): Expression = {

    // The first argument of the TSQL DATEADD function is the interval type, which is one of way too
    // many strings and aliases for "day", "month", "year", etc. We need to extract this string and
    // perform the translation based on what we get
    val interval = args.head match {
      case Column(_, Id(id, _)) => id.toLowerCase()
      case _ =>
        throw new IllegalArgumentException("DATEADD interval type is not valid. Should be 'day', 'month', 'year', etc.")
    }

    // The value is how many units, type indicated by interval, to add to the date
    val value = args(1)

    // And this is the thing we are going to add the value to
    val objectReference = args(2)

    // The interval type names are all over the place in TSQL, some of them having names that
    // belie their actual function.
    interval match {

      // Days are all that Spark DATE_ADD operates on, but the arguments are transposed from TSQL
      // despite the fact that 'dayofyear' implies the number of the day in the year, it is in fact the
      // same as day, as is `weekday`
      case "day" | "dayofyear" | "dd" | "d" | "dy" | "y" | "weekday" | "dw" | "w" =>
        DateAdd(objectReference, value)

      // Months are handled by the MonthAdd function, with arguments transposed from TSQL
      case "month" | "mm" | "m" => AddMonths(objectReference, value)

      // There is no equivalent to quarter in Spark, so we have to use the MonthAdd function and multiply by 3
      case "quarter" | "qq" | "q" => AddMonths(objectReference, Multiply(value, Literal(3)))

      // There is no equivalent to year in Spark SQL, but we use months and multiply by 12
      case "year" | "yyyy" | "yy" => AddMonths(objectReference, Multiply(value, Literal(12)))

      // Weeks are not supported in Spark SQL, but we can multiply by 7 to get the same effect with DATE_ADD
      case "week" | "wk" | "ww" => DateAdd(objectReference, Multiply(value, Literal(7)))

      // Hours are not supported in Spark SQL, but we can use the number of hours to create an INTERVAL
      // and add it to the object reference
      case "hour" | "hh" => Add(objectReference, KnownInterval(value, HOUR_INTERVAL))

      // Minutes are not supported in Spark SQL, but we can use the number of minutes to create an INTERVAL
      // and add it to the object reference
      case "minute" | "mi" | "n" => Add(objectReference, KnownInterval(value, MINUTE_INTERVAL))

      // Seconds are not supported in Spark SQL, but we can use the number of seconds to create an INTERVAL
      // and add it to the object reference
      case "second" | "ss" | "s" => Add(objectReference, KnownInterval(value, SECOND_INTERVAL))

      // Milliseconds are not supported in Spark SQL, but we can use the number of milliseconds to create an INTERVAL
      // and add it to the object reference
      case "millisecond" | "ms" => Add(objectReference, KnownInterval(value, MILLISECOND_INTERVAL))

      // Microseconds are not supported in Spark SQL, but we can use the number of microseconds to create an INTERVAL
      // and add it to the object reference
      case "microsecond" | "mcs" => Add(objectReference, KnownInterval(value, MICROSECOND_INTERVAL))

      // Nanoseconds are not supported in Spark SQL, but we can use the number of nanoseconds to create an INTERVAL
      // and add it to the object reference
      case "nanosecond" | "ns" => Add(objectReference, KnownInterval(value, NANOSECOND_INTERVAL))

      case _ =>
        throw new IllegalArgumentException(
          s"DATEADD interval type '${interval}' is not valid. Should be 'day', 'month', 'year', etc.")
    }
  }
}
