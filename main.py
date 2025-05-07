import discord
from discord.ext import commands
import time
import json

import custom.AI as AI
from custom.commands import Commands as Bot_Commands
from custom.messages import Messages
from custom.lore_handling import LoreHandling

MESSAGES_PATH = "messages.json"

TOKEN = "pee pee poo poo!"

messages_instance = Messages()
bot_commands = Bot_Commands(messages_instance)

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.event
async def on_message(message: discord.Message):
    global IN_USE
    if message.author == bot.user:
        return
    
    if not message.channel.category_id == 1349346892722737265 or message.channel.category is None:  # public server use shit
        lorehandler = LoreHandling(message.author.id, message.channel.id)
        _abc = False
        for i in lorehandler.channels:
            if i == message.channel.id:
                messages_instance_temp = lorehandler
                _abc = True
                break
        if not _abc:
            return
    else:
        messages_instance_temp = messages_instance

    if message.content.startswith("!"):
        await bot_commands.ProcessComands(message)
        return
    async with message.channel.typing():
        start = time.time()
        response = AI.Get_Response(message, messages_instance_temp.messages)
        total = time.time() - start
        if message is None or not message:
            return
        USERNAME = message.author.display_name if message.author.display_name else message.author.global_name
        CONTENT = message.content
        messages_instance_temp.messages.append({
            "role": "user",
            "content": f"{USERNAME}: {CONTENT}"
        })
        messages_instance_temp.messages.append({
            "role": "assistant",
            "content": response
        })
        messages_instance_temp.save()
        await message.reply(f"{response}\n-# Took: {total:.2f} <3")
    await bot.process_commands(message)


bot.run(TOKEN)
