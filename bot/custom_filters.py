import emoji
from pyrogram import filters


def __emoji_filter__(_, c, msg):
    return emoji.is_emoji(str(msg.text)[0])


first_is_emoji = filters.create(__emoji_filter__)


def is_admin(db):
    async def func(flt, _, msg):
        user_id = msg.from_user.id
        return flt.db.exists(user_id) & flt.db.is_active(user_id)

    return filters.create(func, db=db)
