# ------------------------- #
# Don't Remove Credit 
# Ask Doubt @AU_Bot_Discussion 
# Owner @Mr_Mohammed_29 
# ------------------------- #

import uuid

files_db = {}
user_last = {}

def save_file(file_id, file_name, file_size):
    key = str(uuid.uuid4())[:8]

    files_db[key] = {
        "file_id": file_id,
        "file_name": file_name,
        "file_size": file_size,
        "langs": {},
        "subs": {}
    }
    return key

def get_file(key):
    return files_db.get(key)

def add_language(key, lang, file_id):
    files_db[key]["langs"][lang] = file_id

def add_subtitle(key, lang, content):
    files_db[key]["subs"][lang] = content

def set_user_last(user_id, key):
    user_last[user_id] = key

def get_user_last(user_id):
    return user_last.get(user_id)

# ------------------------- #
# Don't Remove Credit 
# Ask Doubt @AU_Bot_Discussion 
# Owner @Mr_Mohammed_29 
# ------------------------- #
