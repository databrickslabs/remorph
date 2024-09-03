package com.databricks.labs.remorph.connections

import com.databricks.labs.remorph.utils.Strings
import com.typesafe.scalalogging.LazyLogging
import org.scalatest.exceptions.TestCanceledException

import java.io.{File, FileNotFoundException}

class EnvGetter extends LazyLogging {
  private val env = getDebugEnv

  def get(key: String): String = env.getOrElse(key, throw new TestCanceledException(s"not in env: $key", 3))

  private def getDebugEnv: Map[String, String] = {
    try {
      val debugEnvFile = String.format("%s/.databricks/debug-env.json", System.getProperty("user.home"))
      val contents = Strings.fileToString(new File(debugEnvFile))
      logger.debug(s"Found debug env file: $debugEnvFile")

      val raw = ujson.read(contents).obj
      val ucws = raw("ucws").obj.mapValues(_.str).toMap
      ucws
    } catch {
      case _: FileNotFoundException => sys.env
    }
  }
}
