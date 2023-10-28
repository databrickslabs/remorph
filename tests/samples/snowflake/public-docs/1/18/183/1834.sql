-- Create a task which defines and then uses configuration
CREATE OR REPLACE TASK root_task_with_config
WAREHOUSE=mywarehouse
SCHEDULE='10 m'
CONFIG=$${"output_dir": "/temp/test_directory/", "learning_rate": 0.1}$$
AS
BEGIN
  LET OUTPUT_DIR STRING := SYSTEM$GET_TASK_GRAPH_CONFIG('output_directory')::string;
  LET LEARNING_RATE DECIMAL := SYSTEM$GET_TASK_GRAPH_CONFIG('learning_rate:v1')::DECIMAL;
      ...
END;