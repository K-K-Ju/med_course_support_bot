from pyrogram.types import ReplyKeyboardMarkup, KeyboardButton


class MenuOptions:
    GET_ALL = '📔Get all new messages'
    GET_BY_USER_ID = '🔍Get messages by user id'
    EXIT = '🚪Exit'


AdminKeyboardMarkup = ReplyKeyboardMarkup([
    [KeyboardButton(MenuOptions.GET_ALL), KeyboardButton(MenuOptions.GET_BY_USER_ID)],
    [KeyboardButton(MenuOptions.EXIT)]
], resize_keyboard=True, is_persistent=True)
