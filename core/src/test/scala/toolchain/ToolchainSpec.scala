package toolchain.testsource

import com.databricks.labs.remorph.toolchain.DirectorySource
import org.scalatest.matchers.should.Matchers
import org.scalatest.wordspec.AnyWordSpec

class ToolchainSpec extends AnyWordSpec with Matchers {
  "Toolchain" should {
    "traverse a directory of files" in {
      val directorySourceWithoutFilter = new DirectorySource("core/src/test/scala/toolchain/testsource")
      val fileNames = directorySourceWithoutFilter.map(_.filename).toSeq
      val expectedFileNames = Seq("test_1.sql", "test_2.sql", "test_3.sql", "not_sql.md")
      fileNames should contain theSameElementsAs expectedFileNames
    }

    "traverse and filter a directory of files" in {
      val directorySource =
        new DirectorySource("core/src/test/scala/toolchain/testsource", Some(_.getFileName.toString.endsWith(".sql")))
      val fileNames = directorySource.map(_.filename).toSeq
      val expectedFileNames = Seq("test_1.sql", "test_2.sql", "test_3.sql")
      fileNames should contain theSameElementsAs expectedFileNames
    }

    "retrieve source code successfully from files" in {
      val directorySource =
        new DirectorySource("core/src/test/scala/toolchain/testsource", Some(_.getFileName.toString.endsWith(".sql")))
      val sources = directorySource.map(_.source).toSeq
      sources should not be empty
      sources.foreach { source =>
        source should not be empty
      }
    }
  }
}
