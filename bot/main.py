from pyrogram.enums import ParseMode
from pyromod import Client
from pyrogram import filters
from pyrogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove
import messages
import bot.config
from bot.db import MessageDb, AdminDb
from bot.dto import MessageDTO, AdminDTO
from bot.static import AdminKeyboardMarkup, MenuOptions
from bot.custom_filters import first_is_emoji, is_admin

app = Client("Med school support Bot")
bot.config.init_config('C:\\Users\\tusen\\Developing\\Python\\med_course_messaging_bot\\config.json')
msg_db = MessageDb()
admins_db = AdminDb()

msg_db.prepare_db()
admins_db.prepare_db()


# ---------------------------- Admin section ---------------------------- #
@app.on_message(filters.private & filters.command(bot.config.config['ADMIN_KEY']))
async def enter_admin_panel(c: Client, msg: Message):
    if not admins_db.exists(msg.chat.id):
        name = (await c.ask(msg.chat.id, 'Enter your name')).text
        admins_db.add(AdminDTO(msg.chat.id, msg.from_user.username, name))
    admins_db.set_active(msg.chat.id, 1)
    await msg.reply('Welcome admin!', reply_markup=AdminKeyboardMarkup)


@app.on_message(filters.private & first_is_emoji & is_admin(admins_db))
async def admin_keyboard_action(c: Client, msg: Message):
    if msg.text == MenuOptions.GET_ALL:
        msgs = msg_db.all()
        for m in msgs:
            await c.send_message(msg.chat.id, f'<b>From</b>:{m.tg_id}\n<b>Datetime</b>:{m.datetime}\n\n{m.text}',
                                 parse_mode=ParseMode.HTML,
                                 reply_markup=InlineKeyboardMarkup(
                                     [[InlineKeyboardButton('До чату...', str(m.tg_id))]]))
    elif msg.text == MenuOptions.GET_BY_USER_ID:
        pass
    elif msg.text == MenuOptions.EXIT:
        admins_db.set_active(msg.chat.id, 0)
        await app.send_message(msg.chat.id, 'You exited admin panel', reply_markup=ReplyKeyboardRemove())


@app.on_callback_query(is_admin(admins_db))
async def reply_query(c: Client, query):
    customer = await app.get_users(int(query.data))
    while True:
        msg = await app.listen(user_id=query.from_user.id, filters=(filters.private & filters.text))
        if msg.text == MenuOptions.EXIT:
            admins_db.set_active_chat(msg.chat.id, 0)
            await c.send_message(msg.chat.id, f'Ви вийшли з діалогу з {customer.username}')
            break

        await c.send_message(customer.id, msg.text)


# ---------------------------- User section ---------------------------- #
@app.on_message(filters.private & filters.text)
async def on_message(c: Client, msg: Message):
    # TODO logging
    admin_tg_id = admins_db.get_admin_by_active_chat(msg.chat.id)
    if admin_tg_id != 0:
        await c.send_message(admin_tg_id, f'From:{msg.from_user.username}\n\n' + msg.text)
    else:
        dto = MessageDTO(msg.chat.id, msg.text, msg.date.isoformat())
        msg_db.add(dto)


@app.on_message(filters.private & filters.command('start'))
async def on_start(c: Client, msg: Message):
    await msg.reply(messages.START_MESSAGE, reply_markup=ReplyKeyboardRemove())


app.run()
