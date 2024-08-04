package com.databricks.labs.remorph.parsers.snowflake.rules

import com.databricks.labs.remorph.parsers.intermediate.{CallFunction, CallMapper, DateAdd, Expression, Fn, RLike}

class SnowflakeCallMapper extends CallMapper {

  override def convert(call: Fn): Expression = {
    call match {
      case CallFunction("DATEADD", args) =>
        DateAdd(args.head, args(1))
      case CallFunction("REGEXP_LIKE", args) =>
        RLike(args.head, args(1))
      case x: CallFunction => super.convert(x)
    }
  }
}
