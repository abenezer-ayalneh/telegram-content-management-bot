import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, Bot
from dotenv import load_dotenv
from pymongo import MongoClient
from misc import constants

load_dotenv()


class MessageHandler:
    bot: Bot
    update: Update
    client = MongoClient(os.getenv('MONGO_CONNECTION_URL'))
    db = client['telegram']

    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    async def decider(self, update: Update):
        # Decide where to go
        self.update = update
        chat_id = update.message.chat_id
        session = self.db.sessions.find_one({"chat_id": chat_id})
        question = session["question"]

        match question:
            case 'update_post_title':
                await self.update_post_title()
            case _:
                await self.default()

    async def update_post_title(self):
        chat_id = self.update.message.from_user.id
        title = self.update.message.text
        text = f"""Success! Title updated."""
        self.db.sessions.update_one({"chat_id": chat_id}, {
                                   "$set": {"question": None, "data.title": title}})
        reply_markup = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    text="≪ Back to Post", callback_data="new_post.back_to_post"),
            ]
        ])
        await self.bot.send_message(text=text, chat_id=chat_id, reply_markup=reply_markup, parse_mode="HTML")

    async def default(self):
        id = self.update.message.from_user.id
        text = f"""Wrong command/message on the wrong time!"""
        await self.bot.send_message(text=text, chat_id=id, parse_mode="HTML")
