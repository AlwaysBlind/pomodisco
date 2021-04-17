import os
from dotenv import load_dotenv
import discord
from wonderwords import RandomWord
from time import sleep
from pomodoro import Pomodoro, PomoStatus
from datetime import timedelta

load_dotenv()
r = RandomWord()

token = os.getenv("TOKEN")
GUILD = os.getenv("GUILD")

client = discord.Client()
pomodoro = None

pomodoros = {}
MAX_INACTIVE_TIME = timedelta(hours=2)

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
        while pomodoro.get_inactive_time() < MAX_INACTIVE_TIME:
            pomodoro.update()
            await pomomessage.edit(content=f"{pomodoro.get_pomo_message()}")
            sleep(1)
        print("Bot is inactive")

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        if message.content == "!pomo":
            random_word = (
                r.word(regex="p.*", include_parts_of_speech=["adjectives"]) + "-pomo"
            )
            channel = await create_text_channel_with_permissions(message, random_word)
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


async def create_text_channel_with_permissions(message, name):
    all_except = discord.Permissions.all()
    all_except.read_messages, all_except.read_message_history = False, False
    permissions = discord.PermissionOverwrite.from_pair(
        discord.Permissions(read_messages=True, read_message_history=True), all_except
    )
    overwrites = {
        message.guild.default_role: permissions,
        message.guild.me: discord.PermissionOverwrite.from_pair(
            discord.Permissions.all(), discord.Permissions.none()
        ),
    }
    return await message.guild.create_text_channel(name=name, overwrites=overwrites)


client.run(token)
