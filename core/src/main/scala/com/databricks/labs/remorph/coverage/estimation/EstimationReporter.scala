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
    os.makeDir.all(outputDir)
    val resultPath = outputDir / s"${estimate.dialect}_${now.getEpochSecond}.json"
    val jsonReport: String = write(estimate, indent = 4)
    os.write(resultPath, jsonReport)
  }
}
