import json
import os
from helpers import crypto

from cryptography.fernet import Fernet

CHAT_INFO_FILENAME = "chat_info.json"

chat_info_ojb = {}

def save_chat_info():
  with open(CHAT_INFO_FILENAME, "w") as f:
    json.dump(chat_info_obj, f)


def update_username(new_username):
  global chat_info_obj
  chat_info_obj['username'] = crypto.encrypt(new_username)
  save_chat_info()


def update_webwork_password(new_password):
  global chat_info_obj
  chat_info_obj['webwork_password'] = crypto.encrypt(new_password)
  save_chat_info()


def update_main_password(new_password):
  global chat_info_obj
  chat_info_obj['main_password'] = crypto.encrypt(new_password)
  save_chat_info()


def get_chat_info():
  global chat_info_obj

  try:
    with open(CHAT_INFO_FILENAME) as f:
      chat_info = json.load(f)

  except FileNotFoundError:
    save_chat_info()

  return crypto.process_chat(chat_info)


def update_webworks(new_webworks):
  global chat_info_obj
  chat_info_obj['webworks'] = crypto.encrypt(json.dumps(new_webworks))
  save_chat_info()


def update_schedule(new_schedule):
  global chat_info_obj
  chat_info_obj['schedule'] = crypto.encrypt(json.dumps(new_schedule))
  save_chat_info()


def switch_notify_grades(switch):
  global chat_info_obj
  chat_info_obj['notify_grades'] = crypto.encrypt(switch)
  save_chat_info()


def update_grades(new_grades):
  global chat_info_obj
  chat_info_obj['grades'] = crypto.encrypt(json.dumps(new_grades))
  save_chat_info()


def update_schedule_notify_minutes(chat_id, new_minutes):
  global chat_info_obj
  chat_info_obj['schedule_notify_minutes'] = json.dumps(new_minutes)
  save_chat_info()
