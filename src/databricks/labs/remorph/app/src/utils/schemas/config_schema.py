from pyspark.sql.types import StructType, StructField, StringType, ArrayType, IntegerType, MapType

# Define the schema for the transformations array
transformations_schema = ArrayType(
    StructType(
        [
            StructField("column_name", StringType(), True),
            StructField("source", StringType(), True),
            StructField("target", StringType(), True),
        ]
    )
)

# Define the schema for the tables array
tables_schema = ArrayType(
    StructType(
        [
            StructField("source_name", StringType(), True),
            StructField("target_name", StringType(), True),
            StructField("drop_columns", ArrayType(StringType()), True),
            StructField("join_columns", ArrayType(StringType()), True),
            StructField("transformations", transformations_schema, True),
            StructField("jdbc_reader_options", MapType(StringType(), StringType()), True),
        ]
    )
)

# Define the overall schema
config_schema = StructType(
    [
        StructField("config_id", IntegerType(), False),
        StructField("source_catalog", StringType(), False),
        StructField("source_schema", StringType(), False),
        StructField("target_catalog", StringType(), False),
        StructField("target_schema", StringType(), False),
        StructField("tables", tables_schema, False),
    ]
)
