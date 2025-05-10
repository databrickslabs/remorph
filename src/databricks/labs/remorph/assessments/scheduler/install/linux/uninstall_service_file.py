import logging
from pathlib import Path
import subprocess


def uninstall_service_file():

    # Stop the system timer
    logging.info("Stoping profiler timer.")
    subprocess.run(["sudo", "systemctl", "stop", "remorph_usage_collection.timer"], check=False)

    # Disbale the system timer
    logging.info("Disabling profiler scheduler.")
    subprocess.run(["sudo", "systemctl", "disable", "remorph_usage_collection.timer"], check=False)

    # Remove the unit file and timer file
    system_files_dir = Path("/etc/systemd/system/")
    unit_file_path = system_files_dir / "remorph_usage_collection.service"
    timer_file_path = system_files_dir / "remorph_usage_collection.timer"
    unit_file_path.unlink()
    timer_file_path.unlink()


def main():
    logging.info("Uninstalling Linux scheduler components...\n")
    uninstall_service_file()
    logging.info("Uninstallation complete.")


if __name__ == "__main__":
    main()
