import os
import datetime
import config 

def criar_mapeamento_vault_time(vault_csv_files):
    """Cria um dicionário mapeando cada vault ao seu time correspondente."""
    vault_team_map = {}
    for csv_path in vault_csv_files:
        filename = os.path.basename(csv_path)
        
        # 1. Começamos assumindo que é o time padrão
        team = config.DEFAULT_TEAM 
        
        # 2. Procuramos no nosso "painel de controle" se há uma regra específica
        for chave, nome_do_time in config.VAULT_TEAM_MAPPING.items():
            if chave in filename:
                team = nome_do_time
                break # Achou o time, pode parar de procurar!
        
        with open(csv_path, "r", encoding="utf-8") as doc:
            for line in doc.readlines()[1:]:
                vault_name = line.split(";")[0].replace('"', '').strip()
                if vault_name:
                    vault_team_map[vault_name] = team
                    
    return vault_team_map

def consolidar_dados(user_data, vault_data, vault_team_map):
    """
    Estrutura os dados brutos de usuários e vaults em um dicionário consolidado.
    """
    all_data = {}
    
    # 1. Processa e filtra os dados dos usuários
    for row in user_data:
        if len(row) < 10:
            continue
        
        nome_vault = row[9]
        email = row[2]
        username = row[3]
        license_info = row[4]

        # Inicializa a estrutura para um novo vault se ele não existir
        if nome_vault not in all_data:
            all_data[nome_vault] = {
                'vaultData': {
                    'Vault name': [], 'Data': [], 'Database Size': [],
                    'File Storage': [], 'Enabled Users': [], 'Objects': [],
                    'Localizacao': vault_team_map.get(nome_vault, "Cloud Team I") 
                },
                'userData': []
            }
        
        # Define as condições de filtro para adicionar um usuário
        is_external = all(dominio not in email for dominio in config.DOMINIOS_IGNORADOS)
        has_license = license_info != 'No license'
        is_not_internal_user = username not in config.MFILES_USERS
        is_not_duplicate = [username, email] not in all_data[nome_vault]['userData']

        if is_external and has_license and is_not_internal_user and is_not_duplicate:
            all_data[nome_vault]['userData'].append([username, email, license_info])

    # 2. Processa os dados técnicos dos vaults
    for row in vault_data:
        if len(row) < 7:
            continue
            
        name_vault = row[0]
        if not name_vault:
            continue


        # Captura os valores e remove espaços extras/quebras de linha
        raw_storage = row[5].strip()
        raw_db_size = row[6].strip()
        raw_objects = row[3].strip()

        # Conversão segura para File Storage (row[5])
        file_storage = float(raw_storage) if raw_storage else 0.0

        # Conversão segura para Database Size (row[6])
        database_size = float(raw_db_size) if raw_db_size else 0.0

        # Conversão segura para Objects (row[3])
        objects = int(raw_objects) if raw_objects else 0

        # Garante que o vault exista no dicionário (caso não tenha usuários)
        if name_vault != "" and name_vault not in all_data:
             all_data[name_vault] = {
                'vaultData': {
                    'Vault name': [], 'Data': [], 'Database Size': [],
                    'File Storage': [], 'Enabled Users': [], 'Objects': [],
                    'Localizacao': vault_team_map.get(name_vault, "Cloud Team I") 
                },
                'userData': []
            }
            
        # Adiciona a chave 'Objects' se ela não existir
        if 'Objects' not in all_data[name_vault]['vaultData']:
            all_data[name_vault]['vaultData']['Objects'] = []

        # Adiciona os dados técnicos ao vault correspondente
        all_data[name_vault]['vaultData']['Vault name'].append(name_vault)
        all_data[name_vault]['vaultData']['Data'].append(datetime.datetime.now())
        all_data[name_vault]['vaultData']['Database Size'].append(round(database_size, 2))
        all_data[name_vault]['vaultData']['File Storage'].append(round(file_storage, 2))
        all_data[name_vault]['vaultData']['Enabled Users'].append(len(all_data[name_vault]['userData']))
        all_data[name_vault]['vaultData']['Objects'].append(objects)
        
    return all_data