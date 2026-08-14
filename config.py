import os
import json
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
# Loads environment variables from the .env file
load_dotenv()

# =====================================================================
# USER AND SUBSCRIPTION CONFIGURATIONS
# =====================================================================
# M-Files users to be ignored (e.g., internal accounts)
users_to_ignore_str = os.getenv("MFILES_IGNORED_USERS_LIST", "")
MFILES_IGNORED_USERS = set(users_to_ignore_str.split(",")) if users_to_ignore_str else set()

# Email domains to be ignored during user filtering
ignored_domains_str = os.getenv("IGNORED_EMAIL_DOMAINS", "")
IGNORED_DOMAINS = tuple(ignored_domains_str.split(",")) if ignored_domains_str else tuple()

# M-Files subscriptions with their aliases (JSON format)
subscriptions_json_str = os.getenv("MFILES_SUBSCRIPTIONS_JSON", "{}")
MFILES_SUBSCRIPTIONS = json.loads(subscriptions_json_str)

# =====================================================================
# EMAIL ALERT CONFIGURATION
# =====================================================================
SENDGRID_EMAIL_RECIPIENTS = [
    ('support@example.com', 'Support Team'),
    ('dev1@example.com', 'Developer One'),
    ('dev2@example.com', 'Developer Two'),
]
SENDGRID_FROM_EMAIL = ('alerts@example.com', 'Alert | M-Files Manage Data Extractor')

# =====================================================================
# VAULT-TEAM MAPPING
# =====================================================================
# Maps vault IDs (or parts of their names) to responsible team names
VAULT_TEAM_MAPPING = { 
    '1': "Team Alpha",
    '2': "Team Beta",
    '3': "Team Gamma",
    '4': "Team Delta",
    '5': "Team Epsilon",
    '6': "Team Zeta"
}
DEFAULT_TEAM = "Team Alpha" # Default team if no specific mapping is found

# =====================================================================
# M-FILES MANAGE CREDENTIALS
# =====================================================================
MFILES_SERVER_URL = os.getenv("MFILES_SERVER_URL")
MFILES_VAULT_GUID = os.getenv("MFILES_VAULT_GUID")
MFILES_USERNAME = os.getenv("MFILES_USERNAME")
MFILES_PASSWORD = os.getenv("MFILES_PASSWORD")

# Validate if credentials were loaded correctly
if not MFILES_USERNAME or not MFILES_PASSWORD:
    raise ValueError("Missing configurations: Define MFILES_USERNAME and MFILES_PASSWORD in the .env file.")

# =====================================================================
# NAVIGATION AND UPLOAD CONFIGURATIONS
# =====================================================================
MFILES_MANAGE_PREFIX = os.getenv("MFILES_MANAGE_PREFIX", "123") # Generic prefix
MANAGE_BASE_URL = f"https://manage.m-files.com/{MFILES_MANAGE_PREFIX}-{{}}/home"

MFILES_UPLOAD_CLASS_ID = 100 # Generic class ID

# 1. BASE TEMPLATE: Static metadata for all uploads
MFILES_METADATA_TEMPLATE = {
    "Subclass": "Extracted from Manage",
    "Account": "ExampleCorp",
    "Observation": "Generated Reports"
}

# 2. PROPERTY MAPPING: Names of dynamic properties in the Vault
MFILES_PROP_FILENAME = "Report (Py)"
MFILES_PROP_DATE = "Date"
MFILES_PROP_MONTH = "Month"

# =====================================================================
# CURRENT CSV HEADER STRUCTURE
# =====================================================================
HEADER_USERS = ['Account Name', 'Account Type', 'Email', 'Full Name', 'License Type', 'Information 1', 'Information 2', 'M-Files Manage role', 'State', 'Vault access', 'Username']
HEADER_VAULTS = ['Name', 'Environment', 'Enabled users', 'Objects', 'Object versions', 'File storage', 'Database size']
