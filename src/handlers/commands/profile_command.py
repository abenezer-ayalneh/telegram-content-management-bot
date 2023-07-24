from src.root import Root


class ProfileCommand:
    root: Root

    def __init__(self):
        self.root = Root()

    async def profile(self):
        user_from_db = self.root.db.users.find_one({"chat_id": self.root.chat_id})
        text = f"Your profile info:\n\nName: {user_from_db['name']}\nUsername: @{user_from_db['username']}"

        if user_from_db['channels'] != []:
            text += "\nChannels: "
            for channel in user_from_db['channels']:
                text += f"@{channel}, ".rstrip(',')
        if user_from_db['groups'] != []:
            text += "\nGroups: "
            for group in user_from_db['groups']:
                text += f"@{group}, ".rstrip(',')

        await self.root.bot.send_message(text=text, chat_id=self.root.chat_id, parse_mode="HTML")