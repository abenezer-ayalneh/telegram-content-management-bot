import json
from telegram import Update

class StartCommand:
    update: Update
    chat_id: int

    async def start(self):
        text = f"""Hello there <b>{self.update.message.from_user.first_name}</b>, welcome to the <b>Telegram Content Management</b> bot. \
            I can help you manage your contents across different groups and channels.\n\nYou can control me by sending these commands:
        """
        with open('config/commands.json') as commands_file:
            commands_json = json.load(commands_file)

            for command in commands_json["commands"]:
                text += "\n/" + command['command'] + \
                    " - " + command['description']

        await self.register_user()
        await self.bot.send_message(text=text, chat_id=self.chat_id, parse_mode="HTML")
    