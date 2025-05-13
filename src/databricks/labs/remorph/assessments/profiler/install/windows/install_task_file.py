from pathlib import Path
from subprocess import run
import getpass
import logging


PROFILER_SCHEDULER_TASK_NAME = "Remorph Usage Collection"


def schedule_usage_collection():
    # Schedule the profiler usage collection task
    pipeline_scheduler_path = f"{Path.cwd().parent}\\pipeline_scheduler.py"
    usage_collection_command = f"python {pipeline_scheduler_path}"
    logging.info(f"Scheduling usage collection task: {usage_collection_command}")
    run(
        [
            "SCHTASKS",
            "/CREATE",
            "/TN",
            PROFILER_SCHEDULER_TASK_NAME,
            "/TR",
            usage_collection_command,
            "/SC",
            "MINUTE",
            "/MO",
            "15",
            "/RL",
            "HIGHEST",
            "/F",
            "/RU",
            getpass.getuser(),
        ],
        check=False,
    )


def main():
    logging.info("Installing Windows profiler components...\n")
    schedule_usage_collection()


if __name__ == "__main__":
    main()
