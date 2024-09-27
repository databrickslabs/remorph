package com.databricks.labs.remorph.coverage.estimation

import com.databricks.labs.remorph.coverage.EstimationReport
import upickle.default._

import java.time.Instant

trait EstimationReporter {
  def report(): Unit
}

class ConsoleEstimationReporter(estimate: EstimationReport) extends EstimationReporter {
  override def report(): Unit = {
    // scalastyle:off println
    println(s"Sample size              : ${estimate.sampleSize}")
    println(s"Output record count      : ${estimate.records.size}")
    println(s"Unique successful parses : ${estimate.uniqueSuccesses}")
    println(s"Parse failures           : ${estimate.parseFailures}")
    println(s"Transpile failures       : ${estimate.transpileFailures}")
    println(s"Overall complexity       : ${estimate.overallComplexity.complexity}")
    println()
    // scalastyle:on println
  }
}

class JsonEstimationReporter(outputDir: os.Path, preserveQueries: Boolean, estimate: EstimationReport)
    extends EstimationReporter {
  override def report(): Unit = {
    val now = Instant.now
    val queriesDir = outputDir / s"${now.getEpochSecond}" / "queries"
    os.makeDir.all(queriesDir)
    val resultPath = outputDir / s"${now.getEpochSecond}" / s"${estimate.dialect}.json"

    // Iterate over the records and modify the transpilationReport.query field
    var count = 0
    val newRecords = estimate.records.map { record =>
      if (preserveQueries) {
        val (queryFilePath, outputFilepath) = record.analysisReport.fingerprint match {
          case Some(fingerprint) =>
            (queriesDir / s"${fingerprint.fingerprint}.sql", queriesDir / s"${fingerprint.fingerprint}_transpiled.sql")
          case None =>
            count += 1
            (queriesDir / s"parse_fail_${count}.sql", null) // No output file for failed transpiles
        }
        os.write(queryFilePath, record.transpilationReport.query)
        record.transpilationReport.output match {
          case Some(output) =>
            os.write(outputFilepath, output)
            record.withQueries(queryFilePath.toString, Some(outputFilepath.toString))
          case None =>
            record.withQueries(queryFilePath.toString, None)
        }
      } else {
        record.withQueries("<redacted>", None)
      }
    }
    val newEstimate = estimate.withRecords(newRecords)
    val jsonReport: String = write(newEstimate, indent = 4)
    os.write(resultPath, jsonReport)
  }
}
