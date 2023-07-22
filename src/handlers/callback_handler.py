import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, Bot
from dotenv import load_dotenv
from pymongo import MongoClient
from misc import constants
from src.handlers.command_handler import CommandHandler

load_dotenv()

class CallbackHandler:
    bot: Bot
    update: Update
    chat_id: int
    client = MongoClient(os.getenv('MONGO_CONNECTION_URL'))
    db = client['telegram']

    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    async def decider(self, update: Update):
        # Decide where to go
        self.update = update
        self.chat_id = update.callback_query.from_user.id
        callback_data = update.callback_query.data

        match callback_data:
            case "new_post.update.title" | "new_post.update.description" | "new_post.update.images":
                await self.new_post_attribute()
            case "new_post.back_to_post":
                await self.new_post_back_to_post()
            case "new_post.post_confirmation":
                await self.post_confirmation()
            case "new_post.confirm_post":
                await self.confirm_post()
            case constants.CHANGE_CHANNEL:
                await self.change_channel()
            case _:
                await self.default()

    async def change_channel(self):
        text = 'Lets connect me to your new channel!\nHere are the two steps needed:\n\n<b>Step 1:</b> You have to add me as an admin to your channel with just the following permissions turned on:\n\t✅ Post Messages\n\t✅ Edit Messages\n\t✅ Delete Messages\n<b>Step 2:</b> Forward me any message from the channel'

        self.db.sessions.update_one({"chat_id": self.chat_id}, {
            "$set": {"question": constants.CONNECT_WITH_CHANNEL}}, upsert=True)

        await self.bot.send_message(text=text, chat_id=self.chat_id, parse_mode="HTML")
        await self.bot.send_message(text="I'm waiting...", chat_id=self.chat_id, parse_mode="HTML")

    async def default(self):
        text = """This button doesn't have a purpose yet! Try another"""
        await self.bot.send_message(text=text, chat_id=self.chat_id, parse_mode="HTML")

    async def new_post_attribute(self):
        message_id = self.update.callback_query.message.id
        attribute = self.update.callback_query.data.split(".")[-1]
        text = f"""Ok. Send me the <b>{attribute}</b> of your post."""

        await self.bot.edit_message_text(text=text, chat_id=self.chat_id, message_id=message_id, parse_mode="HTML")
        self.db.sessions.update_one({"chat_id": self.chat_id}, {
            '$set': {"question": constants.UPDATE_POST_ATTRIBUTE, "attribute": attribute}}, upsert=True)

    async def new_post_back_to_post(self):
        text = f"""Using the following attributes, please add detail information about your post\n"""
        message_id = self.update.callback_query.message.id

        session = self.db.sessions.find_one({"chat_id": self.chat_id})
        for key, value in session['data'].items():
            text += f"\n<b>{key.upper()}</b>: {value}"

        reply_markup = constants.NEW_POST_INLINE_KEYBOARD

        await self.bot.edit_message_text(text=text, chat_id=self.chat_id, message_id=message_id, reply_markup=reply_markup, parse_mode="HTML")

    async def post_confirmation(self):
        text = f"""Here are the details of your post so far:\n"""
        message_id = self.update.callback_query.message.id

        session = self.db.sessions.find_one({"chat_id": self.chat_id})
        for key, value in session['data'].items():
            text += f"\n<b>{key.upper()}</b>: {value}"

        text += '\n\n<b>Are you sure you want to post?</b>'
        reply_markup = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    text="✅ Yes", callback_data="new_post.confirm_post"),
                InlineKeyboardButton(text="❌ No",
                                     callback_data="new_post.back_to_post")
            ]
        ])

        await self.bot.edit_message_text(text=text, chat_id=self.chat_id, message_id=message_id, reply_markup=reply_markup, parse_mode="HTML")

    async def confirm_post(self):
        message_id = self.update.callback_query.message.id
        user = self.db.users.find_one({"chat_id": self.chat_id})

        if user != None and user['channels'] != None and len(user['channels']) > 0:
            channel_id = user['channels'][0]
            session = self.db.sessions.find_one({"chat_id": self.chat_id})
            data = session['data']
            self.db.posts.insert_one(
                {"chat_id": self.chat_id, **data, "status": True})

            post = ''
            for key, value in data.items():
                post += f"\n<b>{key.upper()}</b>: {value}"

            await self.bot.send_message(text=post, chat_id=channel_id, parse_mode="HTML")

            text = f"""Post successfully uploaded! 🎉"""
            await self.bot.edit_message_text(text=text, chat_id=self.chat_id, message_id=message_id, parse_mode="HTML")
        else:
            text = f"""You haven't connected me with your channel ☹️"""

            await self.bot.edit_message_text(text=text, chat_id=self.chat_id, message_id=message_id, parse_mode="HTML")
