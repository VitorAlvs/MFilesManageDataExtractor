import os
import datetime
import config 

def criar_mapeamento_vault_time(vault_csv_files):
    """Creates a dictionary mapping each vault to its corresponding team."""
    vault_team_map = {}
    for csv_path in vault_csv_files:
        filename = os.path.basename(csv_path)
        
        # 1. Start by assuming the default team
        team = config.DEFAULT_TEAM
        
        # 2. Check our "control panel" for a specific rule
        for key, team_name in config.VAULT_TEAM_MAPPING.items():
            if key in filename:
                team = team_name
                break # Found the team, can stop searching!
        
        with open(csv_path, "r", encoding="utf-8") as doc:
            for line in doc.readlines()[1:]:
                vault_name = line.split(";")[0].replace('"', '').strip()
                if vault_name:
                    vault_team_map[vault_name] = team
                    
    return vault_team_map

def consolidate_data(user_data, vault_data, vault_team_map):
    """
    Estrutura os dados brutos de usuários e vaults em um dicionário consolidado.
    """
    all_data = {}
    
    # 1. Processa e filtra os dados dos usuários
    for row in user_data:
        if len(row) < 10:
            continue
        
        vault_name = row[9]
        email = row[2]
        username = row[3]
        license_info = row[4]

        # Inicializa a estrutura para um novo vault se ele não existir
        if vault_name not in all_data:
            all_data[vault_name] = {
                'vaultData': {
                    'VaultName': [], 'Date': [], 'DatabaseSize': [],
                    'FileStorage': [], 'EnabledUsers': [], 'Objects': [],
                    'Location': vault_team_map.get(vault_name, config.DEFAULT_TEAM) 
                },
                'userData': []
            }
        
        # Define as condições de filtro para adicionar um usuário
        is_external = all(domain not in email for domain in config.IGNORED_DOMAINS)
        has_license = license_info != 'No license'
        is_not_internal_user = username not in config.MFILES_IGNORED_USERS
        is_not_duplicate = [username, email] not in all_data[vault_name]['userData']

        if is_external and has_license and is_not_internal_user and is_not_duplicate: # Preserve logic
            all_data[vault_name]['userData'].append([row[3], email])

    # 2. Processa os dados técnicos dos vaults
    for row in vault_data:
        if len(row) < 7:
            continue
            
        name_vault = row[0]
        if not name_vault: # Preserve logic
            continue


        # Capture values and remove extra spaces/newlines
        raw_storage = row[5].strip()
        raw_db_size = row[6].strip()
        raw_objects = row[3].strip()

        # Safe conversion for File Storage (row[5])
        file_storage = float(raw_storage) if raw_storage else 0.0

        # Safe conversion for Database Size (row[6])
        database_size = float(raw_db_size) if raw_db_size else 0.0

        # Safe conversion for Objects (row[3])
        objects = int(raw_objects) if raw_objects else 0

        # Ensure the vault exists in the dictionary (in case it has no users)
        if name_vault != "" and name_vault not in all_data: # Preserve logic
             all_data[name_vault] = {
                'vaultData': {
                    'VaultName': [], 'Date': [], 'DatabaseSize': [],
                    'FileStorage': [], 'EnabledUsers': [], 'Objects': [],
                    'Location': vault_team_map.get(name_vault, config.DEFAULT_TEAM) 
                },
                'userData': []
            }
            
        # Add the 'Objects' key if it doesn't exist
        if 'Objects' not in all_data[name_vault]['vaultData']:
            all_data[name_vault]['vaultData']['Objects'] = []

        # Add technical data to the corresponding vault
        all_data[name_vault]['vaultData']['VaultName'].append(name_vault)
        all_data[name_vault]['vaultData']['Date'].append(datetime.datetime.now())
        all_data[name_vault]['vaultData']['DatabaseSize'].append(round(database_size, 2))
        all_data[name_vault]['vaultData']['FileStorage'].append(round(file_storage, 2))
        all_data[name_vault]['vaultData']['EnabledUsers'].append(len(all_data[name_vault]['userData']))
        all_data[name_vault]['vaultData']['Objects'].append(objects)
        
    return all_data