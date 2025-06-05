from databricks.sdk import WorkspaceClient
from databricks.sdk.service.serving import ChatMessage, ChatMessageRole

class CodeExplainer:
    def __init__(self, ws: WorkspaceClient):
        self.ws = ws
        self.explanation_endpoint = 'databricks-meta-llama-3-1-405b-instruct'
        self.endpoint_exists = self._endpoint_exists()
        self.whole_file_prompt = ('Your job is to provide a high level summary of the following SQL code. This summary should focus on the code\'s overall purpose, not a line by line breakdown. Be concise, but make sure to cover all the main points of the code. An example output '
                                  'is "This code calculates the total sales for each product in the database, broken down by region and compared to target. It uses data from the sales, targets, and products tables."')
        self.statement_prompt = 'Your job is to provide a useful explanation for this bit of SQL code. Be concise'

    def _endpoint_exists(self):
        """Check if the explanation endpoint exists in the workspace"""
        return self.explanation_endpoint in [x.name for x in self.ws.serving_endpoints.list()]

    def _load_file(self, file_path: str):
        """ load an output file from remorph for passing to the explanation endpoint """
        with open(file_path, 'r') as f:
            whole_file = f.read()
        statements = whole_file.split(';')

        return whole_file, statements

    def _write_file(self, file_path: str, content: str):
        """ write the output file with explanations """
        with open(file_path, 'w') as f:
            f.write(content)

    def call_llm(self, sys_prompt: str, code: str) -> str:
        """
        Function to call the LLM model and return the response.
        :param sys_prompt: the system prompt to send to the model
        :param code: the code to explain
        :return: the response from the model
        """
        if not self.endpoint_exists:
            raise ValueError('Explanation endpoint not found in workspace, unable to explain code')

        messages = [
            ChatMessage(role=ChatMessageRole.SYSTEM, content=sys_prompt),
            ChatMessage(role=ChatMessageRole.USER, content=code),
        ]

        response = self.ws.serving_endpoints.query(
            name=self.explanation_endpoint,
            messages=messages,
        )

        message = response.choices[0].message.content
        return message

    def _encomment(self, input: str) -> str:
        """Wrap a string in a comment block"""
        return "/* " + input + " */"

    def explain_file(self, file_path: str):
        """Explain the code in a file"""
        whole_file, statements = self._load_file(file_path)
        whole_file_explanation = self.call_llm(self.whole_file_prompt, whole_file)
        # wrap the explanation in a comment block
        whole_file_explanation = self._encomment(whole_file_explanation)

        # ignore statements which are <5 lines long
        # create a list of explanations, which we will use to recreate the code file with explanations. We'll need
        # to append empty strings for statements that are too short to explain.
        statement_explanations = []
        for statement in statements:
            if len(statement.split('\n')) < 5:
                statement_explanations.append('')
            else:
                explanation = self.call_llm(self.statement_prompt, statement)
                statement_explanations.append(self._encomment(explanation))

        # build an explained file. Start with the whole file explanation at the top and add a couple of blank lines
        output_file = ''
        output_file += whole_file_explanation + '\n\n'
        for i in range(len(statements)):
            output_file += statement_explanations[i]
            output_file += statements[i] + '\n'

        output_path_elements = file_path.split('.')
        file_ext = output_path_elements[-1]
        output_path_str = '.'.join(output_path_elements[:-1])
        output_path_str += ('_explained.' + file_ext)
        self._write_file(output_path_str, output_file)
