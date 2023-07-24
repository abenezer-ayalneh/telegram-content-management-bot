from src.root import Root
from misc import constants


class NewPostCommand:
  root: Root

  def __init__(self):
      self.root = Root()

  async def new_post(self):
      self.root.db.sessions.update_one({"chat_id": self.root.chat_id}, {
          '$set': {"command": "/post", "question": constants.INSERT_POST_INFO, "data": {}}}, upsert=True)

      text = f"""Using the following attributes, please add detailed information about your post"""
      reply_markup = constants.NEW_POST_INLINE_KEYBOARD

      await self.root.bot.send_message(text=text, chat_id=self.root.chat_id, reply_markup=reply_markup, parse_mode="HTML")