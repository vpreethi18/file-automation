# file-automation
import os
import shutil
import logging

logging.basicConfig(
    filename="file_organizer.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


FILE_TYPES = {
    "Images": [".jpg", ".png", ".jpeg", ".gif"],
    "Documents": [".pdf", ".docx", ".txt", ".pptx"],
    "Videos": [".mp4", ".mkv", ".avi"],
    "Music": [".mp3", ".wav"],
    "Archives": [".zip", ".rar"]
}


def organize_files(folder_path):
    try:
        if not os.path.exists(folder_path):
            raise FileNotFoundError("Folder does not exist")

        files = os.listdir(folder_path)

        for file in files:
            file_path = os.path.join(folder_path, file)

            if os.path.isfile(file_path):
                moved = False
                _, ext = os.path.splitext(file)

                for folder, extensions in FILE_TYPES.items():
                    if ext.lower() in extensions:
                        dest_folder = os.path.join(folder_path, folder)
                        os.makedirs(dest_folder, exist_ok=True)

                        destination = os.path.join(dest_folder, file)
                        counter = 1

                        # Handle duplicate file names
                        while os.path.exists(destination):
                            name, extension = os.path.splitext(file)
                            destination = os.path.join(
                                dest_folder, f"{name}_{counter}{extension}"
                            )
                            counter += 1

                        shutil.move(file_path, destination)
                        logging.info(f"Moved {file} to {folder}")
                        moved = True
                        break

                if not moved:
                    other_folder = os.path.join(folder_path, "Others")
                    os.makedirs(other_folder, exist_ok=True)
                    shutil.move(file_path, os.path.join(other_folder, file))
                    logging.info(f"Moved {file} to Others")

        print("✅ File organization completed successfully!")

    except Exception as e:
        logging.error(f"Error occurred: {e}")
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    user_path = input("Enter folder path to organize: ").strip()
    organize_files(user_path)
