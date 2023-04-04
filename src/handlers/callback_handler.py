import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, Bot
from dotenv import load_dotenv
from pymongo import MongoClient
from misc import constants

load_dotenv()


class CallbackHandler:
    bot: Bot
    update: Update
    client = MongoClient(os.getenv('MONGO_CONNECTION_URL'))
    db = client['telegram']

    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    async def decider(self, update: Update):
        # Decide where to go
        self.update = update
        callback_data = update.callback_query.data

        match callback_data:
            case "new_post.title":
                await self.new_post_title()
            case "new_post.back_to_post":
                await self.new_post_back_to_post()
            case _:
                await self.default()

    async def default(self):
        chat_id = self.update.callback_query.from_user.id
        text = """This button doesn't have a purpose yet! Try another"""
        await self.bot.send_message(text=text, chat_id=chat_id, parse_mode="HTML")

    async def new_post_title(self):
        chat_id = self.update.callback_query.from_user.id
        message_id = self.update.callback_query.message.id
        text = """Ok. Send me the title of your post."""

        await self.bot.edit_message_text(text=text, chat_id=chat_id, message_id=message_id, parse_mode="HTML")
        self.db.sessions.update_one({"chat_id": chat_id}, {
            '$set': {"question": constants.UPDATE_POST_TITLE}})
        
    async def new_post_back_to_post(self):
        chat_id = self.update.callback_query.from_user.id
        text = f"""Using the following attributes, please add detail information about your post\n"""
        message_id = self.update.callback_query.message.id

        session = self.db.sessions.find_one({"chat_id": chat_id})
        for key, value in session['data'].items():
            text += f"\n<b>{key.upper()}</b>: {value}"
        
        
        reply_markup = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    text="Title", callback_data="new_post.title"),
                InlineKeyboardButton(text="Description",
                                     callback_data="new_post.description")
            ],
            [
                InlineKeyboardButton("Post ✅", callback_data="new_post.post")
            ]
        ])

        await self.bot.edit_message_text(text=text, chat_id=chat_id, message_id=message_id, reply_markup=reply_markup, parse_mode="HTML")