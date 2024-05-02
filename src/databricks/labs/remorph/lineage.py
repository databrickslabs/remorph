import datetime
import logging
from pathlib import Path

from databricks.labs.remorph.intermediate.dag import DAG
from databricks.labs.remorph.intermediate.root_tables import RootTableIdentifier

logger = logging.getLogger(__name__)


def _generate_dot_file_contents(dag: DAG) -> str:
    _lineage_str = "flowchart TD\n"
    for node_name, node in dag.nodes.items():
        if node.parents:
            for parent in node.parents:
                _lineage_str += f"    {node_name.capitalize()} --> {parent.capitalize()}\n"
        else:
            # Include nodes without parents to ensure they appear in the diagram
            _lineage_str += f"    {node_name.capitalize()}\n"
    return _lineage_str


def lineage_generator(source: str, input_sql: str, output_folder: str):
    input_sql_path = Path(input_sql)
    output_folder = output_folder if output_folder.endswith('/') else output_folder + '/'

    msg = f"Processing for SQLs at this location: {input_sql_path}"
    logger.info(msg)
    root_table_identifier = RootTableIdentifier(source, input_sql_path)
    generated_dag = root_table_identifier.generate_lineage()
    lineage_file_content = _generate_dot_file_contents(generated_dag)

    date_str = datetime.datetime.now().strftime("%d%m%y")

    output_filename = Path(f"{output_folder}lineage_{date_str}.dot")
    if output_filename.exists():
        logger.warning(f'The output file already exists and will be replaced: {output_filename}')
    logger.info(f"Attempting to write the lineage to {output_filename}")
    with output_filename.open('w', encoding='utf-8') as f:
        f.write(lineage_file_content)
    logger.info(f"Succeeded to write the lineage to {output_filename}")
