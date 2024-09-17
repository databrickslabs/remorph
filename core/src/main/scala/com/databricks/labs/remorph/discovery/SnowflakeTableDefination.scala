//scalastyle:off
package com.databricks.labs.remorph.discovery

import com.databricks.labs.remorph.parsers.intermediate.{DataType, StructField}
import com.databricks.labs.remorph.parsers.tsql.{TSqlLexer, TSqlParser}
import org.antlr.v4.runtime.{CharStreams, CommonTokenStream}

import java.sql.Connection
import scala.collection.mutable.ListBuffer

class SnowflakeTableDefination(conn: Connection) {

  private def getDataType(dataTypeString: String): DataType = {
    val inputString = CharStreams.fromString(dataTypeString)
    val lexer = new TSqlLexer(inputString)
    val tokenStream = new CommonTokenStream(lexer)
    val parser = new TSqlParser(tokenStream)
    val ctx = parser.dataType()
    import com.databricks.labs.remorph.parsers.tsql.DataTypeBuilder
    val dataTypeBuilder = new DataTypeBuilder
    dataTypeBuilder.build(ctx)
  }

  def getTableDefinations(): Seq[TableDefinition] = {
    val stmt = conn.createStatement()
    val columnSchemaQuery = s"""SELECT
                               |    sft.TABLE_CATALOG,
                               |    sft.TABLE_SCHEMA,
                               |    sft.TABLE_NAME,
                               |    t.Schema as derivedSchema,
                               |    sft.BYTES,
                               |    sft.TABLE_TYPE
                               |FROM (
                               |    SELECT
                               |        TABLE_CATALOG,
                               |        TABLE_SCHEMA,
                               |        TABLE_NAME,
                               |        LISTAGG(column_name || ':' ||
                               |            CASE
                               |                WHEN numeric_precision IS NOT NULL AND numeric_scale IS NOT NULL
                               |                THEN
                               |                    CONCAT(data_type, '(', numeric_precision, ',' , numeric_scale, ')')
                               |                WHEN LOWER(data_type) = 'text'
                               |                THEN
                               |                    CONCAT('varchar', '(', CHARACTER_MAXIMUM_LENGTH, ')')
                               |                ELSE data_type
                               |             END|| ':' || TO_BOOLEAN(CASE WHEN IS_NULLABLE = 'YES' THEN 'true' ELSE 'false' END),
                               |        '~') WITHIN GROUP (ORDER BY ordinal_position) AS Schema
                               |    FROM
                               |        SNOWFLAKE.INFORMATION_SCHEMA.COLUMNS
                               |    GROUP BY
                               |        TABLE_CATALOG, TABLE_SCHEMA, TABLE_NAME
                               |) t
                               |JOIN SNOWFLAKE.INFORMATION_SCHEMA.TABLES sft
                               |    ON t.TABLE_CATALOG = sft.TABLE_CATALOG
                               |    AND t.TABLE_SCHEMA = sft.TABLE_SCHEMA
                               |    AND t.TABLE_NAME = sft.TABLE_NAME
                               |ORDER BY
                               |    sft.TABLE_CATALOG, sft.TABLE_SCHEMA, sft.TABLE_NAME;""".stripMargin
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
            .map(x => {
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
