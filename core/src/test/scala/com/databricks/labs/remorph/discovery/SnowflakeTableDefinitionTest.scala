package com.databricks.labs.remorph.discovery

import java.sql.{Connection, ResultSet, Statement}

import org.mockito.ArgumentMatchers._
import org.mockito.Mockito._
import org.scalatest.matchers.should.Matchers
import org.scalatest.wordspec.AnyWordSpec

class SnowflakeTableDefinitionTest extends AnyWordSpec with Matchers {

  "getTableDefinitions" should {

    "return table definitions for a all catalogs" in {
      val mockConn = mock(classOf[Connection])
      val mockStmt = mock(classOf[Statement])
      val mockRs = mock(classOf[ResultSet])

      when(mockConn.createStatement()).thenReturn(mockStmt)
      when(mockStmt.executeQuery(anyString())).thenReturn(mockRs)
      when(mockRs.next()).thenReturn(true, false)
      when(mockRs.getString("TABLE_CATALOG")).thenReturn("CATALOG")
      when(mockRs.getString("TABLE_SCHEMA")).thenReturn("SCHEMA")
      when(mockRs.getString("TABLE_NAME")).thenReturn("TABLE")
      when(mockRs.getString("DERIVED_SCHEMA")).thenReturn("col1§int§true§comment‡col2§string§false§comment")
      when(mockRs.getString("LOCATION")).thenReturn(null)
      when(mockRs.getString("FILE_FORMAT_NAME")).thenReturn(null)
      when(mockRs.getString("VIEW_DEFINITION")).thenReturn(null)
      when(mockRs.getInt("BYTES")).thenReturn(1024 * 1024 * 1024)

      // Mock behavior for getAllCatalogs
      val mockCatalogResultSet = mock(classOf[ResultSet])
      when(mockStmt.executeQuery("SHOW DATABASES")).thenReturn(mockCatalogResultSet)
      when(mockCatalogResultSet.next()).thenReturn(true, false)
      when(mockCatalogResultSet.getString("name")).thenReturn("TEST_CATALOG")

      val snowflakeTableDefinitions = new SnowflakeTableDefinitions(mockConn)
      val result = snowflakeTableDefinitions.getAllTableDefinitions

      result should have size 1
      result.head.columns should have size 2
    }

    "return all schemas for a valid catalog" in {
      val mockConn = mock(classOf[Connection])
      val mockStmt = mock(classOf[Statement])
      val mockRs = mock(classOf[ResultSet])

      when(mockConn.createStatement()).thenReturn(mockStmt)
      when(mockStmt.executeQuery(anyString())).thenReturn(mockRs)
      when(mockRs.next()).thenReturn(true, true, false)
      when(mockRs.getString("name")).thenReturn("SCHEMA1", "SCHEMA2")

      val snowflakeTableDefinitions = new SnowflakeTableDefinitions(mockConn)
      val result = snowflakeTableDefinitions.getAllSchemas("CATALOG")

      result should contain allOf ("SCHEMA1", "SCHEMA2")
    }

    "return all catalogs" in {
      val mockConn = mock(classOf[Connection])
      val mockStmt = mock(classOf[Statement])
      val mockRs = mock(classOf[ResultSet])

      when(mockConn.createStatement()).thenReturn(mockStmt)
      when(mockStmt.executeQuery(anyString())).thenReturn(mockRs)
      when(mockRs.next()).thenReturn(true, true, false)
      when(mockRs.getString("name")).thenReturn("CATALOG1", "CATALOG2")

      val snowflakeTableDefinitions = new SnowflakeTableDefinitions(mockConn)
      val result = snowflakeTableDefinitions.getAllCatalogs

      result should contain allOf ("CATALOG1", "CATALOG2")
    }
  }
}
