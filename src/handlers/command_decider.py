from src.handlers.commands.connect_command import ConnectCommand
from src.handlers.commands.help_command import HelpCommand
from src.handlers.commands.new_post_command import NewPostCommand
from src.handlers.commands.profile_command import ProfileCommand
from src.handlers.commands.start_command import StartCommand
from dotenv import load_dotenv
from src.root import Root

load_dotenv()


class CommandDecider:
    # Classes
    root: Root
    start_command: StartCommand
    help_command: HelpCommand
    new_post_command: NewPostCommand
    profile_command: ProfileCommand

    def __init__(self) -> None:
        self.root = Root()
        self.start_command = StartCommand()
        self.help_command = HelpCommand()
        self.connect_command = ConnectCommand()
        self.new_post_command = NewPostCommand()
        self.profile_command = ProfileCommand()

    async def decider(self):
        # Decide where to go
        text = self.root.update.message.text

        match text:
            case '/start':
                await self.start_command.start()
            case '/help':
                await self.help_command.help()
            case '/connect':
                await self.connect_command.connect()
            case '/new_post':
                await self.new_post_command.new_post()
            case '/profile':
                await self.profile_command.profile()
            case _:
                await self.default()

    async def default(self):
        text = f"""Yo, you trippin! There is no command with this name."""
        await self.bot.send_message(text=text, chat_id=self.chat_id, parse_mode="HTML")
