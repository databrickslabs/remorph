-- Create a table that stores the relative file path for each staged file along with any other related data.
CREATE TABLE acct_table (
  acct_name string,
  relative_file_path string
);

-- Create a secure view on the table you created.
-- A role that has the SELECT privilege on the secure view has scoped access to the filtered set of files that include the acct1 text string.
CREATE SECURE VIEW acct1_files
AS
  SELECT BUILD_SCOPED_FILE_URL(@acct_files, relative_file_path) scoped_url
  FROM acct_table
  WHERE acct_name = 'acct1';