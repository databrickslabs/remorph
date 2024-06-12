package com.databricks.labs.remorph.parsers

import com.databricks.labs.remorph.parsers.snowflake.SnowflakeParser.IdContext
import com.databricks.labs.remorph.parsers.{intermediate => ir}
package object snowflake {

  // dummy implementation because the grammar for this is missing
  // see https://github.com/databrickslabs/remorph/issues/258
  private[snowflake] val DummyWindowFrame = ir.WindowFrame(
    frame_type = ir.RowsFrame,
    lower = ir.FrameBoundary(current_row = false, unbounded = true, value = ir.Noop),
    upper = ir.FrameBoundary(current_row = true, unbounded = false, value = ir.Noop))

  private[snowflake] def getIdText(ctx: IdContext): String = {
    // wrong implementation (doesn't work for quoted ids, waiting for grammar fix)
    ctx.getText
  }
}
