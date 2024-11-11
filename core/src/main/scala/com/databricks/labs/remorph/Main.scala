package com.databricks.labs.remorph

import com.databricks.labs.remorph.generators.orchestration.rules.history.RawMigration
import io.circe.{Decoder, jackson}
import io.circe.generic.semiauto._

import java.io.File

case class Payload(command: String, flags: Map[String, String])

object Payload {
  implicit val payloadDecoder: Decoder[Payload] = deriveDecoder
}

object Main extends App with ApplicationContext {
  // scalastyle:off println
  route match {
    case Payload("debug-script", args) =>
      exampleDebugger.debugExample(args("name"))
    case Payload("debug-me", _) =>
      prettyPrinter(workspaceClient.currentUser().me())
    case Payload("debug-coverage", args) =>
      coverageTest.run(os.Path(args("src")), os.Path(args("dst")), args("extractor"))
    case Payload("debug-estimate", args) =>
      val report = estimator.run()
      jsonEstimationReporter(
        os.Path(args("dst")) / s"${now.getEpochSecond}",
        args.get("preserve-queries").exists(_.toBoolean),
        report).report()
      args("console-output") match {
        case "true" => consoleEstimationReporter(os.Path(args("dst")) / s"${now.getEpochSecond}", report).report()
      }
    case Payload("debug-bundle", args) =>
      val dst = new File(args("dst"))
      val queryHistory = queryHistoryProvider.history()
      fileSetGenerator.generate(RawMigration(queryHistory)).runAndDiscardState(Init) match {
        case OkResult(output) => output.persist(dst)
        case PartialResult(output, error) =>
          prettyPrinter(error)
          output.persist(dst)
        case nok: KoResult =>
          prettyPrinter(nok)
      }
    case Payload(command, _) =>
      println(s"Unknown command: $command")
  }

  // make CLI flags available for ApplicationContext
  def flags: Map[String, String] = cliFlags

  // placeholder for global CLI flags
  private var cliFlags: Map[String, String] = Map.empty

  // parse json from the last CLI argument
  private def route: Payload = {
    val payload = jackson.decode[Payload](args.last).right.get
    cliFlags = payload.flags
    payload
  }
}
