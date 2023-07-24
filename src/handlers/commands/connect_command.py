from src.root import Root
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from misc import constants

class ConnectCommand:
    root: Root

    def __init__(self):
        self.root = Root()

    async def connect(self):
        user = self.root.db.users.find_one({"chat_id": self.root.chat_id})

        if user != None and user['channels'] != None and len(user['channels']) > 0:
            text = f"You already have a channel that I am connected to.\nDo you want to change it?"
            reply_markup = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton('Yes ✅', callback_data=constants.CHANGE_CHANNEL),
                    InlineKeyboardButton('No ❌', callback_data=constants.CHANGE_CHANNEL),
                ]
            ])

            await self.root.bot.send_message(text=text, chat_id=self.root.chat_id, reply_markup=reply_markup, parse_mode="HTML")
        else:
            text = 'Lets connect me to your channel!\nHere are the two steps needed:\n\n<b>Step 1:</b> You have to add me as an admin to your channel with just the following permissions turned on:\n\t✅ Post Messages\n\t✅ Edit Messages\n\t✅ Delete Messages\n<b>Step 2:</b> Forward me any message from the channel'

            self.root.db.sessions.update_one({"chat_id": self.root.chat_id}, {
                "$set": {"question": constants.CONNECT_WITH_CHANNEL}}, upsert=True)

            await self.root.bot.send_message(text=text, chat_id=self.root.chat_id, parse_mode="HTML")
            await self.root.bot.send_message(text="I'm waiting...", chat_id=self.root.chat_id, parse_mode="HTML")