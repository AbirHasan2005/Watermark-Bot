# (c) @AbirHasan2005

from configs import Config
from core.database import Database

db = Database(Config.DATABASE_URL, Config.BOT_USERNAME)