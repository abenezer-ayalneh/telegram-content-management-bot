import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, Bot
from telegram._message import Message
from dotenv import load_dotenv
from pymongo import MongoClient
from misc import constants
from src.root import Root

load_dotenv()


class MessageDecider:
    root: Root

    def __init__(self) -> None:
        self.root = Root()

    async def decider(self, update: Update):
        # Decide where to go
        self.update = update
        self.message = update.message
        self.chat_id = update.message.chat_id
        session = self.db.sessions.find_one({"chat_id": self.chat_id})

        if session != None and session['question'] != None:
            question = session["question"]

            match question:
                case constants.UPDATE_POST_ATTRIBUTE:
                    await self.update_post_attribute()
                case constants.CONNECT_WITH_CHANNEL:
                    await self.connect_with_channel()
                case _:
                    await self.default()
        else:
            await self.default()

    async def connect_with_channel(self):
        self.db.users.update_one({"chat_id": self.chat_id}, {
            "$push": {self.message.forward_from_chat.type+'s': self.message.forward_from_chat.id}}, upsert=True)

        text = "<b>Connection done!</b> 📡\nNow I can post, edit and delete posts in you channel"
        await self.bot.send_message(text=text, chat_id=self.chat_id, parse_mode="HTML")

    async def update_post_attribute(self):
        # Get the attribute that is pending to be updated
        attribute = self.db.sessions.find_one(
            {"chat_id": self.chat_id})["attribute"]
        # Get the new value of the attribute
        attribute_value = self.update.message.text
        # Upsert the new attribute
        self.db.sessions.update_one({"chat_id": self.chat_id}, {
            "$set": {"question": None, f"data.{attribute}": attribute_value}}, upsert=True)

        text = f"""Success! {attribute} updated."""
        reply_markup = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    text="≪ Back to Post", callback_data="new_post.back_to_post"),
            ]
        ])

        await self.bot.send_message(text=text, chat_id=self.chat_id, reply_markup=reply_markup, parse_mode="HTML")

    async def default(self):
        text = f"""Wrong command/message or the wrong time!"""
        await self.bot.send_message(text=text, chat_id=self.chat_id, parse_mode="HTML")
