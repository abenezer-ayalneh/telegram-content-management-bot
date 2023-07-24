import json
from src.root import Root


class HelpCommand:
    root: Root

    def __init__(self):
        self.root = Root()

    async def help(self):
        text = 'Need help with commands?\nHere are list of commands you can use:\n'
        with open('config/commands.json') as commands_file:
            commands_json = json.load(commands_file)

            for command in commands_json["commands"]:
                text += "\n/" + command['command'] + \
                    " - " + command['description']

        await self.root.bot.send_message(text=text, chat_id=self.root.chat_id, parse_mode="HTML")
