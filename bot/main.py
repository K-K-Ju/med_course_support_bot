from pyromod import Client
from pyrogram import filters
from pyrogram.types import Message
import messages
import bot.config
from bot.db import MessageDb, AdminDb
from bot.dto import MessageDTO, AdminDTO
from bot.static import AdminKeyboardMarkup, MenuOptions
from bot.custom_filters import first_is_emoji, is_admin

app = Client("Med school support Bot")
bot.config.init_config('your/path')
msg_db = MessageDb()
admins_db = AdminDb()

msg_db.prepare_db()
admins_db.prepare_db()


@app.on_message(filters.private & filters.command(bot.config.config['ADMIN_KEY']))
async def enter_admin_panel(c: Client, msg: Message):
    if not admins_db.exists(msg.chat.id):
        name = (await c.ask(msg.chat.id, 'Enter your name')).text
        admins_db.add(AdminDTO(msg.chat.id, msg.from_user.username, name))

    await msg.reply('Welcome admin!', reply_markup=AdminKeyboardMarkup)


@app.on_message(filters.private & first_is_emoji & is_admin(admins_db))
async def admin_keyboard_action(c: Client, msg: Message):
    if msg.text == MenuOptions.GET_ALL:
        msgs = msg_db.all()
        for m in msgs:
            await c.send_message(msg.chat.id, f'<b>From</b>:{m.tg_id}\n<b>Datetime</b>:{m.datetime}\n\n{m.text}')
    elif msg.text == MenuOptions.GET_BY_USER_ID:
        pass
    elif msg.text == MenuOptions.EXIT:
        admins_db.set_active(msg.chat.id, 0)
        await app.send_message(msg.chat.id, 'You exited admin panel', reply_markup=None)



@app.on_message(filters.private & filters.command('start'))
async def on_start(c: Client, msg: Message):
    await msg.reply(messages.START_MESSAGE)


@app.on_message(filters.private & filters.text)
async def on_message(c: Client, msg: Message):
    # TODO logging
    dto = MessageDTO(msg.chat.id, msg.text, msg.date.isoformat())
    msg_db.add(dto)


app.run()
