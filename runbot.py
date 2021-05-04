import os
from dotenv import load_dotenv
import discord
from wonderwords import RandomWord
from pomodoro import Pomodoro, PomoStatus, UpdateStatus
from datetime import timedelta
import asyncio
from asyncio import sleep

load_dotenv()
r = RandomWord()

token = os.getenv("TOKEN")
GUILD = os.getenv("GUILD")

client = discord.Client()

pomodoros = {}

subscriptions = {}

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

    async def notify_subscribers(subscribers, channel):
        message = " ".join([f"{user.mention}" for user in subscribers])
        if message:
            mention_msg = await channel.send(message)
            await sleep(7)
            asyncio.create_task(mention_msg.delete())

    async def run_pomo(pomodoro, pomomessage):
        while pomodoro.get_inactive_time() < MAX_INACTIVE_TIME:
            status = pomodoro.update()
            if status == UpdateStatus.StatusChange:
                # Om pomo är break och det är 30 sek kvar skicka ut meddelande till alla som är subscribed till den pomon
                try:
                    asyncio.create_task(
                        notify_subscribers(pomodoro.subscribers, pomomessage.channel)
                    )
                except discord.errors.NotFound as e:
                    print(e, "Channel does not exist anymore")
                    return
            try:
                await pomomessage.edit(content=f"{pomodoro.get_pomo_message()}")
            except discord.errors.NotFound as e:
                print(e, "Channel does not exist anymore")
                return

            await sleep(1)
        remove_pomo(pomomessage.channel.id, pomodoro.announcement_message_id)
        await pomomessage.channel.delete()
        print("Bot is inactive")

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        if message.content.startswith("!del"):
            for channel in message.guild.channels:
                if channel.name != "asd":
                    await channel.delete()

        if message.content.startswith("!pomo"):

            ##Create channel and pomo session.
            random_word = (
                r.word(regex="p.*", include_parts_of_speech=["adjectives"]) + "-pomo"
            )
            channel = await create_text_channel_with_permissions(message, random_word)
            if message.content.startswith("!pomo heavy"):
                pomodoro = Pomodoro.get_heavy_pomo()
            else:
                pomodoro = Pomodoro()
            pomodoros[channel.id] = pomodoro

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
            pomodoro.announcement_message_id = pomo_announcement.id

            subscriptions[pomo_announcement.id] = pomodoro

            ##Initiate pomo
            asyncio.create_task(run_pomo(pomodoro, pomomessage))

    @client.event
    async def on_reaction_add(reaction, user):

        ##Reactions for pomo session
        if user == client.user:
            return
        channel_id = reaction.message.channel.id
        if channel_id in pomodoros:
            if reaction.emoji == "▶":
                pomodoros[channel_id].start()
            elif reaction.emoji == "⏸":
                pomodoros[channel_id].stop()
            elif reaction.emoji == "⏩" and pomodoros[channel_id].status in {
                PomoStatus.BREAK,
                PomoStatus.LONGBREAK,
            }:
                pomodoros[channel_id].handle_status()
            asyncio.create_task(reaction.remove(user))

        ##Reactions to subscribe
        if reaction.message.id in subscriptions:
            asyncio.create_task(reaction.remove(user))
            if reaction.emoji == "🔔":
                subscriptions[reaction.message.id].subscribers.add(user)
            if reaction.emoji == "🔕":
                subscriptions[reaction.message.id].subscribers.discard(user)

        # Reagera på meddelandet för att subscriba
        # Se till att det är rrätt meddelande genom message id.
        # channelID istället för namn

    @client.event
    async def on_guild_channel_delete(channel):
        if channel.id in pomodoros:
            pomo = pomodoros[channel.id]
            remove_pomo(channel.id, pomo.announcement_message_id)

    def remove_pomo(channel_id, pomo_announcement_id):
        pomodoros.pop(channel_id)
        subscriptions.pop(pomo_announcement_id)


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
