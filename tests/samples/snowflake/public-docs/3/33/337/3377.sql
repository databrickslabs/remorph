// build connection properties
Properties properties = new Properties();

// Required connection properties
properties.put("user"    ,  "jsmith"      );
properties.put("password",  "mypassword");
properties.put("account" ,  "myaccount");

// Set some additional variables.
properties.put("$variable_1", "some example");
properties.put("$variable_2", "1"           );

// create a new connection
String connectStr = "jdbc:snowflake://localhost:8080";

// Open a connection under the snowflake account and enable variable support
Connection con = DriverManager.getConnection(connectStr, properties);