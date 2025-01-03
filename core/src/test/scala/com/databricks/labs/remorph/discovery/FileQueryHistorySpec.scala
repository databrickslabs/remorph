package com.databricks.labs.remorph.discovery

import org.scalatest.flatspec.AnyFlatSpec
import org.scalatest.matchers.should.Matchers
import java.nio.file.Files
import java.nio.file.StandardOpenOption._
import scala.collection.JavaConverters._

class FileQueryHistorySpec extends AnyFlatSpec with Matchers {

  "FileQueryHistory" should "correctly extract queries from SQL files" in {
    val tempDir = Files.createTempDirectory("test_sql_files")

    try {
      val sqlFile = tempDir.resolve("test.sql")
      val sqlContent =
        """
          |SELECT * FROM table1;
          |SELECT * FROM table2;
          |""".stripMargin
      Files.write(sqlFile, sqlContent.getBytes, CREATE, WRITE)

      val fileQueryHistory = new FileQueryHistory(tempDir)

      val queryHistory = fileQueryHistory.history()

      queryHistory.queries should have size 1
      queryHistory.queries.head.source shouldBe
        """
          |SELECT * FROM table1;
          |SELECT * FROM table2;
          |""".stripMargin

    } finally {
      // Clean up the temporary directory
      Files.walk(tempDir).iterator().asScala.toSeq.reverse.foreach(Files.delete)
    }
  }
}
