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
pomodoros = {
    
}


@client.event
async def on_ready():
    print(client.guilds)
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
            channel = await message.guild.create_text_channel("pomo-test")
            pomodoro = Pomodoro()
            pomodoro.start()
            pomomessage = await channel.send(f"{pomodoro.time_left()}")
            while pomodoro.active:
                await pomomessage.edit(content=f"{pomodoro.time_left()}")
                sleep(0.5)

        if message.content.startswith("Hej"):
            await message.channel.send("I am pomobot: Hello.")


client.run(token)