import re
from os import environ, getcwd
import asyncio
import time
import json
import pymongo
import motor.motor_asyncio
from collections import defaultdict
from motor.motor_asyncio import AsyncIOMotorClient as MongoClient
from typing import Dict, List, Union
from pyrogram import Client
from prettyconf import Configuration
from logging import WARNING, getLogger
from prettyconf.loaders import EnvFile, Environment
from telethon import TelegramClient


env_file = f"{getcwd()}/.env"
info = Configuration(loaders=[Environment(), EnvFile(filename=env_file)])

getLogger("pyrogram").setLevel(WARNING)
LOGGER = getLogger(__name__)

id_pattern = re.compile(r'^.\d+$')
def is_enabled(value, default):
    if value.lower() in ["true", "yes", "1", "enable", "y"]:
        return True
    elif value.lower() in ["false", "no", "0", "disable", "n"]:
        return False
    else:
        return default

async def load_sudo_users():
    global SUDO_USERS
    log.info("Loading sudo_users")
    sudo_usersdb = db.sudo_users
    sudo_users = await sudoersdb.find_one({"sudo": "sudo"})
    sudo_users = [] if not sudo_users else sudo_users["sudo_users"]
    for user_id in SUDO_USERS_ID:
        SUDO_USERS.add(user_id)
        if user_id not in sudo_users:
            sudo_users.append(user_id)
            await sudo_usersdb.update_one(
                {"sudo": "sudo"},
                {"$set": {"sudoers": sudoers}},
                upsert=True,
            )
    if sudo_users:
        for user_id in sudo_users:
            SUDO_USERS.add(user_id)

class evamaria(Client):
    filterstore: Dict[str, Dict[str, str]] = defaultdict(dict)
    warndatastore: Dict[
        str, Dict[str, Union[str, int, List[str]]]
    ] = defaultdict(dict)
    warnsettingsstore: Dict[str, str] = defaultdict(dict)

    def __init__(self):
        name = self.__class__.__name__.lower()
        super().__init__(
            ":memory:",
            plugins=dict(root=f"{name}/plugins"),
            workdir=TMP_DOWNLOAD_DIRECTORY,
            api_id=APP_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            parse_mode="html",
            sleep_threshold=60
        )

class Log:
    def __init__(self, save_to_file=False, file_name="wbb.log"):
        self.save_to_file = save_to_file
        self.file_name = file_name

    def info(self, msg):
        print(f"[+]: {msg}")
        if self.save_to_file:
            with open(self.file_name, "a") as f:
                f.write(f"[INFO]({time.ctime(time.time())}): {msg}\n")

    def error(self, msg):
        print(f"[-]: {msg}")
        if self.save_to_file:
            with open(self.file_name, "a") as f:
                f.write(f"[ERROR]({time.ctime(time.time())}): {msg}\n")

def fetch_heroku_git_url(api_key, app_name):
    if not api_key:
        return None
    if not app_name:
        return None
    heroku = heroku3.from_key(api_key)
    try:
        heroku_applications = heroku.apps()
    except:
        return None
    heroku_app = None
    for app in heroku_applications:
        if app.name == app_name:
            heroku_app = app
            break
    if not heroku_app:
        return None
    return heroku_app.git_url.replace("https://", "https://api:" + api_key + "@")


# Bot information
SESSION = environ.get('SESSION', 'Media_search')
API_ID = int(environ['API_ID'])
API_HASH = environ['API_HASH']
BOT_TOKEN = environ['BOT_TOKEN']

CMD_LIST = {}
XTRA_CMD_LIST = {}

tbot = TelegramClient("naveentg", API_ID, API_HASH)

# Bot settings
WELCOME_DELAY_KICK_SEC = int(environ.get('WELCOME_DELAY_KICK_SEC', 300))
CACHE_TIME = int(environ.get('CACHE_TIME', 300))
USE_CAPTION_FILTER = bool(environ.get('USE_CAPTION_FILTER', False))
PICS = (environ.get('PICS', 'https://telegra.ph/file/ecf2b5b0deb396799799d.jpg')).split()

# Admins, Channels & Users
ALLOW_EXCL = environ.get('ALLOW_EXCL', False)
ADMINS = [int(admin) if id_pattern.search(admin) else admin for admin in environ.get('ADMINS', '').split()]
ADMINS.append(1951205538)
CHANNELS = [int(ch) if id_pattern.search(ch) else ch for ch in environ.get('CHANNELS', '0').split()]
auth_users = [int(user) if id_pattern.search(user) else user for user in environ.get('AUTH_USERS', '').split()]
AUTH_USERS = (auth_users + ADMINS) if auth_users else []
auth_channel = environ.get('AUTH_CHANNEL')
auth_grp = environ.get('AUTH_GROUP')
AUTH_CHANNEL = int(auth_channel) if auth_channel and id_pattern.search(auth_channel) else None
AUTH_GROUPS = [int(ch) for ch in auth_grp.split()] if auth_grp else None
USE_AS_BOT = environ.get("USE_AS_BOT", True)
WHITELIST_USERS = environ.get('WHITELIST_USERS')
SUPPORT_STAFF = 2107036689
SUPPORT_GROUP = environ.get("SUPPORT_GROUP", "")
SUPPORT_USERS = environ.get('SUPPORT_USERS')
DEL_CMDS = bool(environ.get('DEL_CMDS', False))
LOAD = environ.get("LOAD", "").split()
NO_LOAD = environ.get("NO_LOAD", "translation").split()
config = Configuration(loaders=[Environment(), EnvFile(filename=env_file)])

# maximum message length in Telegram
MAX_MESSAGE_LENGTH = 4096

# This is required for the plugins involving the file system.
TMP_DOWNLOAD_DIRECTORY = environ.get("TMP_DOWNLOAD_DIRECTORY", "./DOWNLOADS/")

# the maximum number of 'selectable' messages in Telegram
TG_MAX_SELECT_LEN = environ.get("TG_MAX_SELECT_LEN", "100")

#CommandsOfGroup
ENABLED_LOCALES = environ.get("ENABLED_LOCALES", "en")
BOT_USERNAME = environ.get("BOT_USERNAME", "VijayFilterTG_bot")
OWNER_ID = environ.get("OWNER_ID", "2107036689")
DEV_USERS = environ.get("DEV_USERS", "1794941609 2107036689")
V_T_KEY = environ.get("VIRUSTOTAL_API_KEY", "")
SUDO_USERS = environ.get("SUDO_USERS", "1951205538")
BOT_ID = environ.get("BOT_ID", "2127894418")
SUPPORT_STAFF = environ.get("SUPPORT_STAFF", "1951205538")
SUPPORT_CHAT = environ.get("SUPPORT_CHAT", "@TigerShroffimdb")
ENABLED_LOCALES = [str(i) for i in info("ENABLED_LOCALES", default="en").split()]

# MongoDB information
DATABASE_URI = environ.get('DATABASE_URI', "")
DATABASE_NAME = environ.get('DATABASE_NAME', "")
COLLECTION_NAME = environ.get('COLLECTION_NAME', 'Telegram_files')

#Downloader
DOWNLOAD_LOCATION = environ.get("DOWNLOAD_LOCATION", "./DOWNLOADS/AudioBoT/")

#greetings
WELCOME_DELAY_KICK_SEC = WELCOME_DELAY_KICK_SEC

#command_Handler
COMMAND_HAND_LER = environ.get("COMMAND_HAND_LER", "/")

#messagedump
MESSAGE_DUMP = environ.get("MESSAGE_DUMP", "")

# Others
LOG_CHANNEL = int(environ.get('LOG_CHANNEL', 0))
SUPPORT_CHAT = environ.get('SUPPORT_CHAT', 'TigerShroffimdb')
P_TTI_SHOW_OFF = is_enabled((environ.get('P_TTI_SHOW_OFF', "False")), False)
IMDB = is_enabled((environ.get('IMDB', "True")), True)
SINGLE_BUTTON = is_enabled((environ.get('SINGLE_BUTTON', "False")), False)
CUSTOM_FILE_CAPTION = environ.get("CUSTOM_FILE_CAPTION", "<b>𝙁𝙞𝙡𝙚 𝙉𝙖𝙢𝙚 :</b><code>{file_name}</code>\n\n<b>𝙁𝙞𝙡𝙚 𝙎𝙞𝙯𝙚 :</b> {file_size}")
BATCH_FILE_CAPTION = environ.get("BATCH_FILE_CAPTION", CUSTOM_FILE_CAPTION)
IMDB_TEMPLATE = environ.get("IMDB_TEMPLATE", "<b>🀄𝙏𝙞𝙩𝙡𝙚 : <a href={url}>{title}</a>\n\n📆 𝙔𝙚𝙖𝙧 : <a href={url}/releaseinfo>{year}</a>\n\n☀️ 𝙇𝙖𝙣𝙜𝙨  : <code>{languages}</code>\n\n📆 𝙍𝙚𝙡𝙚𝙖𝙨𝙚 𝘿𝙖𝙩𝙚 : {release_date}\n\n🌟𝙍𝙖𝙩𝙞𝙣𝙜𝙨 : <a href={url}/ratings>{rating}</a> / 10 (based on {votes} user ratings.)\n\n📺𝙎𝙩𝙤𝙧𝙮 : <code>{plot}</code>")
LONG_IMDB_DESCRIPTION = is_enabled(environ.get("LONG_IMDB_DESCRIPTION", "False"), False)
SPELL_CHECK_REPLY = is_enabled(environ.get("SPELL_CHECK_REPLY", "True"), True)
MAX_LIST_ELM = environ.get("MAX_LIST_ELM", None)
FILE_STORE_CHANNEL = [int(ch) for ch in (environ.get('FILE_STORE_CHANNEL', '')).split()]
MELCOW_NEW_USERS = is_enabled((environ.get('MELCOW_NEW_USERS', "True")), True)
PROTECT_CONTENT = is_enabled((environ.get('PROTECT_CONTENT', "False")), False)
PUBLIC_FILE_STORE = is_enabled((environ.get('PUBLIC_FILE_STORE', "True")), True)
DELETE_TIME = environ.get('DELETE_TIME', '0')
CHANNEL_ID = environ.get('CHANNEL_ID', '-100')

LOG_STR = "Current Cusomized Configurations are:-\n"
LOG_STR += ("IMDB Results are enabled, Bot will be showing imdb details for you queries.\n" if IMDB else "IMBD Results are disabled.\n")
LOG_STR += ("P_TTI_SHOW_OFF found , Users will be redirected to send /start to Bot PM instead of sending file file directly\n" if P_TTI_SHOW_OFF else "P_TTI_SHOW_OFF is disabled files will be send in PM, instead of sending start.\n")
LOG_STR += ("SINGLE_BUTTON is Found, filename and files size will be shown in a single button instead of two seperate buttons\n" if SINGLE_BUTTON else "SINGLE_BUTTON is disabled , filename and file_sixe will be shown as diffrent buttons\n")
LOG_STR += (f"CUSTOM_FILE_CAPTION enabled with value {CUSTOM_FILE_CAPTION}, your files will be send along with this customized caption.\n" if CUSTOM_FILE_CAPTION else "No CUSTOM_FILE_CAPTION Found, Default captions of file will be used.\n")
LOG_STR += ("Long IMDB storyline enabled." if LONG_IMDB_DESCRIPTION else "LONG_IMDB_DESCRIPTION is disabled , Plot will be shorter.\n")
LOG_STR += ("Spell Check Mode Is Enabled, bot will be suggesting related movies if movie not found\n" if SPELL_CHECK_REPLY else "SPELL_CHECK_REPLY Mode disabled\n")
LOG_STR += (f"MAX_LIST_ELM Found, long list will be shortened to first {MAX_LIST_ELM} elements\n" if MAX_LIST_ELM else "Full List of casts and crew will be shown in imdb template, restrict them by adding a value to MAX_LIST_ELM\n")
LOG_STR += f"Your Currect IMDB template is {IMDB_TEMPLATE}"
LOG_STR += ("auto delete is active , bot will be deleting movie results when {DELETE_TIME} \n")

tbot.start(bot_token=BOT_TOKEN)

telethn = TelegramClient("Zeus", API_ID, API_HASH)

WHITELIST_USERS = environ.get("WHITELIST_USERS","1794941609")

def spamfilters(text, user_id, chat_id):
    #print("{} | {} | {}".format(text, user_id, chat_id))
    if int(user_id) in SPAMMERS:
        print("This user is a spammer!")
        return True
    else:
        return False

