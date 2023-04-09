from telegram import InlineKeyboardButton, InlineKeyboardMarkup


INSERT_POST_INFO = "insert_post_info"
UPDATE_POST_ATTRIBUTE = "update_post_attribute"
CONNECT_WITH_CHANNEL = "connect_with_channel"
CHANGE_CHANNEL = "change_channel"

NEW_POST_INLINE_KEYBOARD = InlineKeyboardMarkup([
    [
        InlineKeyboardButton(
            text="Title", callback_data="new_post.update.title"),
        InlineKeyboardButton(text="Description",
                             callback_data="new_post.update.description")
    ],
    [
        InlineKeyboardButton(
            "Post ✅", callback_data="new_post.post_confirmation")
    ]
])
