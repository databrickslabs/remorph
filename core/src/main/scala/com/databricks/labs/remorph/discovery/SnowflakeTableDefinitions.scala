package com.databricks.labs.remorph.discovery

import com.databricks.labs.remorph.intermediate.{DataType, Metadata, StructField}
import com.databricks.labs.remorph.parsers.snowflake.{SnowflakeLexer, SnowflakeParser, SnowflakeTypeBuilder}
import org.antlr.v4.runtime.{CharStreams, CommonTokenStream}

import java.sql.Connection
import scala.collection.mutable

class SnowflakeTableDefinitions(conn: Connection) {

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
    val dataTypeBuilder = new SnowflakeTypeBuilder
    dataTypeBuilder.buildDataType(ctx)
  }

  private def getTableDefinitionQuery(catalogName: String): String = {
    s"""WITH column_info AS (
       |  SELECT
       |    TABLE_CATALOG,
       |    TABLE_SCHEMA,
       |    TABLE_NAME,
       |    LISTAGG(
       |      column_name || '§' || CASE
       |        WHEN numeric_precision IS NOT NULL
       |        AND numeric_scale IS NOT NULL THEN CONCAT(data_type, '(', numeric_precision, ',', numeric_scale, ')')
       |        WHEN LOWER(data_type) = 'text' THEN CONCAT('varchar', '(', CHARACTER_MAXIMUM_LENGTH, ')')
       |        ELSE data_type
       |      END || '§' || TO_BOOLEAN(
       |        CASE
       |          WHEN IS_NULLABLE = 'YES' THEN 'true'
       |          ELSE 'false'
       |        END
       |      ) || '§' || COALESCE(COMMENT, ''),
       |      '‡'
       |    ) WITHIN GROUP (
       |      ORDER BY
       |        ordinal_position
       |    ) AS Schema
       |  FROM
       |    ${catalogName}.INFORMATION_SCHEMA.COLUMNS
       |  GROUP BY
       |    TABLE_CATALOG,
       |    TABLE_SCHEMA,
       |    TABLE_NAME
       |)
       |SELECT
       |  sft.TABLE_CATALOG,
       |  sft.TABLE_SCHEMA,
       |  sft.TABLE_NAME,
       |  sft.comment,
       |  sfe.location,
       |  sfe.file_format_name,
       |  sfv.view_definition,
       |  column_info.Schema AS DERIVED_SCHEMA,
       |  FLOOR(sft.BYTES / (1024 * 1024 * 1024)) AS SIZE_GB
       |FROM
       |  column_info
       |  JOIN ${catalogName}.INFORMATION_SCHEMA.TABLES sft ON column_info.TABLE_CATALOG = sft.TABLE_CATALOG
       |  AND column_info.TABLE_SCHEMA = sft.TABLE_SCHEMA
       |  AND column_info.TABLE_NAME = sft.TABLE_NAME
       |  LEFT JOIN ${catalogName}.INFORMATION_SCHEMA.VIEWS sfv ON column_info.TABLE_CATALOG = sfv.TABLE_CATALOG
       |  AND column_info.TABLE_SCHEMA = sfv.TABLE_SCHEMA
       |  AND column_info.TABLE_NAME = sfv.TABLE_NAME
       |  LEFT JOIN ${catalogName}.INFORMATION_SCHEMA.EXTERNAL_TABLES sfe ON column_info.TABLE_CATALOG = sfe.TABLE_CATALOG
       |  AND column_info.TABLE_SCHEMA = sfe.TABLE_SCHEMA
       |  AND column_info.TABLE_NAME = sfe.TABLE_NAME
       |ORDER BY
       |  sft.TABLE_CATALOG,
       |  sft.TABLE_SCHEMA,
       |  sft.TABLE_NAME;
       |""".stripMargin
  }

  /**
   * Retrieves the definitions of all tables in the Snowflake database.
   *
   * @return A sequence of TableDefinition objects representing the tables in the database.
   */
  private def getTableDefinitions(catalogName: String): Seq[TableDefinition] = {
    val stmt = conn.createStatement()
    try {
      val tableDefinitionList = new mutable.ListBuffer[TableDefinition]()
      val rs = stmt.executeQuery(getTableDefinitionQuery(catalogName))
      try {
        while (rs.next()) {
          val tableCatalog = rs.getString("TABLE_CATALOG")
          val tableSchema = rs.getString("TABLE_SCHEMA")
          val tableName = rs.getString("TABLE_NAME")
          val columns = rs
            .getString("DERIVED_SCHEMA")
            .split("‡")
            .map(x => {
              val data = x.split("§")
              val name = data(0)
              val dataType = getDataType(data(1))
              val nullable = data(2).toBoolean
              val comment = if (data.length > 3) Option(data(3)) else None
              StructField(name, dataType, nullable, Option(Metadata(comment)))
            })
          tableDefinitionList.append(
            TableDefinition(
              tableCatalog,
              tableSchema,
              tableName,
              Option(rs.getString("LOCATION")),
              Option(rs.getString("FILE_FORMAT_NAME")),
              Option(rs.getString("VIEW_DEFINITION")),
              columns,
              rs.getInt("SIZE_GB"),
              Option(rs.getString("COMMENT"))))
        }
        tableDefinitionList
      } finally {
        rs.close()
      }
    } finally {
      stmt.close()
    }
  }

  def getAllTableDefinitions: mutable.Seq[TableDefinition] = {
    getAllCatalogs.flatMap(getTableDefinitions)
  }

  def getAllSchemas(catalogName: String): mutable.ListBuffer[String] = {
    val stmt = conn.createStatement()
    try {
      val rs = stmt.executeQuery(s"SHOW SCHEMAS IN $catalogName")
      try {
        val schemaList = new mutable.ListBuffer[String]()
        while (rs.next()) {
          schemaList.append(rs.getString("name"))
        }
        schemaList
      } finally {
        rs.close()
      }
    } finally {
      stmt.close()
    }
  }

  def getAllCatalogs: mutable.ListBuffer[String] = {
    val stmt = conn.createStatement()
    try {
      val rs = stmt.executeQuery("SHOW DATABASES")
      try {
        val catalogList = new mutable.ListBuffer[String]()
        while (rs.next()) {
          catalogList.append(rs.getString("name"))
        }
        catalogList
      } finally {
        rs.close()
      }
    } finally {
      stmt.close()
    }
  }

}
