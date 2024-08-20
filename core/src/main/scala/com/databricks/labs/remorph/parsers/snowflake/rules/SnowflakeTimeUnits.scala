package com.databricks.labs.remorph.parsers.snowflake.rules

object SnowflakeTimeUnits {
  private val dateParts = Map(
    Set("YEAR", "Y", "YY", "YYY", "YYYY", "YR", "YEARS", "YRS") -> "year",
    Set("MONTH", "MM", "MON", "MONS", "MONTHS") -> "month",
    Set("DAY", "D", "DD", "DAYS", "DAYOFMONTH") -> "day",
    Set("DAYOFWEEK", "WEEKDAY", "DOW", "DW") -> "dayofweek",
    Set("DAYOFWEEKISO", "WEEKDAY_ISO", "DOW_ISO", "DW_ISO") -> "dayofweekiso",
    Set("DAYOFYEAR", "YEARDAY", "DOY", "DY") -> "dayofyear",
    Set("WEEK", "W", "WK", "WEEKOFYEAR", "WOY", "WY") -> "week",
    Set("WEEKISO", "WEEK_ISO", "WEEKOFYEARISO", "WEEKOFYEAR_ISO") -> "weekiso",
    Set("QUARTER", "Q", "QTR", "QTRS", "QUARTERS") -> "quarter",
    Set("YEAROFWEEK") -> "yearofweek",
    Set("YEAROFWEEKISO") -> "yearofweekiso")

  def findDatePart(datePart: String): Option[String] =
    dateParts.find(_._1.contains(datePart.toUpperCase())).map(_._2)

  private val timeParts = Map(
    Set("HOUR", "H", "HH", "HR", "HOURS", "HRS") -> "hour",
    Set("MINUTE", "M", "MI", "MIN", "MINUTES", "MINS") -> "minute",
    Set("SECOND", "S", "SEC", "SECONDS", "SECS") -> "second",
    Set("MILLISECOND", "MS", "MSEC", "MILLISECONDS") -> "millisecond",
    Set("MICROSECOND", "US", "USEC", "MICROSECONDS") -> "microsecond",
    Set("NANOSECOND", "NS", "NSEC", "NANOSEC", "NSECOND", "NANOSECONDS", "NANOSECS", "NSECONDS") -> "nanosecond",
    Set("EPOCH_SECOND", "EPOCH", "EPOCH_SECONDS") -> "epoch_second",
    Set("EPOCH_MILLISECOND", "EPOCH_MILLISECONDS") -> "epoch_millisecond",
    Set("EPOCH_MICROSECOND", "EPOCH_MICROSECONDS") -> "epoch_microsecond",
    Set("EPOCH_NANOSECOND", "EPOCH_NANOSECONDS") -> "epoch_nanosecond",
    Set("TIMEZONE_HOUR", "TZH") -> "timezone_hour",
    Set("TIMEZONE_MINUTE", "TZM") -> "timezone_minute")


  def findTimePart(timePart: String): Option[String] =
    timeParts.find(_._1.contains(timePart.toUpperCase())).map(_._2)

  def findDateOrTimePart(part: String): Option[String] =
    (dateParts ++ timeParts).find(_._1.contains(part.toUpperCase())).map(_._2)
}
