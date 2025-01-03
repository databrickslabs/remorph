package com.databricks.labs.remorph.support

import java.sql.Connection

trait ConnectionFactory {
  def newConnection(): Connection
}
