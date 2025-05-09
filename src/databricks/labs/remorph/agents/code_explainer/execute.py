import pprint
import logging

from databricks.labs.remorph.agents.code_explainer.parser import SqlParser
from databricks.labs.remorph.agents.code_explainer.explainer import SQLExplainer
from databricks.labs.remorph.agents.code_explainer.intent import CompareIntent

logger = logging.getLogger(__name__)


def _run(source_doc: str, target_doc: str = '', compare_intent: bool = False, format_flag: bool = False) -> None:
    """Run the SQL Explainer"""
    # Set the experiment

    source_documents = SqlParser(source_doc).parse()

    if not source_documents:
        logger.warning("No code found in the source document.")
        print("[WARN]::No code found in the source document.")
        return

    target_documents = SqlParser(target_doc).parse() if compare_intent else None

    # print("Number of documents: ", len(docs))

    explainer = SQLExplainer(endpoint_name="databricks-llama-4-maverick", format_flag=format_flag)
    source_explanations = explainer.explain_documents(source_documents)
    target_explanations = explainer.explain_documents(target_documents) if target_documents else []

    if source_explanations:
        print("****" * 50)
        print("Source SQL Code Explanation:")
        pprint.pprint(source_explanations[0].get('explanation', "__NOT_FOUND__"))

    if not target_documents:
        return

    if target_explanations:
        print("****" * 50)
        print("Target SQL Code Explanation:")
        pprint.pprint(target_explanations[0].get('explanation', "__NOT_FOUND__"))

    if source_explanations and target_explanations:
        print("****" * 50)
        print("Comparing Code intent of Source SQL and converted ")

        intent_compare = CompareIntent(
            source_intent=source_explanations[0].get('explanation', {}),
            target_intent=target_explanations[0].get('explanation', {}),
            endpoint_name="databricks-claude-3-7-sonnet",
        )

        print("****" * 50)
        print(intent_compare.compare())


def intent(source_doc: str):
    _run(source_doc=source_doc, compare_intent=False, format_flag=False)


def match_intent(source_doc: str, target_doc: str):
    _run(source_doc=source_doc, target_doc=target_doc, compare_intent=True, format_flag=True)
