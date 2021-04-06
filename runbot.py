import os
from dotenv import load_dotenv
import discord

load_dotenv()

token = os.getenv("TOKEN")
GUILD = os.getenv("GUILD")

client = discord.Client()


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

        if message.content.startswith("Hej"):
            await message.channel.send("I am pomobot: Hello.")


client.run(token)