package com.databricks.labs.remorph.generators

import com.databricks.labs.remorph.{RemorphContext, TBA}

package object sql {

  type SQL = TBA[RemorphContext, String]
}
