package com.databricks.labs.remorph

package object intermediate {

  type WithKnownOrigin[A] = A with KnownOrigin
}
