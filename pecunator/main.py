from database.models import Base
from database.database import engine
from bot.bot import bot
from handlers.commands import *

Base.metadata.create_all(engine)


bot.infinity_polling()
