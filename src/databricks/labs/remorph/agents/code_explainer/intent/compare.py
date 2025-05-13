import json
from typing import Any


from databricks_langchain import ChatDatabricks  # type: ignore
from langchain.prompts import ChatPromptTemplate


class CompareIntent:
    def __init__(
        self,
        source_intent: dict[str, Any],
        target_intent: dict[str, Any],
        endpoint_name: str = "databricks-llama-4-maverick",
    ):
        self.source_intent = source_intent
        self.target_intent = target_intent
        self.endpoint_name = endpoint_name
        # self.explainer = SQLExplainer(endpoint_name="databricks-llama-4-maverick", format_flag=True)

        """Initialize the SQL Explainer Chain"""
        self.llm = ChatDatabricks(endpoint=self.endpoint_name, extra_params={"temperature": 0.0})

        # Create the prompt template
        self.prompt_template = ChatPromptTemplate.from_template(
            """
        Analyze the following two JSON segments each containing the code intents of source and migrated target SQL code:

        Source SQL Intent:
        ```json
        {source_intent}
        ```

        Target SQL Intent:
        ```json
        {target_intent}
        ```

        Each JSON has following keys:
        1. sql_type : The type of SQL statement (CREATE, SELECT, INSERT, etc.)
        2. logical_flow : The logical flow and what this SQL code is doing
        3. key_tables : Key tables involved
        4. sql_functions : SQL functions used in the code and their purpose
        5. performance_considerations : Any potential performance considerations
        6. migration_challenges : Identify if there's any potential migration challenges to convert this SQL to Databricks DBSQL.

        Consider the the first 5 keys to compare whether the source and target SQL code are similar or not.
        If you think they are different, estimate the similarity score at the end of the response.
        Also while analyzing the sql_functions, be mindful of the fact that depending on source and target SQL dialects,
        the same function may have different names or parameters. Acknowledge that in your response while calculating the similarity.
        """
        )

        self.llm_chain = self.prompt_template | self.llm

    def compare(self) -> str | list:
        """Compare the code intent of source and target SQL code."""
        source_intent_str = json.dumps(self.source_intent)
        target_intent_str = json.dumps(self.target_intent)
        response = self.llm_chain.invoke({"source_intent": source_intent_str, "target_intent": target_intent_str})

        return response.content
