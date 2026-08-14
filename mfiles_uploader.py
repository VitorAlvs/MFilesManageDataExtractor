# mfiles_uploader.py
import os
import glob
import locale
import config
from pathlib import Path
from datetime import date

def upload_and_cleanup(client, reports_folder):
    """
    Uploads .xlsx files to M-Files and removes local .csv and .xlsx files.
    """
    try:
        locale.setlocale(locale.LC_TIME, 'en_US.UTF-8') # Use a generic English locale
    except locale.Error:
        locale.setlocale(locale.LC_TIME, 'en_US') # Fallback to a more generic English locale
        
    xlsx_files = glob.glob(str(reports_folder / '*.xlsx'))
    csv_files = glob.glob(str(reports_folder / '*.csv'))
    
    print("Starting file upload to M-Files...")
    
    # Process only .xlsx files for upload
    for file_path in xlsx_files:
        filename = os.path.basename(file_path)
        
        # 1. Create a COPY of the static template from config.py
        # Use .copy() to avoid accidentally altering the original dictionary
        extra_info = config.MFILES_METADATA_TEMPLATE.copy()
        
        # 2. Inject dynamic data using the mapped property names
        extra_info[config.MFILES_PROP_FILENAME] = filename
        extra_info[config.MFILES_PROP_DATE] = date.today().isoformat()
        extra_info[config.MFILES_PROP_MONTH] = date.today().strftime("%B").capitalize()
        
        try:
            client.upload_file(
                file_path=file_path, # Use the full path for upload_file
                object_type=0, 
                object_class=config.MFILES_UPLOAD_CLASS_ID, 
                extra_info=extra_info # Send the constructed dictionary!
            )
            print(f"File '{filename}' uploaded successfully.")
        except Exception as e:
            print(f"Error uploading file '{filename}': {e}")
        finally:
            # Ensure the xlsx file is deleted even if upload fails
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
                    print(f"Local file '{filename}' removed.")
            except Exception as remove_error:
                print(f"Error removing local file '{filename}': {remove_error}")
            
    # Process .csv files only for deletion
    for file_path in csv_files:
        filename = os.path.basename(file_path)
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"Local CSV file '{filename}' removed (no upload).")
        except Exception as e:
             print(f"Error removing CSV file '{filename}': {e}")