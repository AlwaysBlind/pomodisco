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

subscriptions = {}


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
            # Om pomo är break och det är 30 sek kvar skicka ut meddelande till alla som är subscribed till den pomon

            try:
                await pomomessage.edit(content=f"{pomodoro.get_pomo_message()}")
            except discord.errors.NotFound as e:
                print(e, "Channel does not exist anymore")
                break
            sleep(1)

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        if message.content == "!pomo":

            ##Create channel and pomo session.
            random_word = (
                r.word(regex="p.*", include_parts_of_speech=["adjectives"]) + "-pomo"
            )
            channel = await create_text_channel_with_permissions(message, random_word)
            pomodoro = Pomodoro()
            pomodoros[channel.id] = pomodoro
            pomodoro.start()

            reactions = ["▶", "⏸", "⏩"]
            pomomessage = await channel.send(f"{pomodoro.get_pomo_message()}")
            for reaction in reactions:
                await pomomessage.add_reaction(reaction)

            ##Create pomo announcement
            pomo_announcement = await message.channel.send(
                f"Pomo session started in channel {channel.mention}. Smash the bell below to subscribe to the pomo session."
            )
            await pomo_announcement.add_reaction("🔔")
            await pomo_announcement.add_reaction("🔕")

            subscriptions[pomo_announcement.id] = pomodoro

            ##Initiate pomo
            await run_pomo(pomodoro, pomomessage)

    @client.event
    async def on_reaction_add(reaction, user):

        ##Reactions for pomo session
        if user == reaction.message.author:
            return
        channel_id = reaction.message.channel.id
        if channel_id in pomodoros:
            await reaction.remove(user)
            if reaction.emoji == "▶":
                pomodoros[channel_id].start()
                await run_pomo(pomodoros[channel_id], reaction.message)
            elif reaction.emoji == "⏸":
                pomodoros[channel_id].stop()
            elif reaction.emoji == "⏩" and pomodoros[channel_id].status in {
                PomoStatus.BREAK,
                PomoStatus.LONGBREAK,
            }:
                pomodoros[channel_id].handle_status()

        ##Reactions to subscribe
        if reaction.message.id in subscriptions:
            await reaction.remove(user)
            if reaction.emoji == "🔔":
                subscriptions[reaction.message.id].subscribe_list.add(user.id)

        # Reagera på meddelandet för att subscriba
        # Se till att det är rrätt meddelande genom message id.
        # channelID istället för namn

    @client.event
    async def on_guild_channel_delete(channel):
        if channel.id in pomodoros:
            pomodoros[channel.id].stop()
            pomodoros.pop(channel.name)
            print(pomodoros)


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
