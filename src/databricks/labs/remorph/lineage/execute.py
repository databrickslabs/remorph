import datetime
import logging
from pathlib import Path

from databricks.labs.remorph.intermediate.dag import DAG
from databricks.labs.remorph.intermediate.root_tables import RootTableIdentifier

logger = logging.getLogger(__name__)


def generate_mermaid_code(dag: DAG, filename) -> None:
    mermaid_code = "flowchart TD\n"
    for node_name, node in dag.nodes.items():
        if node.parents:
            for parent in node.parents:
                mermaid_code += f"    {node_name.capitalize()} --> {parent.name.capitalize()}\n"
        else:
            # Include nodes without parents to ensure they appear in the diagram
            mermaid_code += f"    {node_name.capitalize()}\n"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(mermaid_code)


def lineage_generator(source: str, input_sql: str, output_folder: str):
    input_sql = Path(input_sql)
    output_folder = output_folder if output_folder.endswith('/') else output_folder + '/'
    if input_sql.is_file() or input_sql.is_dir():

        root_table_identifier = RootTableIdentifier(source, input_sql)
        generated_dag = root_table_identifier.generate_lineage()
        date_str = datetime.datetime.now().strftime("%d%m%y")
        output_filename = f"{output_folder}lineage_{date_str}.cot"
        logger.info(f'Writing the COT file to {output_filename}')

        generate_mermaid_code(generated_dag, output_filename)

    else:
        msg = f"{input_sql} does not exist."
        logger.error(msg)
        raise FileNotFoundError(msg)
