from requests import get

#Repurposed from https://github.com/Yarden-zamir/install-mssql-odbc

remove_exits = "True"
docs_url = 'https://raw.githubusercontent.com/MicrosoftDocs/sql-docs/live/docs/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server.md'
#currently Supports only Ubuntu 18
# TODO Add macos for developer support
distro = "Ubuntu"
ODBC_version = "18"

ODBC_section = get(docs_url, timeout=10).text.split(f"Microsoft ODBC {ODBC_version}")[1].split(
    "---")[0]
platforms = ODBC_section.split("### [")[1:]
per_platform_instructions = {}
for platform in platforms:
    name = platform.split("]")[0]
    code = platform.split("```bash")[1].split("```")[0]
    per_platform_instructions[name] = code.replace("exit\n", "") if remove_exits else code

print(per_platform_instructions[distro])
