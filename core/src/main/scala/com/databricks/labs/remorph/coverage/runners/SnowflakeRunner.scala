package com.databricks.labs.remorph.coverage.runners

import net.snowflake.client.jdbc.internal.org.bouncycastle.jce.provider.BouncyCastleProvider

import java.security.spec.PKCS8EncodedKeySpec
import java.security.{KeyFactory, PrivateKey, Security}
import java.sql.DriverManager
import java.util.{Base64, Properties}

class SnowflakeRunner(env: EnvGetter) {
  // scalastyle:off
  Class.forName("net.snowflake.client.jdbc.SnowflakeDriver")
  // scalastyle:on

  private[this] val url = env.get("TEST_SNOWFLAKE_JDBC")
  private[this] val privateKeyPEM = env.get("TEST_SNOWFLAKE_PRIVATE_KEY")

  private def privateKey: PrivateKey = {
    Security.addProvider(new BouncyCastleProvider())
    val keySpecPKCS8 = new PKCS8EncodedKeySpec(
      Base64.getDecoder.decode(
        privateKeyPEM
          .split("\n")
          .drop(1)
          .dropRight(1)
          .mkString))
    val kf = KeyFactory.getInstance("RSA")
    kf.generatePrivate(keySpecPKCS8)
  }

  private[this] val props = {
    val p = new Properties()
    p.put("privateKey", privateKey)
    p
  }
  private[this] val connection = DriverManager.getConnection(url, props)
  private[this] val dumper = new CsvDumper(connection)

  def queryToCSV(query: String): String = dumper.queryToCSV(query)

  def close() {
    connection.close()
  }
}
