package com.databricks.labs.remorph.discovery

import com.databricks.labs.remorph.parsers.intermediate.StructField

import java.sql.Connection
import scala.collection.mutable.ListBuffer
import com.databricks.labs.remorph.parsers.intermediate.DataType


class SnowflakeTableDefination(conn: Connection) {


  private def getColumDetails(): Seq[StructField] = {
    val stmt = conn.createStatement()
    val columnSchemaQuery = s"""select TABLE_CATALOG,TABLE_SCHEMA,TABLE_NAME,column_name,
                   |case
                   |  when numeric_precision is not null and numeric_scale is not null
                   |  then
                   |  concat(data_type, '(', numeric_precision, ',' , numeric_scale, ')')
                   |  when lower(data_type) = 'text'
                   |  then
                   |  concat('varchar', '(', CHARACTER_MAXIMUM_LENGTH, ')')
                   |  else data_type
                   |end as data_type,
                   |is_nullable,
                   |from SNOWFLAKE.INFORMATION_SCHEMA.COLUMNS
                   |order by ordinal_position""".stripMargin
    try {

      val rs = stmt.executeQuery(columnSchemaQuery)
      try {
        val columns = new ListBuffer[StructField]()
        while (rs.next()) {
          columns.append(
            StructField(
              rs.getString("COLUMN_NAME"),
              null,
              rs.getBoolean("IS_NULLABLE")
            )
          )
        }
        columns
      } finally {
        rs.close()
      }
    } finally {
      stmt.close()
    }
  }

  def getTableDefinations(): Seq[TableDefinition] = {
    val stmt = conn.createStatement()
    try {
      val rs: java.sql.ResultSet = stmt.executeQuery(s"""SELECT  TABLE_CATALOG
                                                        |, TABLE_SCHEMA
                                                        |, TABLE_NAME
                                                        |, TABLE_TYPE
                                                        |, BYTES
                                                        |  FROM
                                                        |    SNOWFLAKE.INFORMATION_SCHEMA.TABLES
                                                       """.stripMargin)
      try {
        val tables = new scala.collection.mutable.ListBuffer[TableDefinition]()
        while (rs.next()) {
          tables.append(
            TableDefinition(
              rs.getString("TABLE_CATALOG"),
              rs.getString("TABLE_SCHEMA"),
              rs.getString("TABLE_NAME"),
              null, // location
              Option(rs.getString("TABLE_TYPE")),// FORMAT
              null, // view text
              null, // columns
                rs.getInt("BYTES")/ (1024*1024*1024) // sizeGb
            )

          )
        }

        println(tables(0).table +" "+ tables(0).sizeGb)
        tables
      } finally {
        rs.close()
      }
    } finally {
      stmt.close()
    }
  }

}
