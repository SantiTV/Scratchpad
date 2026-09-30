import os
import uuid
from flask import Flask, request, jsonify, send_from_directory
from dotenv import load_dotenv
from googleapiclient.discovery import build
from google.oauth2 import service_account

load_dotenv("config.env")

app = Flask(__name__)

# Config
VAULT_PATH = os.getenv("OBSIDIAN_VAULT_PATH", "./vault")
GD_FOLDER_ID = os.getenv("GOOGLE_DRIVE_FOLDER_ID")
CREDENTIALS_FILE = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "credentials.json")

# Temporary storage for notes before sync
TEMP_STORAGE = "temp_notes"
if not os.path.exists(TEMP_STORAGE):
    os.makedirs(TEMP_STORAGE)

if not os.path.exists(VAULT_PATH):
    os.makedirs(VAULT_PATH)

def get_drive_service():
    """Authenticates with Google Drive API using a service account."""
    try:
        creds = service_account.Credentials.from_service_account_file(
            CREDENTIALS_FILE, 
            scopes=['https://www.googleapis.com/auth/drive.file']
        )
        return build('drive', 'v3', credentials=creds)
    except Exception as e:
        print(f"Google Drive Auth Error: {e}")
        return None

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/save', methods=['POST'])
def save_note():
    """Saves a note to temporary storage."""
    data = request.json
    content = data.get('content')
    title = data.get('title', 'Untitled')
    
    if not content:
        return jsonify({"error": "Content is required"}), 400

    # Safe filename
    filename = f"{title}.md".replace(" ", "_")
    filepath = os.path.join(TEMP_STORAGE, filename)
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    
    return jsonify({"status": "success", "filename": filename})

@app.route('/list', methods=['GET'])
def list_notes():
    """Lists files in the temporary storage."""
    files = [f for f in os.listdir(TEMP_STORAGE) if f.endswith('.md')]
    return jsonify({"files": files})

@app.route('/sync', methods=['POST'])
def sync_notes():
    """Syncs selected notes to Local (Obsidian) and/or Cloud (GDrive)."""
    data = request.json
    files_to_sync = data.get('files', [])
    targets = data.get('targets', []) # ['local', 'cloud']

    if not files_to_sync:
        return jsonify({"error": "No files selected"}), 400

    results = {"local": [], "cloud": []}

    for filename in files_to_sync:
        src_path = os.path.join(TEMP_STORAGE, filename)
        if not os.path.exists(src_path):
            continue

        # LOCAL SYNC (Obsidian)
        if 'local' in targets:
            try:
                dest_path = os.path.join(VAULT_PATH, filename)
                with open(src_path, 'r', encoding='utf-8') as f_in:
                    content = f_in.read()
                with open(dest_path, 'w', encoding='utf-8') as f_out:
                    f_out.write(content)
                results["local"].append(filename)
            except Exception as e:
                print(f"Local Sync Error {filename}: {e}")

        # CLOUD SYNC (Google Drive)
        if 'cloud' in targets:
            try:
                service = get_drive_service()
                if service:
                    file_metadata = {
                        'name': filename,
                        'parents': [GD_FOLDER_ID] if GD_FOLDER_ID else []
                    }
                    # Upload the file
                    service.files().create(
                        body=file_metadata,
                        media_body=src_path,
                        fields='id'
                    ).execute()
                    results["cloud"].append(filename)
            except Exception as e:
                print(f"Cloud Sync Error {filename}: {e}")

    return jsonify(results)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
