import os
from typing import Any
from telegram import Update, Bot, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove
import json
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.database import Database
from misc import constants

load_dotenv()


class CommandHandler:
    bot: Bot
    update: Update
    chat_id: int
    db: Database

    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    async def decider(self, update: Update):
        # Decide where to go
        self.update = update
        self.chat_id = update.message.chat_id
        text = update.message.text
        client = MongoClient(os.getenv('MONGO_CONNECTION_URL'))
        self.db = client.telegram

        match text:
            case '/start':
                await self.start()
            case '/connect':
                await self.connect()
            case '/help':
                await self.help()
            case '/new_post':
                await self.new_post()
            case '/profile':
                await self.profile()
            case _:
                await self.default()

    async def connect(self):
        text = 'Lets connect me to your channel!\nHere are the two steps needed:\n\n<b>Step 1:</b> You have to add me as an admin to your channel with just the following permissions turned on:\n\t✅ Post Messages\n\t✅ Edit Messages\n\t✅ Delete Messages\n<b>Step 2:</b> Forward me any message from the channel'

        self.db.sessions.update_one({"chat_id": self.chat_id}, {
            "$set": {"question": constants.CONNECT_WITH_CHANNEL}}, upsert=True)

        await self.bot.send_message(text=text, chat_id=self.chat_id, parse_mode="HTML")
        await self.bot.send_message(text="I'm waiting...", chat_id=self.chat_id, parse_mode="HTML")

    async def default(self):
        text = f"""You are tripping! There is no command with this name."""
        await self.bot.send_message(text=text, chat_id=self.chat_id, parse_mode="HTML")

    async def start(self):
        text = f"""Hello there <b>{self.update.message.from_user.first_name}</b>, welcome to the <b>Telegram Content Management</b> bot. \
            I can help you manage your contents across different groups and channels.\n\nYou can control me by sending these commands:
        """
        with open('config/commands.json') as commands_file:
            commands_json = json.load(commands_file)

            for command in commands_json["commands"]:
                text += "\n/" + command['command'] + \
                    " - " + command['description']

        await self.register_user()
        await self.bot.send_message(text=text, chat_id=self.chat_id, parse_mode="HTML")

    async def help(self):
        text = 'Need help with commands?\nHere are list of commands you can use:\n'
        with open('config/commands.json') as commands_file:
            commands_json = json.load(commands_file)

            for command in commands_json["commands"]:
                text += "\n/" + command['command'] + \
                    " - " + command['description']

        await self.bot.send_message(text=text, chat_id=self.chat_id, parse_mode="HTML")

    async def new_post(self):
        self.db.sessions.update_one({"chat_id": self.chat_id}, {
            '$set': {"command": "/post", "question": constants.INSERT_POST_INFO, "data": {}}}, upsert=True)

        text = f"""Using the following attributes, please add detail information about your post"""
        reply_markup = constants.NEW_POST_INLINE_KEYBOARD

        await self.bot.send_message(text=text, chat_id=self.chat_id, reply_markup=reply_markup, parse_mode="HTML")

    async def register_user(self):
        user_from_db = self.db.users.find_one({"chat_id": self.chat_id})
        if user_from_db == None:
            self.db.users.insert_one(
                {
                    "chat_id": self.chat_id,
                    "name": self.update.message.from_user.first_name + " " + self.update.message.from_user.last_name,
                    "username": self.update.message.from_user.username,
                    "channels": [],
                    "groups": [],
                })

    async def profile(self):
        user_from_db = self.db.users.find_one({"chat_id": self.chat_id})
        text = f"Your profile info:\n\nName: {user_from_db['name']}\nUsername: @{user_from_db['username']}"

        if user_from_db['channels'] != []:
            text += "\nChannels: "
            for channel in user_from_db['channels']:
                text += f"@{channel}, ".rstrip(',')
        if user_from_db['groups'] != []:
            text += "\nGroups: "
            for group in user_from_db['groups']:
                text += f"@{group}, ".rstrip(',')

        await self.bot.send_message(text=text, chat_id=self.chat_id, parse_mode="HTML")
