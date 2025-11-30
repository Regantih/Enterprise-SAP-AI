import os
import json
import time
import requests
import base64

class SAPDocumentClient:
    def __init__(self, service_key_path=None):
        self.service_key = self._load_service_key(service_key_path)
        self.token = None
        self.token_expires_at = 0

    def _load_service_key(self, path):
        # Try env var first
        env_key = os.getenv("SAP_DOX_SERVICE_KEY")
        if env_key:
            return json.loads(env_key)
        
        # Try file path
        if path and os.path.exists(path):
            with open(path, 'r') as f:
                return json.load(f)
        
        return None

    def _get_token(self):
        if not self.service_key:
            raise ValueError("No Service Key found.")

        if self.token and time.time() < self.token_expires_at:
            return self.token

        uaa = self.service_key['uaa']
        client_id = uaa['clientid']
        client_secret = uaa['clientsecret']
        url = uaa['url'] + '/oauth/token'

        response = requests.post(
            url,
            data={'grant_type': 'client_credentials'},
            auth=(client_id, client_secret)
        )
        response.raise_for_status()
        data = response.json()
        self.token = data['access_token']
        self.token_expires_at = time.time() + data['expires_in'] - 60
        return self.token

    def process_document(self, file_path):
        """
        Full workflow: Upload -> Poll -> Extract
        """
        if not self.service_key:
            print("⚠️ No SAP Service Key. Skipping real DOX call.")
            return None

        token = self._get_token()
        base_url = self.service_key['url'] + '/document-information-extraction/v1'
        
        # 1. Upload
        print(f"   [SAP DOX] Uploading {os.path.basename(file_path)}...")
        with open(file_path, 'rb') as f:
            files = {'file': (os.path.basename(file_path), f, 'application/pdf')}
            headers = {'Authorization': f'Bearer {token}'}
            payload = {
                'options': json.dumps({
                    'extraction': {
                        'headerFields': ['documentNumber', 'grossAmount', 'currencyCode', 'senderName', 'documentDate'],
                        'lineItemFields': ['description', 'quantity', 'unitOfMeasure', 'unitPrice', 'netAmount']
                    },
                    'clientId': 'default'
                })
            }
            
            resp = requests.post(f"{base_url}/document/jobs", headers=headers, files=files, data=payload)
            resp.raise_for_status()
            job_id = resp.json()['id']

        # 2. Poll
        print(f"   [SAP DOX] Polling job {job_id}...")
        status = 'PENDING'
        while status in ['PENDING', 'RUNNING']:
            time.sleep(2)
            resp = requests.get(f"{base_url}/document/jobs/{job_id}", headers=headers)
            resp.raise_for_status()
            status = resp.json()['status']
            print(f"   [SAP DOX] Status: {status}")

        if status != 'DONE':
            raise Exception(f"Job failed with status: {status}")

        # 3. Get Results
        # The result is already in the polling response for DOX v1
        extraction = resp.json()['extraction']
        return self._format_results(extraction)

    def _format_results(self, extraction):
        header = extraction.get('headerFields', [])
        items = extraction.get('lineItems', [])
        
        summary = "--- SAP DOCUMENT EXTRACTION RESULTS ---\n"
        for field in header:
            if field['value']:
                summary += f"{field['name']}: {field['value']}\n"
        
        summary += "\nLine Items:\n"
        for row in items:
            line_str = []
            for col in row:
                if col['value']:
                    line_str.append(f"{col['name']}: {col['value']}")
            summary += " - " + ", ".join(line_str) + "\n"
            
        return summary
