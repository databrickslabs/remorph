from __future__ import annotations

from typing import Any, Dict, Optional, List


from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import ResponseSchema, StructuredOutputParser
from langchain_core.documents import Document
from databricks_langchain import ChatDatabricks

from databricks.labs.remorph.agents.code_explainer.parser import SqlParser


class SQLExplainer:
    """SQL Explainer class to explain SQL code using Databricks LLM."""

    def __init__(self, endpoint_name: str = "databricks-llama-4-maverick", format_flag: bool = False):
        self.endpoint_name = endpoint_name
        self.format_flag = format_flag

        """Initialize the SQL Explainer Chain"""
        self.llm = ChatDatabricks(endpoint=self.endpoint_name, extra_params={"temperature": 0.0})

        # Create the prompt template
        self.prompt_template = ChatPromptTemplate.from_template(
            """
        Analyze the following SQL code segment and explain its purpose and functionality:

        ```sql
        {sql_segment}
        ```

        Provide a comprehensive explanation including:
        1. What kind of SQL statement this is (CREATE, SELECT, INSERT, etc.)
        2. The logical flow and what this SQL code is doing
        3. Key tables involved
        4. SQL functions used in the code and their purpose
        5. Any potential performance considerations
        6. Identify if there's any potential migration challenges to convert this SQL to Databricks DBSQL.

        {format_instructions}
        """
        )

        # Create the LLM chain
        # self.llm_chain = ConversationChain(
        #     llm=self.llm,
        #     prompt=self.prompt_template,
        #     memory = ConversationBufferMemory()
        # )

        self.llm_chain = self.prompt_template | self.llm

    def format_output(self) -> Optional[StructuredOutputParser]:
        """Format the output from the LLM into a structured format"""
        # Define the response schema
        sql_type_schema = ResponseSchema(
            name="sql_type",
            description="What kind of SQL statement this is (CREATE, SELECT, INSERT, etc.).\
            If it's a create statement, include the database/schema (if available), table/view name and columns.",
        )

        sql_flow_schema = ResponseSchema(
            name="sql_flow",
            description="The logical flow of the SQL and what this SQL code is doing.\
            Include the key tables and operations involved (Filter, Join, Group by etc).\
            Write the SQL flow in a way we explain the ETL logic",
        )

        key_tables_schema = ResponseSchema(
            name="key_tables",
            description="extract all the tables/views along with schema details mentioned in the SQL and output them as comma .\
                        separated python list.",
        )

        sql_functions_schema = ResponseSchema(
            name="sql_functions",
            description="List of SQL functions used in the SQL and their purpose.\
                        Extract the Output as comma separated python list each having a tuple of function name and its purpose.",
        )

        performance_considerations_schema = ResponseSchema(
            name="performance_considerations",
            description="Identify if there's any potential performance considerations and suggest optimization techniques.",
        )

        migration_challenges_schema = ResponseSchema(
            name="migration_challenges",
            description="Identify if there's any potential migration challenges to convert this SQL to Databricks DBSQL. Identify the \
                        SQL functions and features that are not supported in Databricks DBSQL and suggest alternatives.",
        )

        response_schema = [
            sql_type_schema,
            sql_flow_schema,
            key_tables_schema,
            sql_functions_schema,
            performance_considerations_schema,
            migration_challenges_schema,
        ]

        # Create the output parser
        output_parser = StructuredOutputParser.from_response_schemas(response_schema)

        return output_parser

    def explain_document(self, doc: Document) -> Dict[str, Any]:
        """Explain a single SQL document"""
        sql_segment = doc.page_content

        output_parser = self.format_output()
        format_instructions = output_parser.get_format_instructions()

        result = dict()
        # Run the chain
        response = (
            self.llm_chain.invoke({"sql_segment": sql_segment, "format_instructions": format_instructions})
            if self.format_flag
            else self.llm_chain.invoke({"sql_segment": sql_segment, "format_instructions": ""})
        )

        # format the output if flag is set to True
        result["explanation"] = output_parser.parse(response.content) if self.format_flag else response.content

        # Add metadata to the result
        result["metadata"] = doc.metadata
        result["original_sql"] = sql_segment

        return result

    def explain_documents(self, docs: List[Document]) -> List[Dict[str, Any]]:
        """Explain multiple SQL documents"""
        results = []
        for doc in docs:
            result = self.explain_document(doc)
            results.append(result)
        return results

    def batch_explain(self, sql_file_path: str) -> List[Dict[str, Any]]:
        """Parse and explain all SQL segments in a file"""
        parser = SqlParser(file_path=sql_file_path)
        docs = parser.parse()
        return self.explain_documents(docs)
