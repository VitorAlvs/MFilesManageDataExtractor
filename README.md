*   [🇧🇷 Português](#português)
*   [🇺🇸 English](#english)

## 🇧🇷 Português <a name="português"></a>

Automação de extração, tratamento e carga de dados do M-Files Manage para SQL Server, com geração de relatórios Excel e upload automático para o M-Files.

### 🎯 Objetivo e Motivação

Este projeto foi desenvolvido para automatizar a coleta de dados de volumetria (como contagem de objetos, uso de armazenamento e número de usuários) de diferentes vaults gerenciados pelo M-Files. Embora o M-Files possua uma API REST robusta para interagir com o conteúdo dos vaults, os dados consolidados de volumetria não estão disponíveis através dela, sendo acessíveis apenas pelo portal web do **M-Files Manage**.

A abordagem manual de acessar o portal para cada vault, exportar relatórios e consolidar as informações é demorada, propensa a erros e inviabiliza o monitoramento contínuo. Com o objetivo de otimizar esse processo, esta solução utiliza automação web (Selenium) para simular a navegação humana, extrair os relatórios em CSV e centralizar os dados de forma eficiente.

O resultado é um fluxo ETL completo que permite coletar métricas de forma regular, inseri-las em um banco de dados SQL Server para análise histórica e gerar relatórios consolidados, eliminando a necessidade de intervenção manual.

---


### 📝 Sobre o projeto

Este projeto executa um fluxo completo de ETL:

1.  Extrai relatórios de assinaturas do M-Files Manage via Selenium.
2.  Processa e filtra informações de usuários e vaults.
3.  Grava métricas em bancos SQL Server separados para cadastro e volumetria.
4.  Gera relatórios Excel consolidados.
5.  Faz upload dos relatórios para o M-Files.
6.  Registra todo o processo em logs.

### ✨ Funcionalidades principais

*   Extração automatizada de CSVs de `vaults` e `users` pelo Manage.
*   Navegação com Selenium em `headless` (sem abrir janela visível).
*   Filtragem de usuários internos e domínios ignorados.
*   Consolidação de dados por vault e time responsável.
*   Inserção de dados em dois bancos SQL Server (`ExampleGeneralDB` e `ExampleVaultDataDB`).
*   Geração de planilha Excel consolidada e com formatação.
*   Upload automático dos relatórios para o vault do M-Files.
*   Limpeza dos arquivos locais após upload.
*   Logs de execução gravados em `logs/`.

### 📂 Estrutura do projeto

```text
MFilesManageDataExtractor/
├── main.py
├── config.py
├── web_extractor.py
├── file_handler.py
├── data_processor.py
├── db_insert.py
├── report_generator.py
├── mfiles_uploader.py
├── send_email.py
├── setup_env.bat
├── run_app.bat
├── requirements.txt
├── .env
├── .gitignore
└── logs/
```

### ▶️ Como usar

#### Requisitos mínimos

*   Python 3.9+
*   Mozilla Firefox
*   GeckoDriver compatível com seu Firefox
*   ODBC Driver 17 for SQL Server
*   Acesso aos bancos de dados `ExampleGeneralDB` e `ExampleVaultDataDB`

#### Passos de instalação

1.  Clone o repositório:
    ```bash
    git clone https://github.com/your-username/MFilesManageDataExtractor
    cd MFilesManageDataExtractor
    ```

2.  Crie o arquivo `.env` na raiz do projeto.

3.  Execute o setup:
    ```bash
    setup_env.bat
    ```

4.  Execute o projeto:
    ```bash
    python main.py
    ```

#### Execução agendada

Use `run_app.bat` no Windows Task Scheduler para rodar o processo automaticamente.

### 🧾 Arquivo `.env`

Crie um `.env` similar a este:

```env
CONN_STR_GENERAL="DRIVER={ODBC Driver 17 for SQL Server};SERVER=your_server;DATABASE=ExampleGeneralDB;UID=your_user;PWD=your_password"
CONN_STR_DATA="DRIVER={ODBC Driver 17 for SQL Server};SERVER=your_server;DATABASE=ExampleVaultDataDB;UID=your_user;PWD=your_password"

MFILES_SERVER_URL="https://your-server.cloudvault.m-files.com/REST/"
MFILES_VAULT_GUID="{XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX}"
MFILES_USERNAME="user@example.com"
MFILES_PASSWORD="your_mfiles_password"

MFILES_MANAGE_PREFIX="123"
MFILES_SUBSCRIPTIONS_JSON='{"12345678": "alias1", "23456789": "alias2"}'
MFILES_IGNORED_USERS_LIST="user1,user2,admin,test"
IGNORED_EMAIL_DOMAINS="@example.com,@another-example.com"

SENDGRID_API_KEY="your_sendgrid_api_key"
```

#### O que cada variável significa

*   `CONN_STR_GENERAL`: Conexão para o banco `ExampleGeneralDB`.
*   `CONN_STR_DATA`: Conexão para o banco `ExampleVaultDataDB`.
*   `MFILES_SERVER_URL`: URL do servidor M-Files REST.
*   `MFILES_VAULT_GUID`: Identificador do vault de destino.
*   `MFILES_USERNAME` / `MFILES_PASSWORD`: Credenciais para M-Files e Manage.
*   `MFILES_MANAGE_PREFIX`: Prefixo usado para montar a URL do Manage.
*   `MFILES_SUBSCRIPTIONS_JSON`: Assinaturas do Manage com alias para cada tenant (formato JSON).
*   `MFILES_IGNORED_USERS_LIST`: Usuários internos que devem ser ignorados (lista separada por vírgulas).
*   `IGNORED_EMAIL_DOMAINS`: Domínios de e-mail a excluir do processamento (lista separada por vírgulas).
*   `SENDGRID_API_KEY`: Chave para enviar alertas por e-mail se o formato dos CSVs mudar.

> O `.env` não deve ser comitado. Ele é usado apenas localmente.

### ⚙️ O papel de `config.py`

O `config.py` centraliza as regras de negócio e parâmetros usados por todo o sistema.

#### Principais componentes de `config.py`

*   `MFILES_IGNORED_USERS`: Conjunto de usuários internos excluídos.
*   `IGNORED_DOMAINS`: Domínios ignorados durante a filtragem.
*   `MFILES_SUBSCRIPTIONS`: Dicionário com ID de assinatura e alias.
*   `VAULT_TEAM_MAPPING`: Mapeia IDs de vault para os nomes dos times.
*   `DEFAULT_TEAM`: Time padrão quando o vault não está em `VAULT_TEAM_MAPPING`.
*   `MFILES_SERVER_URL`, `MFILES_VAULT_GUID`, `MFILES_USERNAME`, `MFILES_PASSWORD`: Configurações do M-Files.
*   `MFILES_MANAGE_PREFIX`: Valor usado na URL do M-Files Manage.
*   `MANAGE_BASE_URL`: URL base para acesso às assinaturas.
*   `MFILES_UPLOAD_CLASS_ID`: Class ID utilizado para upload no M-Files.
*   `MFILES_METADATA_TEMPLATE`: Metadados estáticos aplicados nos uploads.
*   `MFILES_PROP_FILENAME`, `MFILES_PROP_DATE`, `MFILES_PROP_MONTH`: Nomes das propriedades dinâmicas do upload.
*   `HEADER_USERS` e `HEADER_VAULTS`: Cabeçalhos esperados nos CSVs exportados.

### 🧩 Responsabilidade de cada arquivo

*   `main.py`: Orquestra todo o fluxo do ETL.
*   `web_extractor.py`: Faz login no Manage, baixa CSVs de vaults e usuários.
*   `file_handler.py`: Move CSVs do `Downloads`, valida cabeçalhos e os parseia.
*   `data_processor.py`: Consolida dados, filtra usuários e associa times.
*   `db_insert.py`: Valida e insere dados nas tabelas SQL Server.
*   `report_generator.py`: Cria as planilhas Excel formatadas.
*   `mfiles_uploader.py`: Faz upload dos relatórios e remove os arquivos locais.
*   `send_email.py`: Envia alertas por SendGrid em caso de cabeçalhos inesperados.
*   `setup_env.bat`: Cria o ambiente virtual e instala dependências.
*   `run_app.bat`: Executa o `main.py` de forma previsível no Windows.

### 🔄 Fluxo completo de execução

1.  `main.py` inicializa o navegador headless.
2.  `web_extractor.py` baixa os CSVs do Manage.
3.  `file_handler.py` recolhe os arquivos do `Downloads` e os lê.
4.  `data_processor.py` filtra e consolida os dados.
5.  `db_insert.py` insere as informações em SQL Server.
6.  `report_generator.py` cria a planilha final.
7.  `mfiles_uploader.py` faz upload e limpa arquivos locais.
8.  Logs são salvos em `logs/`.

### 📌 Observações

*   Os relatórios são enviados como arquivos `.xlsx` ao M-Files.
*   Caso os cabeçalhos dos CSVs mudem, o módulo `send_email.py` tenta notificar a equipe.
*   `logs/` armazena o histórico de execução.
*   Ajustes futuros de vaults e propriedades podem ser feitos em `config.py`.

### 📦 Dependências

As bibliotecas estritamente necessárias para a execução do sistema estão mapeadas abaixo:

*   `pandas`: Manipulação e análise de dados
*   `selenium`: Automação web e navegação headless
*   `xlsxwriter`: Geração de planilhas Excel com formatação
*   `mfiles`: Integração com M-Files REST API
*   `pyodbc`: Conexão e operações com banco de dados SQL Server
*   `python-dotenv`: Carregamento seguro de variáveis de ambiente

(A instalação é gerida automaticamente pelo arquivo `setup_env.bat`)

---

### 🔒 Segurança

⚠️ **IMPORTANTE:**

*   **Nunca** faça commit do arquivo `.env` com credenciais reais.
*   O arquivo `.gitignore` já está configurado para proteger logs e dados sensíveis (`*.csv`, `*.xlsx`, `.env`, `logs/`).
*   Utilize usuários de banco de dados e M-Files com os privilégios mínimos necessários para a rotina.

---

### 📝 Licença

Este projeto é licenciado sob a licença MIT.

---

## 🇺🇸 English <a name="english"></a>

Automation for extracting, processing, and loading data from M-Files Manage to SQL Server, including Excel report generation and automatic upload to M-Files.

### 🎯 Objective and Motivation

This project was developed to automate the collection of volumetry data (such as object counts, storage usage, and user numbers) from various vaults managed by M-Files. Although M-Files has a robust REST API for interacting with vault content, consolidated volumetry data is not available through it and can only be accessed via the **M-Files Manage** web portal.

The manual approach of accessing the portal for each vault, exporting reports, and consolidating the information is time-consuming, error-prone, and hinders continuous monitoring. To optimize this process, this solution uses web automation (Selenium) to simulate human navigation, extract the CSV reports, and centralize the data efficiently.

The result is a complete ETL flow that allows metrics to be collected regularly, inserted into a SQL Server database for historical analysis, and consolidated reports to be generated, eliminating the need for manual intervention.

---

### 📝 About the Project

This project executes a complete ETL flow:

1.  Extracts subscription reports from M-Files Manage via Selenium.
2.  Processes and filters user and vault information.
3.  Records metrics into separate SQL Server databases for registration and volumetry.
4.  Generates consolidated Excel reports.
5.  Uploads the reports to M-Files.
6.  Logs the entire process.

### ✨ Key Features

*   Automated extraction of `vaults` and `users` CSVs from Manage.
*   Headless Selenium browsing (without visible window).
*   Filtering of internal users and ignored domains.
*   Data consolidation by vault and responsible team.
*   Data insertion into two SQL Server databases (`ExampleGeneralDB` and `ExampleVaultDataDB`).
*   Generation of consolidated and formatted Excel spreadsheets.
*   Automatic upload of reports to the M-Files vault.
*   Cleanup of local files after upload.
*   Execution logs saved in `logs/`.

### 📂 Project Structure

```text
MFilesManageDataExtractor/
├── main.py
├── config.py
├── web_extractor.py
├── file_handler.py
├── data_processor.py
├── db_insert.py
├── report_generator.py
├── mfiles_uploader.py
├── send_email.py
├── setup_env.bat
├── run_app.bat
├── requirements.txt
├── .env
├── .gitignore
└── logs/
```

### ▶️ How to Use

#### Minimum Requirements

*   Python 3.9+
*   Mozilla Firefox
*   GeckoDriver compatible with your Firefox version
*   ODBC Driver 17 for SQL Server
*   Access to `ExampleGeneralDB` and `ExampleVaultDataDB` databases

#### Installation Steps

1.  Clone the repository:
    ```bash
    git clone https://github.com/your-username/MFilesManageDataExtractor
    cd MFilesManageDataExtractor
    ```

2.  Create the `.env` file in the project root.

3.  Run the setup script:
    ```bash
    setup_env.bat
    ```

4.  Execute the project:
    ```bash
    python main.py
    ```

#### Scheduled Execution

Use `run_app.bat` with Windows Task Scheduler to run the process automatically.

### 🧾 `.env` File

Create a `.env` file similar to this:

```env
CONN_STR_GENERAL="DRIVER={ODBC Driver 17 for SQL Server};SERVER=your_server;DATABASE=ExampleGeneralDB;UID=your_user;PWD=your_password"
CONN_STR_DATA="DRIVER={ODBC Driver 17 for SQL Server};SERVER=your_server;DATABASE=ExampleVaultDataDB;UID=your_user;PWD=your_password"

MFILES_SERVER_URL="https://your-server.cloudvault.m-files.com/REST/"
MFILES_VAULT_GUID="{XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX}"
MFILES_USERNAME="user@example.com"
MFILES_PASSWORD="your_mfiles_password"

MFILES_MANAGE_PREFIX="123"
MFILES_SUBSCRIPTIONS_JSON='{"12345678": "alias1", "23456789": "alias2"}'
MFILES_IGNORED_USERS_LIST="user1,user2,admin,test"
IGNORED_EMAIL_DOMAINS="@example.com,@another-example.com"

SENDGRID_API_KEY="your_sendgrid_api_key"
```

#### What each variable means

*   `CONN_STR_GENERAL`: Connection string for the `ExampleGeneralDB` database.
*   `CONN_STR_DATA`: Connection string for the `ExampleVaultDataDB` database.
*   `MFILES_SERVER_URL`: M-Files REST server URL.
*   `MFILES_VAULT_GUID`: Identifier for the target vault.
*   `MFILES_USERNAME` / `MFILES_PASSWORD`: Credentials for M-Files and Manage.
*   `MFILES_MANAGE_PREFIX`: Prefix used to construct the Manage URL.
*   `MFILES_SUBSCRIPTIONS_JSON`: Manage subscriptions with aliases for each tenant (JSON format).
*   `MFILES_IGNORED_USERS_LIST`: Internal users to be ignored (comma-separated list).
*   `IGNORED_EMAIL_DOMAINS`: Email domains to exclude from processing (comma-separated list).
*   `SENDGRID_API_KEY`: Key for sending email alerts if CSV format changes.

> The `.env` file should not be committed. It is for local use only.

### ⚙️ The Role of `config.py`

`config.py` centralizes business rules and parameters used throughout the system.

#### Key Components of `config.py`

*   `MFILES_IGNORED_USERS`: Set of internal users to be excluded.
*   `IGNORED_DOMAINS`: Domains ignored during filtering.
*   `MFILES_SUBSCRIPTIONS`: Dictionary with subscription ID and alias.
*   `VAULT_TEAM_MAPPING`: Maps vault IDs to team names.
*   `DEFAULT_TEAM`: Default team when a vault is not in `VAULT_TEAM_MAPPING`.
*   `MFILES_SERVER_URL`, `MFILES_VAULT_GUID`, `MFILES_USERNAME`, `MFILES_PASSWORD`: M-Files configurations.
*   `MFILES_MANAGE_PREFIX`: Value used in the M-Files Manage URL.
*   `MANAGE_BASE_URL`: Base URL for accessing subscriptions.
*   `MFILES_UPLOAD_CLASS_ID`: Class ID used for M-Files uploads.
*   `MFILES_METADATA_TEMPLATE`: Static metadata applied to uploads.
*   `MFILES_PROP_FILENAME`, `MFILES_PROP_DATE`, `MFILES_PROP_MONTH`: Names of dynamic upload properties.
*   `HEADER_USERS` and `HEADER_VAULTS`: Expected headers in exported CSVs.

### 🧩 Responsibility of Each File

*   `main.py`: Orchestrates the entire ETL flow.
*   `web_extractor.py`: Logs into Manage, downloads vault and user CSVs.
*   `file_handler.py`: Moves CSVs from `Downloads`, validates headers, and parses them.
*   `data_processor.py`: Consolidates data, filters users, and associates teams.
*   `db_insert.py`: Validates and inserts data into SQL Server tables.
*   `report_generator.py`: Creates formatted Excel spreadsheets.
*   `mfiles_uploader.py`: Uploads reports and removes local files.
*   `send_email.py`: Sends alerts via SendGrid in case of unexpected headers.
*   `setup_env.bat`: Creates the virtual environment and installs dependencies.
*   `run_app.bat`: Executes `main.py` predictably on Windows.

### 🔄 Full Execution Flow

1.  `main.py` initializes the headless browser.
2.  `web_extractor.py` downloads CSVs from Manage.
3.  `file_handler.py` collects files from `Downloads` and reads them.
4.  `data_processor.py` filters and consolidates the data.
5.  `db_insert.py` inserts the information into SQL Server.
6.  `report_generator.py` creates the final spreadsheet.
7.  `mfiles_uploader.py` uploads and cleans up local files.
8.  Logs are saved in `logs/`.

### 📌 Notes

*   Reports are sent as `.xlsx` files to M-Files.
*   If CSV headers change, the `send_email.py` module attempts to notify the team.
*   `logs/` stores the execution history.
*   Future adjustments to vaults and properties can be made in `config.py`.

### 📦 Dependencies

The strictly necessary libraries for the system's execution are listed below:

*   `pandas`: Data manipulation and analysis
*   `selenium`: Web automation and headless browsing
*   `xlsxwriter`: Excel spreadsheet generation with formatting
*   `mfiles`: Integration with M-Files REST API
*   `pyodbc`: Connection and operations with SQL Server databases
*   `python-dotenv`: Secure loading of environment variables

(Installation is automatically managed by the `setup_env.bat` file)

---

### 🔒 Security

⚠️ **IMPORTANT:**

*   **Never** commit the `.env` file with real credentials.
*   The `.gitignore` file is already configured to protect logs and sensitive data (`*.csv`, `*.xlsx`, `.env`, `logs/`).
*   Use database and M-Files users with the minimum necessary privileges for the routine.

---

### 📝 License

This project is licensed under the MIT License.
