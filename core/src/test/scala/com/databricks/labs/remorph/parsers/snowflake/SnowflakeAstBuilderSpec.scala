package com.databricks.labs.remorph.parsers.snowflake

import com.databricks.labs.remorph.parsers.intermediate.{Alias, Column, NamedTable, Project}
import org.antlr.v4.runtime.{CharStreams, CommonTokenStream}
import org.scalatest.matchers.should.Matchers
import org.scalatest.wordspec.AnyWordSpec

class SnowflakeAstBuilderSpec extends AnyWordSpec with Matchers {

  private def parseString(input: String): SnowflakeParser.Snowflake_fileContext = {
    val inputString = CharStreams.fromString(input)
    val lexer = new SnowflakeLexer(inputString)
    val tokenStream = new CommonTokenStream(lexer)
    val parser = new SnowflakeParser(tokenStream)
    val tree = parser.snowflake_file()
    // uncomment the following line if you need a peek in the Snowflake AST
    // println(tree.toStringTree(parser))
    tree
  }

  "SnowflakeVisitor" should {
    "translate a simple SELECT query" in {
      val query = "SELECT a FROM b"

      val sfTree = parseString(query)

      val result = new SnowflakeAstBuilder().visit(sfTree)

      result shouldBe Project(NamedTable("b", Map.empty, is_streaming = false), Seq(Column("a")))
    }

    "translate a simple SELECT query with an aliased column" in {

      val query = "SELECT a AS aa FROM b"

      val sfTree = parseString(query)

      val result = new SnowflakeAstBuilder().visit(sfTree)

      result shouldBe
        Project(NamedTable("b", Map.empty, is_streaming = false), Seq(Alias(Column("a"), Seq("aa"), None)))
    }

    "translate a simple SELECT query involving multiple columns" in {

      val query = "SELECT a, b, c FROM table_x"

      val sfTree = parseString(query)

      val result = new SnowflakeAstBuilder().visit(sfTree)

      result shouldBe Project(
        NamedTable("table_x", Map.empty, is_streaming = false),
        Seq(Column("a"), Column("b"), Column("c")))
    }

    "translate a SELECT query involving multiple columns and aliases" in {

      val query = "SELECT a, b AS bb, c FROM table_x"

      val sfTree = parseString(query)

      val result = new SnowflakeAstBuilder().visit(sfTree)

      result shouldBe Project(
        NamedTable("table_x", Map.empty, is_streaming = false),
        Seq(Column("a"), Alias(Column("b"), Seq("bb"), None), Column("c")))
    }
  }

}
