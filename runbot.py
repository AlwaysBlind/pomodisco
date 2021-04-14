import os
from dotenv import load_dotenv
import discord
from time import sleep
from pomodoro import Pomodoro

load_dotenv()

token = os.getenv("TOKEN")
GUILD = os.getenv("GUILD")

client = discord.Client()

pomodoro = None

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
        f"{client.user} is connected to the following guild:\n"
        f"{guild.name}(id: {guild.id})"
        f"Pomoooooooo"
    )

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        if message.content.startswith("!pomo"):
            pomodoro = Pomodoro()
            pomodoro.start()
            pomomessage = await message.channel.send(f"{pomodoro.get_pomo_message()}")
            while (pomodoro.active):
                pomomessage.update()
                await pomomessage.edit(content=f"{pomodoro.get_pomo_message()}")
                sleep(0.5)

        if message.content.startswith("Hej"):
            await message.channel.send("I am pomobot: Hello.")


client.run(token)