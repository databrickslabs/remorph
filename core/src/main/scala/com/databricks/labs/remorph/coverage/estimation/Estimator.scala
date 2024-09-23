package com.databricks.labs.remorph.coverage.estimation

import com.typesafe.scalalogging.LazyLogging
import os.Path


class Estimator extends LazyLogging{

  def run(outputDir: Path, dialect: String): Unit = {

    logger.info(s"Estimating coverage for $dialect with output to $outputDir")
  }
}
