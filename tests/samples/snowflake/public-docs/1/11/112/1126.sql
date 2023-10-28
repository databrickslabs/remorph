-- Create a table to store the file metadata

  CREATE TABLE images_table
  (
      file_url string,
      image_format string,
      dimensions_X number,
      dimensions_Y number,
      tags array,
      dominant_color string,
      relative_path string
  );

-- Load the metadata from the JSON document into the table.

COPY INTO images_table
  FROM
  (SELECT $1:file_url::STRING, $1:image_format::STRING, $1:size::NUMBER, $1:tags, $1:dominant_color::STRING, GET_RELATIVE_PATH(@images_stage, $1:file_url)
  FROM
  @images_stage/image_metadata.json)
  FILE_FORMAT = (type = json);

-- Create a view that queries the pre-signed URL for an image as well as the image metadata stored in a table.
CREATE VIEW image_catalog AS
(
  SELECT
   size,
   get_presigned_url(@images_stage, relative_path) AS presigned_url,
   tags
  FROM
    images_table
);