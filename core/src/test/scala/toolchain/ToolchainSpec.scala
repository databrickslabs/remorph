package toolchain.testsource

import com.databricks.labs.remorph.transpilers.DirectorySource
import org.scalatest.matchers.should.Matchers
import org.scalatest.wordspec.AnyWordSpec

import java.nio.file.Paths

class ToolchainSpec extends AnyWordSpec with Matchers {
  private val projectBaseDir = Paths.get(".").toAbsolutePath.normalize
  private val moduleBaseDir = if (projectBaseDir.endsWith("core")) projectBaseDir else projectBaseDir.resolve("core")
  private val testSourceDir = moduleBaseDir.resolve("src/test/resources/toolchain/testsource").toString

  "Toolchain" should {
    "traverse a directory of files" in {
      val directorySourceWithoutFilter = new DirectorySource(testSourceDir)
      val fileNames = directorySourceWithoutFilter.map(_.filename).toSeq
      val expectedFileNames = Seq("test_1.sql", "test_2.sql", "test_3.sql", "not_sql.md")
      fileNames should contain theSameElementsAs expectedFileNames
    }

    "traverse and filter a directory of files" in {
      val directorySource =
        new DirectorySource(testSourceDir, Some(_.getFileName.toString.endsWith(".sql")))
      val fileNames = directorySource.map(_.filename).toSeq
      val expectedFileNames = Seq("test_1.sql", "test_2.sql", "test_3.sql")
      fileNames should contain theSameElementsAs expectedFileNames
    }

    "retrieve source code successfully from files" in {
      val directorySource =
        new DirectorySource(testSourceDir, Some(_.getFileName.toString.endsWith(".sql")))
      val sources = directorySource.map(_.source).toSeq
      sources should not be empty
      sources.foreach { source =>
        source should not be empty
      }
    }
  }
}
