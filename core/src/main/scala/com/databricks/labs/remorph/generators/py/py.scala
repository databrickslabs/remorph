package com.databricks.labs.remorph.generators

import com.databricks.labs.remorph.{Transformation, Phase}

package object py {

  type Python = Transformation[Phase, String]
}
