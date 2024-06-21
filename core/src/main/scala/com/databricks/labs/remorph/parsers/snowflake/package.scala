package com.databricks.labs.remorph.parsers

import com.databricks.labs.remorph.parsers.{intermediate => ir}
package object snowflake {

  // dummy implementation because the grammar for this is missing
  // see https://github.com/databrickslabs/remorph/issues/258
  private[snowflake] val DummyWindowFrame =
    ir.WindowFrame(frame_type = ir.RowsFrame, lower = ir.UnboundedPreceding, upper = ir.UnboundedFollowing)

}
