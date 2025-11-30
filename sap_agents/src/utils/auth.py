import os
import requests
from requests.auth import HTTPBasicAuth
import yaml

def load_config(config_path="config/sap_config.yaml"):
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)

def get_sap_session(config=None):
    """
    Creates a requests session with SAP authentication.
    Supports Basic Auth and API Key for now.
    """
    if config is None:
        # Fallback to env vars if no config object provided
        base_url = os.getenv("SAP_ODATA_URL")
        username = os.getenv("SAP_USERNAME")
        password = os.getenv("SAP_PASSWORD")
        api_key = os.getenv("SAP_API_KEY")
    else:
        base_url = config.get('base_url')
        username = config.get('username') or os.getenv("SAP_USERNAME")
        password = config.get('password') or os.getenv("SAP_PASSWORD")
        api_key = config.get('api_key') or os.getenv("SAP_API_KEY")

    session = requests.Session()
    
    if username and password:
        session.auth = HTTPBasicAuth(username, password)
    elif api_key:
        session.headers.update({"APIKey": api_key})
    
    # Common SAP headers
    session.headers.update({
        "Accept": "application/json",
        "Content-Type": "application/json"
    })
    
    return session, base_url
