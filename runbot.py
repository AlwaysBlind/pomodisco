import os
from dotenv import load_dotenv
import discord
from wonderwords import RandomWord
from time import sleep
from pomodoro import Pomodoro

load_dotenv()
r = RandomWord()

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

        if message.content == "!pomo":
            random_word = r.word(regex="p.*", include_parts_of_speech=["adjectives"]) + "-pomo"
            channel = await message.guild.create_text_channel(random_word)
            await message.channel.send(f"Pomo session started in channel {channel.mention}")
            pomodoro = Pomodoro()
            pomodoros[random_word] = pomodoro
            pomodoro.start()

            pomomessage = await channel.send(f"{pomodoro.get_pomo_message()}")
            while (pomodoro.active):
                pomodoro.update()
                await pomomessage.edit(content=f"{pomodoro.get_pomo_message()}")
                sleep(1)

client.run(token)
