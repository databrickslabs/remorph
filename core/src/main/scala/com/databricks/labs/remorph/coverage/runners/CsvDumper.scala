package com.databricks.labs.remorph.coverage.runners

import com.github.tototoshi.csv.CSVWriter

import java.io.StringWriter
import java.sql.{Connection, ResultSet}

class CsvDumper(connection: Connection) {
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

    // write the header
    val metaData = resultSet.getMetaData
    val columnCount = metaData.getColumnCount
    val header = (1 to columnCount).map(metaData.getColumnName)
    csvWriter.writeRow(header)

    // write the data
    while (resultSet.next()) {
      val row = (1 to columnCount).map(resultSet.getString)
      csvWriter.writeRow(row)
    }

    writer.toString()
  }
}
