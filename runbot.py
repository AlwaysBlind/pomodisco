import os
from dotenv import load_dotenv
import discord
from wonderwords import RandomWord
from time import sleep
from pomodoro import Pomodoro, PomoStatus

load_dotenv()
r = RandomWord()

token = os.getenv("TOKEN")
GUILD = os.getenv("GUILD")

client = discord.Client()
pomodoro = None

pomodoros = {}


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

    async def run_pomo(pomodoro, pomomessage):
        while pomodoro.active:
            pomodoro.update()
            await pomomessage.edit(content=f"{pomodoro.get_pomo_message()}")
            sleep(1)

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        if message.content == "!pomo":
            random_word = (
                r.word(regex="p.*", include_parts_of_speech=["adjectives"]) + "-pomo"
            )
            channel = await message.guild.create_text_channel(random_word)
            await message.channel.send(
                f"Pomo session started in channel {channel.mention}"
            )
            pomodoro = Pomodoro()
            pomodoros[random_word] = pomodoro
            pomodoro.start()

            reactions = ["▶", "⏸", "⏩"]
            pomomessage = await channel.send(f"{pomodoro.get_pomo_message()}")
            for reaction in reactions:
                await pomomessage.add_reaction(reaction)

            await run_pomo(pomodoro, pomomessage)

    @client.event
    async def on_reaction_add(reaction, user):

        if user == reaction.message.author:
            return
        channel_name = reaction.message.channel.name
        if channel_name in pomodoros:
            await reaction.remove(user)
            if reaction.emoji == "▶":
                pomodoros[channel_name].start()
                await run_pomo(pomodoros[channel_name], reaction.message)
            elif reaction.emoji == "⏸":
                pomodoros[channel_name].stop()
            elif reaction.emoji == "⏩" and pomodoros[channel_name].status in {
                PomoStatus.BREAK,
                PomoStatus.LONGBREAK,
            }:
                pomodoros[channel_name].handle_status()


client.run(token)
