from src.root import Root


class ChannelMessages:
    root: Root

    def __init__(self) -> None:
        self.root = Root()
    
    async def connect_with_channel(self):
        self.root.db.users.update_one({"chat_id": self.root.chat_id}, {
            "$push": {self.root.message.forward_from_chat.type+'s': self.root.message.forward_from_chat.id}}, upsert=True)

        text = "<b>Connection done!</b> 📡\nNow I can post, edit and delete posts in you channel"
        await self.root.bot.send_message(text=text, chat_id=self.root.chat_id, parse_mode="HTML")