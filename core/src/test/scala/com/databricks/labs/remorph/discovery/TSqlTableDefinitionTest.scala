package com.databricks.labs.remorph.discovery

import org.mockito.ArgumentMatchers.anyString
import org.mockito.Mockito._
import org.scalatest.flatspec.AnyFlatSpec
import org.scalatest.matchers.should.Matchers
import org.scalatestplus.mockito.MockitoSugar

import java.sql.{Connection, ResultSet, Statement}

class TSqlTableDefinitionTest extends AnyFlatSpec with Matchers with MockitoSugar {

  "getTableDefinitions" should "return correct table definitions for valid catalog name" in {
    val conn = mock[Connection]
    val stmt = mock[Statement]
    val rs = mock[ResultSet]
    val mockRs = mock[ResultSet]
    when(conn.createStatement()).thenReturn(stmt)
    when(stmt.executeQuery(anyString())).thenReturn(mockRs)
    when(mockRs.next()).thenReturn(true, false)
    when(mockRs.getString("TABLE_CATALOG")).thenReturn("CATALOG")
    when(mockRs.getString("TABLE_SCHEMA")).thenReturn("SCHEMA")
    when(mockRs.getString("TABLE_NAME")).thenReturn("TABLE")
    when(mockRs.getString("DERIVED_SCHEMA")).thenReturn("col1§int§true§hi‡col2§string§false§hi")
    when(mockRs.getString("LOCATION")).thenReturn(null)
    when(mockRs.getString("FILE_FORMAT_NAME")).thenReturn(null)
    when(mockRs.getString("VIEW_DEFINITION")).thenReturn(null)
    when(mockRs.getInt("BYTES")).thenReturn(1024 * 1024 * 1024)

    when(stmt.executeQuery("SELECT NAME FROM sys.databases WHERE NAME != 'MASTER'")).thenReturn(rs)
    when(rs.next()).thenReturn(true, false)
    when(rs.getString("name")).thenReturn("catalog")

    val tSqlTableDefinitions = new TSqlTableDefinitions(conn)
    val result = tSqlTableDefinitions.getAllTableDefinitions
    result should not be empty
  }

  "getAllSchemas" should "return all schemas for valid catalog name" in {
    val conn = mock[Connection]
    val stmt = mock[Statement]
    val rs = mock[ResultSet]
    when(conn.createStatement()).thenReturn(stmt)
    when(stmt.executeQuery(anyString())).thenReturn(rs)
    when(rs.next()).thenReturn(true, false)
    when(rs.getString("SCHEMA_NAME")).thenReturn("schema")

    val tSqlTableDefinitions = new TSqlTableDefinitions(conn)
    val result = tSqlTableDefinitions.getAllSchemas("catalog")
    result should contain("schema")
  }

  "getAllCatalogs" should "return all catalogs" in {
    val conn = mock[Connection]
    val stmt = mock[Statement]
    val rs = mock[ResultSet]
    when(conn.createStatement()).thenReturn(stmt)
    when(stmt.executeQuery(anyString())).thenReturn(rs)
    when(rs.next()).thenReturn(true, false)
    when(rs.getString("name")).thenReturn("catalog")

    val tSqlTableDefinitions = new TSqlTableDefinitions(conn)
    val result = tSqlTableDefinitions.getAllCatalogs
    result should contain("catalog")
  }

}
