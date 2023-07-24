import json
from src.root import Root


class StartCommand:
    root: Root

    def __init__(self):
        self.root = Root()

    async def start(self):
        text = f"""Hello there <b>{self.root.update.message.from_user.first_name}</b>, welcome to the <b>Telegram Content Management</b> bot. \
            I can help you manage your contents across different groups and channels.\n\nYou can control me by sending these commands:
        """
        with open('config/commands.json') as commands_file:
            commands_json = json.load(commands_file)

            for command in commands_json["commands"]:
                text += "\n/" + command['command'] + \
                    " - " + command['description']

        await self.register_user()
        await self.root.bot.send_message(text=text, chat_id=self.root.chat_id, parse_mode="HTML")

    async def register_user(self):
        user_from_db = self.root.db.users.find_one(
            {"chat_id": self.root.chat_id})
        if user_from_db == None:
            self.root.db.users.insert_one(
                {
                    "chat_id": self.root.chat_id,
                    "name": self.root.update.message.from_user.first_name + " " + self.root.update.message.from_user.last_name,
                    "username": self.root.update.message.from_user.username,
                    "channels": [],
                    "groups": [],
                })
