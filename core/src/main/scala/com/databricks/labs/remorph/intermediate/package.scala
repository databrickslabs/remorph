package com.databricks.labs.remorph

package object intermediate {
  type WithKnownLocationRange[A] = A with KnownLocationRange
}
