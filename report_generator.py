import pandas as pd
from datetime import date

def _format_sheet(writer, df, sheet_name, header):
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

def generate_user_vault_reports(all_data, destination_path):
    """Generates an Excel report for each vault with the list of active users."""
    print("Generating user reports per vault...")
    for vault_name, data in all_data.items():
        if not vault_name.strip():
            print("[ERROR] Empty vault name detected, skipping...")
            continue
        
        if data['userData']:
            header = ['Name', 'Email']
            df = pd.DataFrame(data['userData'], columns=header).sort_values(by='Name')
            
            filename = f'active_users_{vault_name}_{date.today().strftime("%Y-%m-%d")}.xlsx'
            excel_path = destination_path / filename
            
            with pd.ExcelWriter(excel_path, engine='xlsxwriter') as writer:
                df.to_excel(writer, sheet_name='Users', index=False, header=False, startrow=1)
                _format_sheet(writer, df, 'Users', header)
            print(f"Report '{filename}' created.")
        else:
            print(f"[WARNING] Vault '{vault_name}' has no active users to generate a report.")


def generate_consolidated_user_report(all_data, destination_path):
    """Generates a single Excel report with active users from all vaults, including the Vault column."""
    print("Generating consolidated user report by vault...")
    header = ['Vault', 'Name', 'Email']
    rows = []

    for vault_name, data in all_data.items():
        if not vault_name.strip():
            print("[ERROR] Empty vault name detected, skipping...")
            continue

        for name, email in data.get('userData', []):
            rows.append([vault_name, name, email])

    df = pd.DataFrame(rows, columns=header)
    if not df.empty:
        df = df.sort_values(by=['Vault', 'Name']).reset_index(drop=True)

    filename = f'consolidated_active_users_{date.today().strftime("%Y-%m-%d")}.xlsx'
    excel_path = destination_path / filename

    with pd.ExcelWriter(excel_path, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Users', index=False, header=False, startrow=1)
        _format_sheet(writer, df, 'Users', header)

    print(f"Consolidated report '{filename}' created successfully.")


def generate_consolidated_report(all_data, destination_path):
    """Generates a single Excel report with consolidated data from all vaults."""
    print("Generating consolidated vault report...")
    header = ['Location', 'Vault', 'Date', 'Objects',  'DB Size (GB)', 'File Storage (GB)', 'Enabled Users']
    rows = []

    for vault_name, data in all_data.items():
        vault_details = data['vaultData']
        if not vault_details['VaultName']: continue
        
        rows.append([
            vault_details['Location'],
            vault_details['VaultName'][0],
            vault_details['Date'][0],
            vault_details['Objects'][0],
            vault_details['DatabaseSize'][0],
            vault_details['FileStorage'][0],
            vault_details['EnabledUsers'][0]
        ])

    df = pd.DataFrame(rows, columns=header).sort_values(by=['Location', 'Vault'])
    
    # Convert the 'Date' column to a formatted string, preventing row formats from altering its display in Excel
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce').dt.strftime('%d/%m/%Y %H:%M:%S').fillna('')
    
    filename = f'vault_data_{date.today().strftime("%Y-%m-%d")}.xlsx'
    excel_path = destination_path / filename
    
    with pd.ExcelWriter(excel_path, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Vaults', index=False, header=False, startrow=1)
        _format_sheet(writer, df, 'Vaults', header)
    
    print(f"Consolidated report '{filename}' created successfully.")