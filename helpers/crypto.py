from cryptography.fernet import Fernet
import json
import os

SECRET = os.environ['SECRET'].encode()
print("python - crypto: {}".format(os.environ))
print("{} {}".format(SECRET, os.environ['SECRET']))
cipher_suite = Fernet(SECRET)

def encrypt(content):
  return cipher_suite.encrypt(content.encode()).decode()

def decrypt(content):
  return cipher_suite.decrypt(content.encode()).decode()

def process_chat(chat):
  encrypted_fields = {
    'username': False,
    'main_password': False,
    'webwork_password': False,
    'webworks': True,
    'schedule': True,
    'grades': True
  }
  for field, require_loads in encrypted_fields.items():
    if field in chat:
      chat[field] = decrypt(chat[field])

      if require_loads:
        chat[field] = json.loads(chat[field])
  return chat
