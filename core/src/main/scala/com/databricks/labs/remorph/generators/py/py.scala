package com.databricks.labs.remorph.generators

import com.databricks.labs.remorph.{TBA, RemorphContext}

package object py {

  type Python = TBA[RemorphContext, String]
}
