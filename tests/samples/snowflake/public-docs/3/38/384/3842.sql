SELECT
    v.$1, v.$2, ...
  FROM
    @my_stage( FILE_FORMAT => 'csv_format', PATTERN => '.*my_pattern.*') v;