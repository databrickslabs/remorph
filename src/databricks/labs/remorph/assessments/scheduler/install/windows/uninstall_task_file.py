import logging
from pathlib import Path
import subprocess


def uninstall_task_file():
    # Delete the registered task
    logging.info("Deleting scheduled task from task manager.")
    subprocess.run(["schtasks", "/Delete", "/TN", "Remorph Usage Collection", "/F"], check=False)

    # Remove the imported task if still exists
    logging.info("Removing task file from the Downloads folder.")
    downloads_path = Path.home() / "Downloads"
    task_def_path = downloads_path / "usage_collection_task.xml"
    if task_def_path.exists():
        logging.info("Task file still exists. Removing.")
        task_def_path.unlink()


def main():
    logging.info("Uninstalling Windows scheduler components...\n")
    uninstall_task_file()
    logging.info("Uninstallation complete.")


if __name__ == "__main__":
    main()
