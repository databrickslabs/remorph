import datetime
import logging
from pathlib import Path

from databricks.labs.remorph.intermediate.dag import DAG
from databricks.labs.remorph.intermediate.root_tables import RootTableIdentifier

logger = logging.getLogger(__name__)


def generate_cot_file(dag: DAG) -> str:
    lineage_str = "flowchart TD\n"
    for node_name, node in dag.nodes.items():
        if node.parents:
            for parent in node.parents:
                lineage_str += f"    {node_name.capitalize()} --> {parent.name.capitalize()}\n"
        else:
            # Include nodes without parents to ensure they appear in the diagram
            lineage_str += f"    {node_name.capitalize()}\n"
    return lineage_str


def write_lineage_file(output_folder, lineage_file_content) -> None:
    date_str = datetime.datetime.now().strftime("%d%m%y")
    output_filename = f"{output_folder}lineage_{date_str}.cot"
    logger.info(f'Writing the lineage to: {output_filename}')

    if Path(output_filename).exists():
        logger.warning(f'The output file exists. It will be replaced: {output_filename}')

    with open(output_filename, 'w', encoding='utf-8') as f:
        f.write(lineage_file_content)

    logger.info(f'The lineage is written to : {output_filename}')


def lineage_generator(source: str, input_sql: str, output_folder: str):
    input_sql = Path(input_sql)
    output_folder = output_folder if output_folder.endswith('/') else output_folder + '/'
    if input_sql.is_file() or input_sql.is_dir():
        msg = f"Processing for SQLs at this location: {input_sql}"
        logger.info(msg)
        root_table_identifier = RootTableIdentifier(source, input_sql)
        generated_dag = root_table_identifier.generate_lineage()
        lineage_file_content = generate_cot_file(generated_dag)
        write_lineage_file(output_folder, lineage_file_content)

    else:
        msg = f"{input_sql} does not exist."
        logger.error(msg)
        raise FileNotFoundError(msg)
