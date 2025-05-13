from subprocess import run, CalledProcessError
import logging


PROFILER_SCHEDULER_TASK_NAME = "Remorph Usage Collection"


def is_task_scheduled():
    try:
        logging.info("Checking if task exists.")
        run(["SCHTASKS", "/QUERY", "/TN", PROFILER_SCHEDULER_TASK_NAME], check=True, text=True)
        return True
    except CalledProcessError as e:
        error_msg = e.stderr
        logging.error(f"Failed to query scheduled usage collection task: {error_msg}")
        return False


def uninstall_task_file():
    # Delete the scheduled task
    logging.info("Deleting scheduled task from the task manager.")
    if is_task_scheduled():
        try:
            run(["SCHTASKS", "/DELETE", "/TN", PROFILER_SCHEDULER_TASK_NAME, "/F"], check=True)
        except CalledProcessError as e:
            error_msg = e.stderr
            logging.info(f"Failed to delete the usage collection task: {error_msg}")


def main():
    logging.info("Uninstalling profiler task components...\n")
    uninstall_task_file()


if __name__ == "__main__":
    main()
