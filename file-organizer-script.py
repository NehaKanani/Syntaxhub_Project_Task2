import os
import shutil
import logging
from datetime import datetime

# ================= CONFIGURATION =================
TARGET_FOLDER = r"C:\Users\Neha\Downloads"  # Change path
DRY_RUN = True  # Set False to actually move files
LOG_FILE = "organizer.log"
# =================================================


def setup_logger():
    logging.basicConfig(
        filename=LOG_FILE,
        level=logging.INFO,
        format="%(asctime)s - %(message)s"
    )


def get_unique_name(destination, filename):
    name, ext = os.path.splitext(filename)
    counter = 1

    while os.path.exists(os.path.join(destination, filename)):
        filename = f"{name}_{counter}{ext}"
        counter += 1

    return filename


def organize_files(folder, dry_run=False):
    for item in os.listdir(folder):
        item_path = os.path.join(folder, item)

        if os.path.isfile(item_path):
            ext = os.path.splitext(item)[1].lower().strip(".")

            if not ext:
                ext = "others"

            target_dir = os.path.join(folder, ext.upper())

            if not os.path.exists(target_dir):
                if not dry_run:
                    os.makedirs(target_dir)
                logging.info(f"Created folder: {target_dir}")

            new_name = get_unique_name(target_dir, item)
            target_path = os.path.join(target_dir, new_name)

            if dry_run:
                print(f"[DRY-RUN] Would move: {item} -> {target_dir}")
            else:
                shutil.move(item_path, target_path)
                logging.info(f"Moved: {item} -> {target_path}")
                print(f"Moved: {item}")


def main():
    setup_logger()
    logging.info("File Organizer Started")

    if not os.path.exists(TARGET_FOLDER):
        print("Target folder does not exist.")
        return

    organize_files(TARGET_FOLDER, DRY_RUN)

    logging.info("File Organizer Finished")
    print("Operation completed.")


if __name__ == "__main__":
    main()
