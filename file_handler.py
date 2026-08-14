import os
import getpass
import config
import send_email
from pathlib import Path

def move_csv_files_to_local_folder():
    """
    Moves user and vault CSV files from the Downloads folder to the script's local folder.
    Returns the path to the script's local folder.
    """
    username = os.environ.get('USERNAME') or getpass.getuser()
    if not username:
        raise EnvironmentError("Could not determine the username.")
    
    download_path = Path.home() / 'Downloads'
    destination_path = Path.cwd() # Current working directory
    
    print(f"Searching for CSV files in: {download_path}")
    downloaded_files = os.listdir(download_path)
    
    for file_name in downloaded_files:
        if "vaults" in file_name or "users" in file_name:
            source_path = download_path / file_name
            destination_file_path = destination_path / file_name
            os.rename(source_path, destination_file_path)
            print(f"File '{file_name}' moved to '{destination_path}'.")
    return destination_path

def parse_csv(csv_path):
    """
    Reads a single CSV file, removes the header, and returns a list of lists.
    """
    processed_data = []
    with open(csv_path, "r", encoding="utf-8") as doc:
        lines = doc.read().split("\n")

        header = lines[0].replace('"', "").replace('\ufeff', "").strip().split(";")
        
        if not (header == config.HEADER_USERS or header == config.HEADER_VAULTS):
            send_email.send_alert_email()
        else:
            pass
        
        content_lines = lines[1:]  # Remove header
        for line in content_lines:
            if line.strip(): # Ignore empty lines
                fields = [field.strip().replace('"', '') for field in line.split(";")]
                processed_data.append(fields)
    return processed_data
