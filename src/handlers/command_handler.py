import os
from telegram import Update, Bot, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove
import json
from dotenv import load_dotenv
from pymongo import MongoClient
from misc import constants

load_dotenv()


class CommandHandler:
    bot: Bot
    update: Update

    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    async def decider(self, update: Update):
        # Decide where to go
        self.update = update
        command = update.message.text

        match command:
            case '/start':
                await self.start()
            case '/help':
                await self.help()
            case '/new_post':
                await self.new_post()
            case _:
                await self.default()

    async def default(self):
        chat_id = self.update.message.from_user.id
        text = f"""You are tripping! There is no command with this name."""
        await self.bot.send_message(text=text, chat_id=chat_id, parse_mode="HTML")

    async def start(self):
        id = self.update.message.from_user.id
        text = f"""Hello there <b>{self.update.message.from_user.first_name}</b>, welcome to the <b>Telegram Content Management</b> bot. \
            Here are some of the things you can do with this bot:
        - Upload a post
        """
        await self.bot.send_message(text=text, chat_id=id, parse_mode="HTML")

    async def help(self):
        chat_id = self.update.message.from_user.id
        text = 'Need help with commands?\nHere are list of commands you can use:\n'
        with open('src/misc/commands.json') as commands_file:
            commands_json = json.load(commands_file)

            for command in commands_json["commands"]:
                text += "\n/" + command['command'] + \
                    " - " + command['description']

        await self.bot.send_message(text=text, chat_id=chat_id, parse_mode="HTML")

    async def new_post(self):
        client = MongoClient(os.getenv('MONGO_CONNECTION_URL'))
        db = client['telegram']
        sessions = db['sessions']

        sessions.update_one({"chat_id": self.update.message.chat_id}, {
            '$set': {"command": "/post", "question": constants.INSERT_POST_INFO, "data": {}}}, upsert=True)

        chat_id = self.update.message.from_user.id
        text = f"""Using the following attributes, please add detail information about your post"""
        reply_markup = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    text="Title", callback_data="new_post.title"),
                InlineKeyboardButton(text="Description",
                                     callback_data="new_post.description")
            ],
            [
                InlineKeyboardButton("Post ✅", callback_data="post")
            ]
        ])

        await self.bot.send_message(text=text, chat_id=chat_id, reply_markup=reply_markup, parse_mode="HTML")
