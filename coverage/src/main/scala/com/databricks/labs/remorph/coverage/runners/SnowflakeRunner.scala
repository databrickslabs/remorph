package com.databricks.labs.remorph.coverage.runners

import java.io.StringWriter
import java.sql.{Connection, DriverManager, ResultSet}

class SnowflakeRunner(env: EnvGetter) {
  //  Class.forName(driver)
  val connection = DriverManager.getConnection(url, username, password)

  def queryToCSV(query: String): String = {
    val statement = connection.createStatement()
    val resultSet = statement.executeQuery(query)
    val csv = resultSetToCSV(resultSet)
    resultSet.close()
    statement.close()
    csv
  }

    private def resultSetToCSV(resultSet: ResultSet): String = {
      val writer = new StringWriter()
      val csvWriter = new CSVWriter(writer)
      csvWriter.writeAll(resultSetToArrayList(resultSet))
      writer.toString()
  }

  def close() {
    connection.close()
  }
}
