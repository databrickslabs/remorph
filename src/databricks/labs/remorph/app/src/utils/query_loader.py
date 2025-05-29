import os


def load_query(category, query_name, **kwargs):
    """
    Loads an SQL query from the 'queries' folder (ddls or dmls) and formats it with provided parameters.

    Args:
        category (str): 'ddls' or 'dmls' (subdirectory in 'queries')
        query_name (str): The name of the SQL file without extension.
        kwargs: Dynamic parameters to format inside the query.

    Returns:
        str: The formatted SQL query.

    Raises:
        FileNotFoundError: If the SQL file is not found.
        ValueError: If an invalid category is provided.
    """

    valid_categories = {"ddls", "dmls"}

    if category not in valid_categories:
        raise ValueError(f"Invalid category '{category}'. Choose from {valid_categories}")

    query_path = os.path.join(os.path.dirname(__file__), "..", "queries", category, f"{query_name}.sql")

    if not os.path.exists(query_path):
        raise FileNotFoundError(f"Query file '{query_name}.sql' not found in '{category}'")

    with open(query_path, "r", encoding="utf-8") as file:
        query = file.read()

    return query.format(**kwargs)
