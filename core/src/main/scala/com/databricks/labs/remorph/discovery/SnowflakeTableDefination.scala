package com.databricks.labs.remorph.discovery

import com.databricks.labs.remorph.parsers.intermediate.{DataType, StructField}
import com.databricks.labs.remorph.parsers.snowflake.{SnowflakeLexer, SnowflakeParser}
import org.antlr.v4.runtime.{CharStreams, CommonTokenStream}

import java.sql.Connection
import scala.collection.mutable.ListBuffer

/**
 * Class representing the definition of a Snowflake table.
 *
 * @param conn The SQL connection to the Snowflake database.
 */
class SnowflakeTableDefination(conn: Connection) {

  /**
   * Parses a data type string and returns the corresponding DataType object.
   *
   * @param dataTypeString The string representation of the data type.
   * @return The DataType object corresponding to the input string.
   */
  private def getDataType(dataTypeString: String): DataType = {
    val inputString = CharStreams.fromString(dataTypeString)
    val lexer = new SnowflakeLexer(inputString)
    val tokenStream = new CommonTokenStream(lexer)
    val parser = new SnowflakeParser(tokenStream)
    val ctx = parser.dataType()
    import com.databricks.labs.remorph.parsers.snowflake.SnowflakeTypeBuilder
    val dataTypeBuilder = new SnowflakeTypeBuilder
    dataTypeBuilder.buildDataType(ctx)
  }

  /**
   * Retrieves the definitions of all tables in the Snowflake database.
   *
   * @return A sequence of TableDefinition objects representing the tables in the database.
   */
  def getTableDefinitions: Seq[TableDefinition] = {
    val stmt = conn.createStatement()
    val columnSchemaQuery = Constant.tableDefinitionQuery
    try {
      val tableDefinitionList = new scala.collection.mutable.ListBuffer[TableDefinition]()
      val rs = stmt.executeQuery(columnSchemaQuery)
      try {
        while (rs.next()) {
          val TABLE_CATALOG = rs.getString("TABLE_CATALOG")
          val TABLE_SCHEMA = rs.getString("TABLE_SCHEMA")
          val TABLE_NAME = rs.getString("TABLE_NAME")
          val columns = new ListBuffer[StructField]()
          rs.getString(4)
            .split("~")
            .foreach(x => {
              val data = x.split(":")
              val name = data(0)
              val dataType = getDataType(data(1))
              columns.append(StructField(name, dataType, data(2).toBoolean))
            })
          tableDefinitionList.append(
            TableDefinition(
              TABLE_CATALOG,
              TABLE_SCHEMA,
              TABLE_NAME,
              null, // location
              Option(rs.getString("TABLE_TYPE")), // FORMAT
              null, // view text
              columns,
              rs.getInt("BYTES") / (1024 * 1024 * 1024) // sizeGb
            ))
        }
        print(tableDefinitionList.size)
        tableDefinitionList
      } finally {
        rs.close()
      }
    } finally {
      stmt.close()
    }
  }

}
