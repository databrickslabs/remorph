# import os
# import streamlit as st
#
#
# def save_json(json_data, path: str):
#     try:
#         import dbutils
#
#         is_databricks = True
#     except ImportError:
#         is_databricks = False
#     path = path if path.endswith('/') else f'{path}/'
#     full_path_with_extension = f'{path}config.json'
#     if is_databricks:
#         try:
#             dbutils.fs.put(full_path_with_extension, json_data, overwrite=True)
#             print(f"JSON file successfully saved to Databricks workspace path: {path}")
#             st.success(f"JSON file successfully saved to Databricks workspace path: {path}")
#         except Exception as e:
#             print(f"Failed to save JSON to Databricks workspace: {e}")
#             st.exception(e)
#     else:
#         # Local environment: Save to local file system
#         try:
#             os.makedirs(os.path.dirname(path), exist_ok=True)
#             with open(full_path_with_extension, "w") as file:
#                 file.write(json_data)
#             print(f"JSON file successfully saved to local path: {full_path_with_extension}")
#             st.success(f"JSON file successfully saved to locaL path: {full_path_with_extension}")
#         except Exception as e:
#             print(f"Failed to save JSON locally: {e}")
