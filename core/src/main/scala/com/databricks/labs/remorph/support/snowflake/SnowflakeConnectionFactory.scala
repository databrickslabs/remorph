package com.databricks.labs.remorph.support.snowflake

import com.databricks.labs.remorph.coverage.runners.EnvGetter
import com.databricks.labs.remorph.support.ConnectionFactory
import net.snowflake.client.jdbc.internal.org.bouncycastle.jce.provider.BouncyCastleProvider

import java.security.spec.PKCS8EncodedKeySpec
import java.security.{KeyFactory, PrivateKey, Security}
import java.sql.{Connection, DriverManager}
import java.util.{Base64, Properties}

// TODO: This is not how we will handle connections in the future

class SnowflakeConnectionFactory(env: EnvGetter) extends ConnectionFactory {
  // scalastyle:off
  Class.forName("net.snowflake.client.jdbc.SnowflakeDriver")
  // scalastyle:on

  private val url = env.get("TEST_SNOWFLAKE_JDBC")
  private val privateKeyPEM = env.get("TEST_SNOWFLAKE_PRIVATE_KEY")

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

  private val props = new Properties()
  props.put("privateKey", privateKey)

  def newConnection(): Connection = DriverManager.getConnection(url, props)
}
