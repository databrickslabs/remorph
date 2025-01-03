package com.databricks.labs.remorph.coverage.estimation

import com.databricks.labs.remorph.coverage.{EstimationReport, EstimationReportEncoders}
import io.circe.syntax._

trait EstimationReporter {
  def report(): Unit
}

class SummaryEstimationReporter(outputDir: os.Path, estimate: EstimationReport) extends EstimationReporter {
  override def report(): Unit = {
    val ruleFrequency = estimate.overallComplexity.pfStats.ruleNameCounts.toSeq
      .sortBy(-_._2) // Sort by count in ascending order
      .map { case (ruleName, count) => s"| $ruleName | $count |\n" }
      .mkString
    val tokenFrequency = estimate.overallComplexity.pfStats.tokenNameCounts.toSeq
      .sortBy(-_._2) // Sort by count in ascending order
      .map { case (tokenName, count) => s"| $tokenName | $count |\n" }
      .mkString

    val output =
      s"""
         |# Conversion Complexity Estimation Report
         |## Report explanation:
         |
         |### Sample size
         |The number of records used to provide estimate. In other words the total
         |number of records in the input dataset.
         |### Output record count
         |The number of records generated to track output. This includes
         |both successful and failed transpilations, but the analysis tries
         |to avoid duplicates in both successful and failed transpilations.
         |### Unique successful transpiles
         |The number of unique queries that were successfully transpiled
         |from source dialect to Databricks SQL. This count does not include
         |queries that were duplicates of previously seen queries with just
         |simple parameter changes.
         |### Unique Parse failures
         |The number of unique queries that failed to parse and therefore
         |could not produce IR or be transpiled.
         |### Transpile failures
         |The number of unique queries that were parsed, produced an IR Plan,
         |but then failed to transpile to Databricks SQL. Note that this means
         |that there is a bug in either the IR generation or the source generation.
         |### Overall complexity
         |The overall complexity of the queries in the dataset. This is a rough
         |estimate of how difficult it will be to complete a port of system
         |if the supplied queries are representative of the source system.
         |
         |This can be somewhat subjective in that a query that is very complex in terms
         |of the number of statements or the number of joins may not be as complex as
         |it appears to be. However, it is a good starting point for understanding the
         |scope.
         |
         |### Statistics used to calculate overall complexity
         |While complexity is presented as one of four categories, being, *LOW*, *MEDIUM*,
         |*COMPLEX*, and *VERY_COMPLEX*, the actual judgement is based on a numeric score
         |calculated from the presence of various elements in the query. A low score
         |results in a complexity of *LOW* and a high score results in a complexity of *VERY_COMPLEX*.
         |
         |The individual scores for each query are then used to calculate the mean, median, and other
         |statistics that may be used to determine the overall complexity. The raw values are
         |contained in the report so that different interpretations can be made than the ones
         |provided by the current version of the estimate command.
         |
         |## Metrics
         | | Metric                      | Value                          |
         | |:----------------------------|--------------------------------:|
         | | Sample size                 | ${f"${estimate.sampleSize}%,d"}|
         | | Output record count         | ${f"${estimate.records.size}%,d"}|
         | | Unique successful transpiles| ${estimate.uniqueSuccesses}   |
         | | Unique Parse failures       | ${estimate.parseFailures}      |
         | | Transpile failures          | ${estimate.transpileFailures}  |
         | | Overall complexity (ALL)    | ${estimate.overallComplexity.allStats.complexity} |
         | | Overall complexity (SUCCESS)| ${estimate.overallComplexity.successStats.complexity} |
         |
         |## Failing Parser Rule and Failed Token Frequencies
         | This table shows the top N ANTLR grammar rules where parsing errors occurred and therefore
         | where spent in improving the parser will have the most impact. It should be used as a starting
         | point as these counts may include many instances of the same error. So fixing one parsing problem
         | may rid you of a large number of failing queries.
         |
         | | Rule Name                   | Frequency                      |
         | |:----------------------------|--------------------------------:|
         | $ruleFrequency
         |
         | This table is less useful than the rule table but it may be useful to see if there might be
         | a missing token definition or a token that is a keyword but not bing allowed as an identifier etc.
         |
         | | Token Name                  | Frequency                      |
         | |:----------------------------|--------------------------------:|
         | $tokenFrequency
         |
         |## Statistics used to calculate overall complexity (ALL results)
         |
         | | Metric                      | Value                          |
         | |:----------------------------|--------------------------------:|
         | | Mean score | ${f"${estimate.overallComplexity.allStats.meanScore}%,.2f"}|
         | | Standard deviation | ${f"${estimate.overallComplexity.allStats.stdDeviation}%,.2f"}|
         | | Mode score | ${estimate.overallComplexity.allStats.modeScore}|
         | | Median score | ${estimate.overallComplexity.allStats.medianScore}|
         | | Percentile 25 | ${f"${estimate.overallComplexity.allStats.percentile25}%,.2f"}|
         | | Percentile 50 | ${f"${estimate.overallComplexity.allStats.percentile50}%,.2f"}|
         | | Percentile 75 | ${f"${estimate.overallComplexity.allStats.percentile75}%,.2f"}|
         | | Geometric mean score | ${f"${estimate.overallComplexity.allStats.geometricMeanScore}%,.2f"}|
         |
         |## Statistics used to calculate overall complexity (Successful results only)
         |
         | | Metric                      | Value                          |
         | |:----------------------------|--------------------------------:|
         | | Mean score | ${f"${estimate.overallComplexity.successStats.meanScore}%,.2f"}|
         | | Standard deviation | ${f"${estimate.overallComplexity.successStats.stdDeviation}%,.2f"}|
         | | Mode score | ${estimate.overallComplexity.successStats.modeScore}|
         | | Median score | ${estimate.overallComplexity.successStats.medianScore}|
         | | Percentile 25 | ${f"${estimate.overallComplexity.successStats.percentile25}%,.2f"}|
         | | Percentile 50 | ${f"${estimate.overallComplexity.successStats.percentile50}%,.2f"}|
         | | Percentile 75 | ${f"${estimate.overallComplexity.successStats.percentile75}%,.2f"}|
         | | Geometric mean score | ${f"${estimate.overallComplexity.successStats.geometricMeanScore}%,.2f"}|
         |""".stripMargin

    val summaryFilePath = outputDir / "summary.md"
    os.write(summaryFilePath, output)
    // scalastyle:off println
    println(s"Summary report written to ${summaryFilePath}")
    // scalastyle:on println
  }
}

class JsonEstimationReporter(outputDir: os.Path, preserveQueries: Boolean, estimate: EstimationReport)
    extends EstimationReporter
    with EstimationReportEncoders {
  override def report(): Unit = {
    val queriesDir = outputDir / "queries"
    os.makeDir.all(queriesDir)
    val resultPath = outputDir / s"${estimate.dialect}.json"

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
    val jsonReport: String = newEstimate.asJson.spaces4
    os.write(resultPath, jsonReport)
  }
}
