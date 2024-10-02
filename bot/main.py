from pyromod import Client
from pyrogram import filters
from pyrogram.types import Message

app = Client("Med school support Bot")


@app.on_message(filters.command('start'))
async def on_start(c: Client, msg: Message):
    await msg.reply('Received message')


app.run()
