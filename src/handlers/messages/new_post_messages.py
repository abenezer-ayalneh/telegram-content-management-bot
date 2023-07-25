from src.root import Root
from telegram import InlineKeyboardButton, InlineKeyboardMarkup


class NewPostMessages:
    root: Root

    def __init__(self) -> None:
        self.root = Root()

    async def update_post_attribute(self):
        # Get the attribute that is pending to be updated
        attribute = self.root.db.sessions.find_one(
            {"chat_id": self.root.chat_id})["attribute"]
        # Get the new value of the attribute
        attribute_value = self.root.update.message.text
        # Upsert the new attribute
        self.root.db.sessions.update_one({"chat_id": self.root.chat_id}, {
            "$set": {"question": None, f"data.{attribute}": attribute_value}}, upsert=True)

        text = f"""Success! {attribute} updated."""
        reply_markup = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    text="≪ Back to Post", callback_data="new_post.back_to_post"),
            ]
        ])

        await self.root.bot.send_message(text=text, chat_id=self.root.chat_id, reply_markup=reply_markup, parse_mode="HTML")
