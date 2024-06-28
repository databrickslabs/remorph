# Databricks notebook source
# MAGIC %md
# MAGIC # Reconiliation Config Examples

# COMMAND ----------

# MAGIC %md
# MAGIC ### Source Table
# MAGIC | p_id | p_name | price | discount | offer | creation_date |
# MAGIC |------|--------|-------|----------|-------|---------------|
# MAGIC | 1 | 'p-1' | 1000 | 1.5 | 1.010 | 2000-01-01 |
# MAGIC | 2 | 'p-2' | 2000 | 7.0155 | 0.105 | 2000-02-02 |
# MAGIC | 3 | 'p-3' | 3000 | 1.01435 | 1.052 | 2000-03-03 |
# MAGIC | 4 | 'p-4' | 4000 | 4.0 | 4.0 | 2000-05-05 |
# MAGIC
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ### Target Table
# MAGIC | product_id | product_name | price | discount | offer | creation_date |
# MAGIC |------|--------|-------|----------|-------|---------------|
# MAGIC | 1 | 'p-1' | 1000 | 1.5 | 1.010 | 2000-01-01T01:00:00.000+00:00 |
# MAGIC | 2 | 'p-2' | 2050 | 7.0160 | 0.106 | 2000-01-01T01:00:00.000+00:00 |
# MAGIC | 3 | 'p-3' | 3100 | 2.01435 | 1.057 | 2000-01-01T01:00:00.000+00:00 |
# MAGIC | 5 | 'p-5' | 5000 | 5.0 | 5.0 | 2000-01-01T01:00:00.000+00:00 |
# MAGIC
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ### Data Overview
# MAGIC
# MAGIC | Record Type | Count | Comment |
# MAGIC | ---------------- | ----- | ------- |
# MAGIC | Match Records | 1 | **p_id=1** |
# MAGIC | Mismatch Records | 2 | **p_id=2 and p_id=3** |
# MAGIC | Missing Records in src | 1 | **p_id 5 is not in src** |
# MAGIC | Missing Records in tgt | 1 | **p_id 4 is not in tgt** |

# COMMAND ----------

# MAGIC %md
# MAGIC ## Run with Basic Config and Column Mapping
# MAGIC
# MAGIC ```
# MAGIC {
# MAGIC   "source_catalog": "source_catalog",
# MAGIC   "source_schema": "source_schema",
# MAGIC   "target_catalog": "target_catalog",
# MAGIC   "target_schema": "target_schema",
# MAGIC   "tables": [
# MAGIC     {
# MAGIC       "source_name": "product",
# MAGIC       "target_name": "product",
# MAGIC       "join_columns": ["p_id"],
# MAGIC       "column_mapping": [
# MAGIC         {
# MAGIC           "source_name": "p_id",
# MAGIC           "target_name": "product_id"
# MAGIC         },
# MAGIC         {
# MAGIC           "source_name": "p_name",
# MAGIC           "target_name": "product_name"
# MAGIC         }
# MAGIC       ]
# MAGIC     }
# MAGIC   ]
# MAGIC }
# MAGIC ```

# COMMAND ----------

# MAGIC %md
# MAGIC ### Expected Result
# MAGIC
# MAGIC | Record Type | Count | Comment |
# MAGIC | ---------------- | ----- | ------- |
# MAGIC | Match Records | 0 | **no transformation for creation_date** |
# MAGIC | Mismatch Records | 3 | **p_id=1, p_id=2 and p_id=3** |
# MAGIC | Missing Records in src | 1 | **p_id 5 is not in src** |
# MAGIC | Missing Records in tgt | 1 | **p_id 4 is not in tgt** |

# COMMAND ----------

# MAGIC %md
# MAGIC ### Run with User Transformations
# MAGIC
# MAGIC ```
# MAGIC {
# MAGIC   "source_catalog": "source_catalog",
# MAGIC   "source_schema": "source_schema",
# MAGIC   "target_catalog": "target_catalog",
# MAGIC   "target_schema": "target_schema",
# MAGIC   "tables": [
# MAGIC     {
# MAGIC       "source_name": "product",
# MAGIC       "target_name": "product",
# MAGIC       "join_columns": ["p_id"],
# MAGIC       "column_mapping": [
# MAGIC         {
# MAGIC           "source_name": "p_id",
# MAGIC           "target_name": "product_id"
# MAGIC         },
# MAGIC         {
# MAGIC           "source_name": "p_name",
# MAGIC           "target_name": "product_name"
# MAGIC         }
# MAGIC       ]
# MAGIC     }
# MAGIC   ],
# MAGIC "transformations": [
# MAGIC         {
# MAGIC           "column_name": "creation_date",
# MAGIC           "source": "creation_date",
# MAGIC           "target": "to_date(creation_date,'yyyy-mm-dd')"
# MAGIC         },
# MAGIC  ]
# MAGIC }
# MAGIC ```

# COMMAND ----------

# MAGIC %md
# MAGIC ### Expected Result
# MAGIC
# MAGIC **one match because of user transformation applied on create_date**
# MAGIC | Record Type | Count | Comment |
# MAGIC | ---------------- | ----- | ------- |
# MAGIC | Match Records | 1 | **p_id=1** |
# MAGIC | Mismatch Records | 2 | **p_id=2 and p_id=3** |
# MAGIC | Missing Records in src | 1 | **p_id 4 is not in src** |
# MAGIC | Missing Records in tgt | 1 | **p_id 5 is not in tgt** |
# MAGIC
# MAGIC **Mismatch Fields:** price,discount,offer

# COMMAND ----------

# MAGIC %md
# MAGIC ### Run with Explicit Select
# MAGIC
# MAGIC
# MAGIC ```
# MAGIC {
# MAGIC   "source_catalog": "source_catalog",
# MAGIC   "source_schema": "source_schema",
# MAGIC   "target_catalog": "target_catalog",
# MAGIC   "target_schema": "target_schema",
# MAGIC   "tables": [
# MAGIC     {
# MAGIC       "source_name": "product",
# MAGIC       "target_name": "product",
# MAGIC       "select_columns":["p_id", "p_name"]
# MAGIC       "join_columns": ["p_id"],
# MAGIC       "column_mapping": [
# MAGIC         {
# MAGIC           "source_name": "p_id",
# MAGIC           "target_name": "product_id"
# MAGIC         },
# MAGIC         {
# MAGIC           "source_name": "p_name",
# MAGIC           "target_name": "product_name"
# MAGIC         }
# MAGIC       ]
# MAGIC     }
# MAGIC   ],
# MAGIC }
# MAGIC ```

# COMMAND ----------

# MAGIC %md
# MAGIC ### Expected Result
# MAGIC
# MAGIC **no mismatch becuase we are not considering mismatch columns in select**
# MAGIC | Record Type | Count | Comment |
# MAGIC | ---------------- | ----- | ------- |
# MAGIC | Match Records | 3 | **p_id=1, p_id=2 and p_id=3** |
# MAGIC | Mismatch Records | 0 |  |
# MAGIC | Missing Records in src | 1 | **p_id 4 is not in src** |
# MAGIC | Missing Records in tgt | 1 | **p_id 5 is not in tgt** |

# COMMAND ----------

# MAGIC %md
# MAGIC ### Run with Explicit Drop
# MAGIC
# MAGIC ```
# MAGIC {
# MAGIC   "source_catalog": "source_catalog",
# MAGIC   "source_schema": "source_schema",
# MAGIC   "target_catalog": "target_catalog",
# MAGIC   "target_schema": "target_schema",
# MAGIC   "tables": [
# MAGIC     {
# MAGIC       "source_name": "product",
# MAGIC       "target_name": "product",
# MAGIC       "drop_columns":["offer"]
# MAGIC       "join_columns": ["p_id"],
# MAGIC       "column_mapping": [
# MAGIC         {
# MAGIC           "source_name": "p_id",
# MAGIC           "target_name": "product_id"
# MAGIC         },
# MAGIC         {
# MAGIC           "source_name": "p_name",
# MAGIC           "target_name": "product_name"
# MAGIC         }
# MAGIC       ]
# MAGIC     }
# MAGIC   ],
# MAGIC   "transformations": [
# MAGIC         {
# MAGIC           "column_name": "creation_date",
# MAGIC           "source": "creation_date",
# MAGIC           "target": "to_date(creation_date,'yyyy-mm-dd')"
# MAGIC         },
# MAGIC  ]
# MAGIC }
# MAGIC ```

# COMMAND ----------

# MAGIC %md
# MAGIC ### <span style="color:red">Expected Result</span>
# MAGIC **offer field is dropped and considered in mismatch**
# MAGIC | Record Type | Count | Comment |
# MAGIC | ---------------- | ----- | ------- |
# MAGIC | Match Records | 1 | **p_id=1** |
# MAGIC | Mismatch Records | 2 | **p_id=2 and p_id=3** |
# MAGIC | Missing Records in src | 1 | **p_id 4 is not in src** |
# MAGIC | Missing Records in tgt | 1 | **p_id 5 is not in tgt** |
# MAGIC
# MAGIC **Mismatch Fields:** price,discount

# COMMAND ----------

# MAGIC %md
# MAGIC ### Run with filters
# MAGIC
# MAGIC ```
# MAGIC {
# MAGIC   "source_catalog": "source_catalog",
# MAGIC   "source_schema": "source_schema",
# MAGIC   "target_catalog": "target_catalog",
# MAGIC   "target_schema": "target_schema",
# MAGIC   "tables": [
# MAGIC     {
# MAGIC       "source_name": "product",
# MAGIC       "target_name": "product",
# MAGIC       "join_columns": ["p_id"],
# MAGIC       "column_mapping": [
# MAGIC         {
# MAGIC           "source_name": "p_id",
# MAGIC           "target_name": "product_id"
# MAGIC         },
# MAGIC         {
# MAGIC           "source_name": "p_name",
# MAGIC           "target_name": "product_name"
# MAGIC         }
# MAGIC       ]
# MAGIC     }
# MAGIC   ],
# MAGIC   "transformations": [
# MAGIC         {
# MAGIC           "column_name": "creation_date",
# MAGIC           "source": "creation_date",
# MAGIC           "target": "to_date(creation_date,'yyyy-mm-dd')"
# MAGIC         },
# MAGIC  ],
# MAGIC  "filters": {
# MAGIC   "source": "p_id = 1",
# MAGIC   "target": "product_id = 1"
# MAGIC  }
# MAGIC }
# MAGIC ```
# MAGIC
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ### Expected Result
# MAGIC
# MAGIC **no mismatch,as we are filtering only p_id=1**
# MAGIC | Record Type | Count | Comment |
# MAGIC | ---------------- | ----- | ------- |
# MAGIC | Match Records | 0 | **p_id=1** |
# MAGIC | Mismatch Records | 0 | |
# MAGIC | Missing Records in src | 0 | |
# MAGIC | Missing Records in tgt | 0 | |
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ### Run with Thresholds Comparison
# MAGIC Supported Comparison
# MAGIC
# MAGIC Percentage
# MAGIC Absolute
# MAGIC Dates/Timestamp
# MAGIC
# MAGIC ```
# MAGIC {
# MAGIC   "source_catalog": "source_catalog",
# MAGIC   "source_schema": "source_schema",
# MAGIC   "target_catalog": "target_catalog",
# MAGIC   "target_schema": "target_schema",
# MAGIC   "tables": [
# MAGIC     {
# MAGIC       "source_name": "product",
# MAGIC       "target_name": "product",
# MAGIC       "join_columns": ["p_id"],
# MAGIC       "column_mapping": [
# MAGIC         {
# MAGIC           "source_name": "p_id",
# MAGIC           "target_name": "product_id"
# MAGIC         },
# MAGIC         {
# MAGIC           "source_name": "p_name",
# MAGIC           "target_name": "product_name"
# MAGIC         }
# MAGIC       ]
# MAGIC     }
# MAGIC   ],
# MAGIC   "transformations": [
# MAGIC         {
# MAGIC           "column_name": "creation_date",
# MAGIC           "source": "creation_date",
# MAGIC           "target": "to_date(creation_date,'yyyy-mm-dd')"
# MAGIC         },
# MAGIC  ],
# MAGIC  "threshold": [
# MAGIC   {
# MAGIC     "column_name": "price",
# MAGIC     "upper_bound": "-50",
# MAGIC     "lower_bound": "50",
# MAGIC     "type"="float"
# MAGIC   },
# MAGIC     {
# MAGIC     "column_name": "discount",
# MAGIC     "upper_bound": "-20",
# MAGIC     "lower_bound": "20",
# MAGIC     "type"="float"
# MAGIC   },
# MAGIC     {
# MAGIC     "column_name": "offer",
# MAGIC     "upper_bound": "-5%",
# MAGIC     "lower_bound": "5%",
# MAGIC     "type"="float"
# MAGIC   }
# MAGIC  ]
# MAGIC }
# MAGIC ```

# COMMAND ----------

# MAGIC %md
# MAGIC ### Expected Result
# MAGIC
# MAGIC **1 mismatch,as we are applied threshold comparison which matches the p_id=2 columns as match**
# MAGIC | Record Type | Count | Comment |
# MAGIC | ---------------- | ----- | ------- |
# MAGIC | Match Records | 0 | **p_id=1 and pid=2** |
# MAGIC | Mismatch Records | 0 | |
# MAGIC | Missing Records in src | 1 |**p_id 4 is not in src** |
# MAGIC | Missing Records in tgt | 1 |**p_id 5 is not in tgt**|
# MAGIC | Threshold Mismatch | 1 |**p_id=3**|

# COMMAND ----------

# MAGIC %md
# MAGIC ### Run with JDBC Options

# COMMAND ----------

# MAGIC %md
# MAGIC ### JDBC Options
# MAGIC
# MAGIC Using JDBC Options we can parallelize the read from the source system using a key(**generally primary key**).
# MAGIC
# MAGIC
# MAGIC
# MAGIC ```
# MAGIC
# MAGIC {
# MAGIC   "source_catalog": "source_catalog",
# MAGIC   "source_schema": "source_schema",
# MAGIC   "target_catalog": "target_catalog",
# MAGIC   "target_schema": "target_schema",
# MAGIC   "tables": [
# MAGIC     {
# MAGIC       "source_name": "product",
# MAGIC       "target_name": "product",
# MAGIC       "join_columns": ["p_id"],
# MAGIC       "column_mapping": [
# MAGIC         {
# MAGIC           "source_name": "p_id",
# MAGIC           "target_name": "product_id"
# MAGIC         },
# MAGIC         {
# MAGIC           "source_name": "p_name",
# MAGIC           "target_name": "product_name"
# MAGIC         }
# MAGIC       ],
# MAGIC       "jdbc_reader_options": {
# MAGIC           "number_partitions": 10,
# MAGIC           "partition_column": "p_id",
# MAGIC           "lower_bound": "0",
# MAGIC           "upper_bound": "10000000"
# MAGIC       },
# MAGIC   ]
# MAGIC }
# MAGIC ```

# COMMAND ----------

# MAGIC %md
# MAGIC ### Run Without Joining Keys
# MAGIC
# MAGIC
# MAGIC ```
# MAGIC
# MAGIC
# MAGIC {
# MAGIC   "source_catalog": "source_catalog",
# MAGIC   "source_schema": "source_schema",
# MAGIC   "target_catalog": "target_catalog",
# MAGIC   "target_schema": "target_schema",
# MAGIC   "tables": [
# MAGIC     {
# MAGIC       "source_name": "product",
# MAGIC       "target_name": "product",
# MAGIC       "column_mapping": [
# MAGIC         {
# MAGIC           "source_name": "p_id",
# MAGIC           "target_name": "product_id"
# MAGIC         },
# MAGIC         {
# MAGIC           "source_name": "p_name",
# MAGIC           "target_name": "product_name"
# MAGIC         }
# MAGIC       ],
# MAGIC   ]
# MAGIC }
# MAGIC ```
# MAGIC
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ### Expected Result
# MAGIC
# MAGIC **reconciliation is done only at row level**
# MAGIC | Record Type | Count | Comment |
# MAGIC | ---------------- | ----- | ------- |
# MAGIC | Match Records | 0 | **p_id=1** |
# MAGIC | Mismatch Records | 0 | |
# MAGIC | Missing Records in src | 3 |**p_id=2, p_id=3,p_id 4 is not in src**|
# MAGIC | Missing Records in tgt | 3 |**p_id=2, p_id=3,p_id 5 is not in tgt** |

# COMMAND ----------

# MAGIC %md
# MAGIC ## Complex datatypes

# COMMAND ----------

# MAGIC %md
# MAGIC ### Source Data
# MAGIC
# MAGIC | p_id | 	array_col | map_col	 | struct_col	        | array_of_map            |
# MAGIC |------|------------|----------|--------------------|-------------------------|
# MAGIC | 1    | [3,2,1]    | {"a":1}  | {"f1":"a","f2":1}	 | [{"aa":"1"},{"ab":"2"}] |
# MAGIC | 2    | [6,5,4]    | {"b":2}  | {"f1":"b","f2":2}	 | [{"ba":"1"},{"bb":"2"}] |
# MAGIC | 3    | [7,9,8]    | {"c":3}  | {"f1":"c","f2":3}	 | [{"cb":"2"},{"ca":"1"}] |
# MAGIC | 5    | [57,58,59] | {"e":5}  | {"f1":"e","f2":5}	 | [{"db":"2"},{"da":"1"}] |

# COMMAND ----------

# MAGIC %md
# MAGIC ### Target Data
# MAGIC
# MAGIC | p_id | array_col  | map_col  | struct_col         | array_of_map            |
# MAGIC |------|------------|----------|--------------------|-------------------------|
# MAGIC | 1    | [1,2,3]    | {"a":1}  | {"f1":"a","f2":1}  | [{"aa":"1"},{"ab":"2"}] |
# MAGIC | 2    | [4,5,6]    | {"b":2}  | {"f1":"bb","f2":2} | [{"bb":"1"},{"ba":"2"}] |
# MAGIC | 3    | [7,8,9]    | {"c":34} | {"f1":"c","f2":3}  | [{"ca":"1"},{"cb":"2"}] |
# MAGIC | 4    | [47,48,49] | {"d":4}  | {"f1":"d","f2":4}  | [{"da":"1"},{"db":"2"}] |

# COMMAND ----------

# MAGIC %md
# MAGIC ### Run with Complex Data Types
# MAGIC
# MAGIC ```
# MAGIC
# MAGIC {
# MAGIC   "source_catalog": "source_catalog",
# MAGIC   "source_schema": "source_schema",
# MAGIC   "target_catalog": "target_catalog",
# MAGIC   "target_schema": "target_schema",
# MAGIC   "tables": [
# MAGIC     {
# MAGIC       "source_name": "product",
# MAGIC       "target_name": "product",
# MAGIC       "join_columns": ["p_id"],
# MAGIC       "transformations": [
# MAGIC         {
# MAGIC           "column_name": "map_col",
# MAGIC           "source": "cast(to_json(map_col) as string)",
# MAGIC           "target": "cast(to_json(map_col) as string)"
# MAGIC         },
# MAGIC         {
# MAGIC           "column_name": "struct_col",
# MAGIC           "source": "cast(to_json(struct_col) as string)",
# MAGIC           "target": "cast(to_json(struct_col) as string)"
# MAGIC         },
# MAGIC         {
# MAGIC           "column_name": "array_col",
# MAGIC           "source": "concat_ws(',', sort_array(array_col))",
# MAGIC           "target": "concat_ws(',', sort_array(array_col))"
# MAGIC         },
# MAGIC  ]
# MAGIC   ]
# MAGIC }
# MAGIC ```

# COMMAND ----------

# MAGIC %md
# MAGIC ### Expected Result
# MAGIC
# MAGIC | Record Type | Count | Comment |
# MAGIC | ---------------- | ----- | ------- |
# MAGIC | Match Records | 1 | **p_id=1** |
# MAGIC | Mismatch Records | 2 | **p_id=2 and p_id=3** |
# MAGIC | Missing Records in src | 1 | **p_id 4 is not in src** |
# MAGIC | Missing Records in tgt | 1 | **p_id 5 is not in tgt** |
# MAGIC
# MAGIC **array_of_map is not included in the reconciliation**

# COMMAND ----------

# MAGIC %md
# MAGIC ## UDF Support
# MAGIC
# MAGIC ### Note: sort_array_of_map_string_int is a user-defined function.You can create your own user-defined function for complex transformations and use it in the same way as below:
# MAGIC
# MAGIC ```
# MAGIC
# MAGIC {
# MAGIC   "source_catalog": "source_catalog",
# MAGIC   "source_schema": "source_schema",
# MAGIC   "target_catalog": "target_catalog",
# MAGIC   "target_schema": "target_schema",
# MAGIC   "tables": [
# MAGIC     {
# MAGIC       "source_name": "product",
# MAGIC       "target_name": "product",
# MAGIC       "select_columns":["p_id","array_of_map"],
# MAGIC       "join_columns": ["p_id"],
# MAGIC       "transformations": [
# MAGIC         {
# MAGIC           "column_name": "array_of_map",
# MAGIC           "source": "sort_array_of_map_string_int(array_of_map)",
# MAGIC           "target": "sort_array_of_map_string_int(array_of_map)"
# MAGIC         },
# MAGIC  ]
# MAGIC   ]
# MAGIC }
# MAGIC ```
