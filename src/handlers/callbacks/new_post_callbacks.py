from src.root import Root
from misc import constants
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

class NewPostCallbacks:
    root: Root

    def __init__(self):
        self.root = Root()

    async def update_attribute(self):
        message_id = self.root.update.callback_query.message.id
        attribute = self.root.update.callback_query.data.split(".")[-1]
        text = f"""Ok. Send me the <b>{attribute}</b> of your post."""

        await self.root.bot.edit_message_text(text=text, chat_id=self.root.chat_id, message_id=message_id, parse_mode="HTML")
        self.root.db.sessions.update_one({"chat_id": self.root.chat_id}, {
            '$set': {"question": constants.UPDATE_POST_ATTRIBUTE, "attribute": attribute}}, upsert=True)

    async def back_to_post(self):
        text = f"""Using the following attributes, please add detail information about your post\n"""
        message_id = self.root.update.callback_query.message.id

        session = self.root.db.sessions.find_one({"chat_id": self.root.chat_id})
        for key, value in session['data'].items():
            text += f"\n<b>{key.upper()}</b>: {value}"

        reply_markup = constants.NEW_POST_INLINE_KEYBOARD

        await self.root.bot.edit_message_text(text=text, chat_id=self.root.chat_id, message_id=message_id, reply_markup=reply_markup, parse_mode="HTML")

    async def post_confirmation(self):
        text = f"""Here are the details of your post so far:\n"""
        message_id = self.root.update.callback_query.message.id

        session = self.root.db.sessions.find_one({"chat_id": self.root.chat_id})
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

        await self.root.bot.edit_message_text(text=text, chat_id=self.root.chat_id, message_id=message_id, reply_markup=reply_markup, parse_mode="HTML")

    async def confirm_post(self):
        message_id = self.root.update.callback_query.message.id
        user = self.root.db.users.find_one({"chat_id": self.root.chat_id})

        if user != None and user['channels'] != None and len(user['channels']) > 0:
            channel_id = user['channels'][0]
            session = self.root.db.sessions.find_one({"chat_id": self.root.chat_id})
            data = session['data']
            self.root.db.posts.insert_one(
                {"chat_id": self.root.chat_id, **data, "status": True})

            post = ''
            for key, value in data.items():
                post += f"\n<b>{key.upper()}</b>: {value}"

            await self.root.bot.send_message(text=post, chat_id=channel_id, parse_mode="HTML")

            text = f"""Post successfully uploaded! 🎉"""
            await self.root.bot.edit_message_text(text=text, chat_id=self.root.chat_id, message_id=message_id, parse_mode="HTML")
        else:
            text = f"""You haven't connected me with your channel ☹️"""

            await self.root.bot.edit_message_text(text=text, chat_id=self.root.chat_id, message_id=message_id, parse_mode="HTML")
