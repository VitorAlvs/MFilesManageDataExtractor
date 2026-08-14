import pyodbc
from os import getenv
from dotenv import load_dotenv
from pyodbc import connect
from data_processor import consolidar_dados
import os 

base_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(base_dir, '.env')

load_dotenv(dotenv_path=env_path, encoding='utf-8')

conn_str_general = getenv("CONN_STR_GENERAL")
if not conn_str_general:
    raise ValueError("System is missing the expected environment variable 'CONN_STR_GENERAL'. Please check your .env file.")

conn_str_data = getenv("CONN_STR_DATA")
if not conn_str_data:
    raise ValueError("System is missing the expected environment variable 'CONN_STR_DATA'. Please check your .env file.")

conn_general_db = connect(conn_str_general)
conn_data_db = connect(conn_str_data)

cursor_general_db = conn_general_db.cursor()
cursor_data_db = conn_data_db.cursor()


# Check if the subscription already exists in the database
def check_subscription(subscription_name):
    try:
        select_subscription_id_query = "SELECT SubscriptionID FROM Subscriptions WHERE SubscriptionName = ?;"
        cursor_general_db.execute(select_subscription_id_query, (subscription_name,))
        subscription_id = cursor_general_db.fetchone()
        if subscription_name == "":
            print("Subscription name is empty.")
        elif subscription_id == None:
            # print("Subscription not found in the database.")
            insert_subscription_query = "INSERT INTO Subscriptions (SubscriptionName) VALUES (?);"
            print("Inserted new subscription.")
            cursor_general_db.execute(insert_subscription_query, (subscription_name,))
            conn_general_db.commit()  # COMMIT the transaction
            return check_subscription(subscription_name)  # Return the result of recursive call
        else:
            result = int(str(subscription_id).strip('(),'))
            return result
    except pyodbc.Error as e:
        print(f"SQL Error: {e}")
        conn_general_db.rollback()
        raise

def check_vault_general_db(vault_name, subscription_id):
    try:
        select_vault_id_query = "SELECT VaultID FROM Vaults WHERE VaultName = ?;"
        cursor_general_db.execute(select_vault_id_query, (vault_name,))
        vault_id = cursor_general_db.fetchone()
        if vault_name == "":
            print("Vault name is empty.")
        elif vault_id == None:
            print("Vault not found in the general database.")
            insert_vault_query = "INSERT INTO Vaults (VaultName, SubscriptionID) VALUES (?, ?);"
            print("Inserted new vault into general database.")
            cursor_general_db.execute(insert_vault_query, (vault_name, subscription_id))
            conn_general_db.commit()  # COMMIT the transaction
            return check_vault_general_db(vault_name, subscription_id)  # Return the result of recursive call
        else:
            result = int(str(vault_id).strip('(),'))
            return result
    except pyodbc.Error as e:
        print(f"SQL Error: {e}")
        conn_general_db.rollback()
        raise

def check_vault_data_db(vault_name, vault_id):
    try:
        check_vault_query = "SELECT 1 FROM Vaults WHERE VaultName = ?;"
        cursor_data_db.execute(check_vault_query, (vault_name,))
        existing_vault = cursor_data_db.fetchone()
        if vault_name == "":
            print("Vault name is empty.")
        elif existing_vault == None:
            insert_vault_query = "INSERT INTO Vaults (ServerID, VaultName) VALUES (?, ?);"
            cursor_data_db.execute(insert_vault_query, (vault_id, vault_name))
            conn_data_db.commit()  # COMMIT the transaction
    except pyodbc.Error as e:
        print(f"SQL Error: {e}")
        conn_data_db.rollback()
        raise

def insert_volumetry(vault_id, data):
    date = data['vaultData']['Data'][0]
    obj = int(data['vaultData']['Objects'][0])
    file = float(data['vaultData']['File Storage'][0])
    db = float(data['vaultData']['Database Size'][0])
    users = int(data['vaultData']['Enabled Users'][0])

    try:
        insert_volumetry_query = "INSERT INTO VolumetryData (DateTime, ObjectCount, FileStorageGB, DatabaseSizeGB, UserCount, ServerID) VALUES (?, ?, ?, ?, ?, ?);"
        cursor_data_db.execute(insert_volumetry_query, (date, obj, file, db, users, vault_id))
        conn_data_db.commit()  # COMMIT the transaction
    except pyodbc.Error as e:
        print(f"SQL Error: {e}")
        conn_data_db.rollback()
        raise

def insert_data_into_database(consolidated_data):
    try:
        for each in consolidated_data:        
            if consolidated_data[each]['vaultData']['VaultName'] != []:
                subscription = consolidated_data[each]['vaultData']['Location']
                subscription_id = check_subscription(subscription)
                vault_name = consolidated_data[each]['vaultData']['VaultName'][0]
                vault_id = check_vault_general_db(vault_name, subscription_id)
                check_vault_data_db(vault_name, vault_id)        
                insert_volumetry(vault_id, consolidated_data[each])
    except Exception as e:
        print(f"Error inserting data: {e}")
        raise
