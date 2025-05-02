import logging
from pathlib import Path
import subprocess
import shutil


# Leveraging the Task manager in Windows has the following benefits:
# 1. No dependency on 3P software
# 2. Executes even if user is not logged in
# 3. Can be configured to run on schedule
# 4. Automatic start at boot
# 5. Can handle restart
# 6. Service-level execution w/ system permissions
def install_task_file():
    # Prepare the task file for import
    logging.info("Copying task file to Downloads folder.")
    downloads_path = Path.home() / "Downloads"
    task_def_path = downloads_path / "usage_collection_task.xml"
    shutil.copy2("usage_collection_task.xml", downloads_path)

    # TODO: Dynamically update the `REPLACE_ME` values in task template
    # Import the task definition, force overwrite if exists
    logging.info("Importing task from task file.")
    subprocess.run(["schtasks", "/Create", "/TN", "Remorph Usage Collection", "/XML", task_def_path, "/F"], check=False)


def main():
    logging.info("Installing Windows scheduler components...\n")
    install_task_file()
    logging.info("Installation complete.")


if __name__ == "__main__":
    main()
