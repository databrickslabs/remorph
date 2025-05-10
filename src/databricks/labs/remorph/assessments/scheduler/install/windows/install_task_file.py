import logging
from pathlib import Path
import subprocess
import shutil


def install_task_file():
    # Prepare the task file for import
    logging.info("Copying task file to Downloads folder.")
    downloads_path = Path.home() / "Downloads"
    task_def_path = downloads_path / "usage_collection_task.xml"
    shutil.copy2("usage_collection_task.xml", downloads_path)

    # Import the task definition, force overwrite if exists
    logging.info("Importing task from task file.")
    subprocess.run(["schtasks", "/Create", "/TN", "Remorph Usage Collection", "/XML", task_def_path, "/F"], check=False)


def main():
    logging.info("Installing Windows scheduler components...\n")
    install_task_file()
    logging.info("Installation complete.")


if __name__ == "__main__":
    main()
