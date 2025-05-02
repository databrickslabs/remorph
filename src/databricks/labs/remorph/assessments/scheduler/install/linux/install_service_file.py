import logging
from pathlib import Path
import subprocess
import shutil


def install_service_file():

    # Copy the unit file to `/etc/systemd/system/`
    system_files_dir = Path("/etc/systemd/system/")
    unit_file_path = system_files_dir / "remorph_usage_collection.service"
    shutil.copy2("remorph_usage_collection.service", unit_file_path)

    # Copy the timer file to `/etc/systemd/system/`
    timer_file_path = system_files_dir / "remorph_usage_collection.timer"
    shutil.copy2("remorph_usage_collection.timer", timer_file_path)

    # Ensure that the scheduler script exits too
    scheduler_path = Path(__file__).parent.parent.parent / "pipeline_scheduler.py"
    if not scheduler_path.exists():
        raise FileNotFoundError(f"Could not find the profiler scheduler: {scheduler_path}")

    # Reload the `systemd` process to pick up the new files
    logging.info("Reloading systemd.")
    subprocess.run(["sudo", "systemctl", "daemon-reload"], check=False)

    # Enable the system timer
    logging.info("Enabling profiler scheduler.")
    subprocess.run(["sudo", "systemctl", "enable", "remorph_usage_collection.timer"], check=False)

    # Start the system timer
    logging.info("Starting profiler timer.")
    subprocess.run(["sudo", "systemctl", "start", "remorph_usage_collection.timer"], check=False)


def main():
    logging.info("Installing Linux scheduler components...\n")
    install_service_file()
    logging.info("Installation complete.")


if __name__ == "__main__":
    main()
