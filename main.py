# Importações de bibliotecas padrão e de terceiros
import glob
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import mfiles

# Importações dos nossos módulos
import config
import web_extractor
import file_handler
import data_processor
import report_generator
import mfiles_uploader
import db_insert 

def run_automation():
    """Main function that orchestrates the entire automation process."""
    
    # =====================================================================
    # 1. INITIALIZATION AND DATA EXTRACTION
    # =====================================================================
    try:
        firefox_options = Options()
        firefox_options.add_argument("--headless")
        driver = webdriver.Firefox(options=firefox_options)
        mfiles_client = mfiles.Client(
            server=config.MFILES_SERVER_URL,
            user=config.MFILES_USERNAME,
            password=config.MFILES_PASSWORD,
            vault=config.MFILES_VAULT_GUID
        )
        for sub_id, alias in config.MFILES_SUBSCRIPTIONS.items():
            web_extractor.extract_manage_data(
                driver, sub_id, alias, config.MFILES_USERNAME, config.MFILES_PASSWORD
            )
    finally:
        driver.quit()
        print("Browser closed.")

    # =====================================================================
    # 2. FILE ORGANIZATION AND READING
    # =====================================================================
    local_folder = file_handler.move_csv_files_to_local_folder()
    
    user_csvs = glob.glob(str(local_folder / 'users*.csv'))
    vault_csvs = glob.glob(str(local_folder / 'vaults*.csv'))

    user_data_raw = []
    vault_data_raw = []

    for csv_file in user_csvs:
        user_data_raw.extend(file_handler.parse_csv(csv_file))
    
    for csv_file in vault_csvs:
        vault_data_raw.extend(file_handler.parse_csv(csv_file))

    # =====================================================================
    # 3. DATA PROCESSING AND CONSOLIDATION
    # =====================================================================
    vault_team_map = data_processor.create_vault_team_mapping(vault_csvs)
    consolidated_data = data_processor.consolidate_data(user_data_raw, vault_data_raw, vault_team_map)

    # =====================================================================
    # 4. DATABASE INSERTION
    # =====================================================================
    print("\nStarting data insertion into the database...")
    # Calls the main function of the db_insert module, passing the processed data
    db_insert.insert_data_into_database(consolidated_data)
    print("Data successfully inserted into the database!")


    # =====================================================================
    # 5. REPORT GENERATION
    # =====================================================================

    # User reports per vault (1 report per vault)
    report_generator.generate_user_vault_reports(consolidated_data, local_folder)
    # General report with all users 
    report_generator.generate_consolidated_user_report(consolidated_data, local_folder)
    # Report with vault volumetry and user data
    report_generator.generate_consolidated_report(consolidated_data, local_folder)

    # # =====================================================================
    # # 6. UPLOAD AND CLEANUP
    # # =====================================================================
    mfiles_uploader.upload_and_cleanup(mfiles_client, local_folder)
    
    print("\nProcess completed successfully!")


# =====================================================================
# 7. INITIALIZATION AND LOG CONFIGURATION
# =====================================================================
if __name__ == "__main__":
    import sys
    import os
    from datetime import datetime

    def configure_logs():
        """Configures print interception to save output to a .txt file."""
        class PrintLogger:
            def __init__(self, log_path):
                self.log_file = open(log_path, "a", encoding="utf-8")

            def write(self, message):
                self.log_file.write(message)
                self.log_file.flush()

            def flush(self):
                self.log_file.flush()
                
        os.makedirs("logs", exist_ok=True)
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S') # Example: 2023-10-27_14-30-00
        log_file_path = f"logs/execution_{timestamp}.txt"

        sys.stdout = PrintLogger(log_file_path)
        sys.stderr = sys.stdout 
        return log_file_path

    log_file_path = configure_logs()

    print(f"============================================================")
    print(f"STARTING AUTOMATION - {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print(f"Log file generated at: {log_file_path}")
    print(f"============================================================")

    try:
        run_automation()
    finally:
        print(f"============================================================")
        print(f"FINISHING AUTOMATION - {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        print(f"============================================================")