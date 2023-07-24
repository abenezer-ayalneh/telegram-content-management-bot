import os
from typing import Self
from telegram import Update, Bot
from pymongo.database import Database
from pymongo import MongoClient
from dotenv import dotenv_values


class Root:
    _instance = None
    bot: Bot
    update: Update | None
    chat_id: int | None
    db: Database

    def __new__(self: type[Self]) -> Self:
        if self._instance is None:
            self._instance = super().__new__(self)
        return self._instance

    def __init__(self) -> None:
      # Assign the bot
      env = dotenv_values('.env')
      token = env['TELEGRAM_BOT_TOKEN']
      self.bot = Bot(token)

      # Assign the db
      client = MongoClient(os.getenv('MONGO_CONNECTION_URL'))
      self.db = client.telegram

    def set_update(self, update: Update):
      self.update = update
      self.chat_id = update.message.chat_id if update.message != None else update.callback_query.message.chat_id
