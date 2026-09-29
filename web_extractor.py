import pandas as pd
from datetime import date

def _formatar_planilha(writer, df, sheet_name, header):
    """Função auxiliar para aplicar formatação em uma planilha."""
    worksheet = writer.sheets[sheet_name]
    workbook = writer.book

    # Formatos
    header_format = workbook.add_format({'bg_color': '#4ea72e', 'border': 1, 'border_color': '#8ed973', 'bold': True, 'color': 'white'})
    cell_format1 = workbook.add_format({'bg_color': '#daf2d0', 'border': 1, 'border_color': '#8ed973'})
    cell_format2 = workbook.add_format({'bg_color': '#FFFFFF', 'border': 1, 'border_color': '#8ed973'})

    # Aplica formato ao cabeçalho
    for col, value in enumerate(header):
        worksheet.write(0, col, value, header_format)

    # Formata linhas alternadas
    for row_num in range(len(df)):
        formato = cell_format1 if (row_num + 1) % 2 != 0 else cell_format2
        worksheet.write_row(row_num + 1, 0, df.iloc[row_num], formato)
    
    # Ajusta largura das colunas
    for i, col in enumerate(df.columns):
        values = df[col].astype(str).map(len)
        column_len = max(int(values.max()) if values.size else 0, len(col))
        worksheet.set_column(i, i, column_len + 2)
    
    # Autofilter
    worksheet.autofilter(0, 0, len(df), len(df.columns) - 1)

def gerar_planilhas_usuarios(all_data, destino_path):
    """Gera uma planilha Excel para cada vault com a lista de usuários ativos."""
    print("Gerando planilhas de usuários por vault...")
    for vault_name, data in all_data.items():
        if not vault_name.strip():
            print("[ERRO] Nome de vault vazio detectado, pulando...")
            continue
        
        if data['userData']:
            header = ['Nome', 'E-mail', 'Licença']
            df = pd.DataFrame(data['userData'], columns=header).sort_values(by='Nome')
            
            filename = f'usuarios_ativos_{vault_name}_{date.today().strftime("%d-%m-%Y")}.xlsx'
            excel_path = destino_path / filename
            
            with pd.ExcelWriter(excel_path, engine='xlsxwriter') as writer:
                df.to_excel(writer, sheet_name='Usuarios', index=False, header=False, startrow=1)
                _formatar_planilha(writer, df, 'Usuarios', header)
            print(f"Planilha '{filename}' criada.")
        else:
            print(f"[AVISO] Vault '{vault_name}' não possui usuários ativos para gerar planilha.")


def gerar_planilha_usuarios_consolidada(all_data, destino_path):
    """Gera uma única planilha Excel com os usuários ativos de todos os vaults, incluindo a coluna Vault."""
    print("Gerando planilha consolidada de usuários por vault...")
    header = ['Vault', 'Nome', 'E-mail', 'Licença']
    linhas = []

    for vault_name, data in all_data.items():
        if not vault_name.strip():
            print("[ERRO] Nome de vault vazio detectado, pulando...")
            continue

        for nome, email, license in data.get('userData', []):
            linhas.append([vault_name, nome, email, license])

    df = pd.DataFrame(linhas, columns=header)
    if not df.empty:
        df = df.sort_values(by=['Vault', 'Nome']).reset_index(drop=True)

    filename = f'usuarios_ativos_consolidado_{date.today().strftime("%d-%m-%Y")}.xlsx'
    excel_path = destino_path / filename

    with pd.ExcelWriter(excel_path, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Usuarios', index=False, header=False, startrow=1)
        _formatar_planilha(writer, df, 'Usuarios', header)

    print(f"Planilha consolidada '{filename}' criada com sucesso.")


def gerar_planilha_consolidada(all_data, destino_path):
    """Gera uma única planilha Excel com os dados consolidados de todos os vaults."""
    print("Gerando planilha consolidada de vaults...")
    header = ['Localização', 'Vault', 'Data', 'Objetos',  'DB em GB', 'DSK em GB', 'QTD Licenças']
    linhas = []

    for vault_name, data in all_data.items():
        vault_details = data['vaultData']
        if not vault_details['Vault name']: continue
        
        linhas.append([
            vault_details['Localizacao'],
            vault_details['Vault name'][0],
            vault_details['Data'][0],
            vault_details['Objects'][0],
            vault_details['Database Size'][0],
            vault_details['File Storage'][0],
            vault_details['Enabled Users'][0]
        ])

    df = pd.DataFrame(linhas, columns=header).sort_values(by=['Localização', 'Vault'])
    
    # Converte a coluna 'Data' para uma string formatada, evitando que os formatos de linha alterem sua visualização no Excel
    df['Data'] = pd.to_datetime(df['Data'], errors='coerce').dt.strftime('%d/%m/%Y %H:%M:%S').fillna('')
    
    filename = f'Dados_de_vaults_{date.today().strftime("%d-%m-%Y")}.xlsx'
    excel_path = destino_path / filename
    
    with pd.ExcelWriter(excel_path, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Vaults', index=False, header=False, startrow=1)
        _formatar_planilha(writer, df, 'Vaults', header)
    
    print(f"Planilha consolidada '{filename}' criada com sucesso.")