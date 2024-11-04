package com.databricks.labs.remorph.generators

import com.databricks.labs.remorph.{Phase, Transformation}

package object sql {

  type SQL = Transformation[Phase, String]
}
