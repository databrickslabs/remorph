package com.databricks.labs.remorph.coverage.runners

import com.databricks.labs.remorph.utils.Strings
import com.fasterxml.jackson.databind.{DeserializationFeature, ObjectMapper}
import com.fasterxml.jackson.module.scala.DefaultScalaModule
import com.fasterxml.jackson.module.scala.ClassTagExtensions
import com.typesafe.scalalogging.LazyLogging

import java.io.{File, FileNotFoundException}

case class DebugEnv(ucws: Map[String, String])

class EnvGetter extends LazyLogging {
  private val env = getDebugEnv()

  def get(key: String): String = env.getOrElse(key, throw new RuntimeException(s"not in env: $key"))

  private def getDebugEnv(): Map[String, String] = {
    try {
      val debugEnvFile = String.format("%s/.databricks/debug-env.json", System.getProperty("user.home"))
      val contents = Strings.fileToString(new File(debugEnvFile))
      logger.debug(s"Found debug env file: $debugEnvFile")
      val mapper = new ObjectMapper() with ClassTagExtensions
      mapper.configure(DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES, false)
      mapper.registerModule(DefaultScalaModule)
      val envs = mapper.readValue[DebugEnv](contents)
      envs.ucws
    } catch {
      case _: FileNotFoundException => sys.env
    }
  }
}