-- see https://docs.snowflake.com/en/sql-reference/identifier-literal

String sql_command;

// Create a Statement object to use later.
System.out.println("Create JDBC statement.");
Statement statement = connection.createStatement();
System.out.println("Create function.");
sql_command = "CREATE FUNCTION speed_of_light() RETURNS INTEGER AS $$ 299792458 $$";
statement.execute(sql_command);

System.out.println("Create prepared statement.");
sql_command = "SELECT IDENTIFIER(?)()";
PreparedStatement ps = connection.prepareStatement(sql_command);
// Bind
ps.setString(1, "speed_of_light");
ResultSet rs = ps.executeQuery();
if (rs.next()) {
  System.out.println("Speed of light (m/s) = " + rs.getInt(1));
}