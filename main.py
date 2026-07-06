import asyncio
import json
import discord
from discord.ext import commands

from config import TOKEN, DEFAULT_PREFIX

# ======================================================
# GUILD ID (for fast sync)
# ======================================================
GUILD_ID = 1506159710456254474


# ======================================================
# PREFIX SYSTEM
# ======================================================
def get_prefix(bot, message):
    try:
        with open("prefixes.json", "r") as f:
            prefixes = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        prefixes = {}

    if message.guild:
        return prefixes.get(str(message.guild.id), DEFAULT_PREFIX)

    return DEFAULT_PREFIX


# ======================================================
# INTENTS
# ======================================================
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True


# ======================================================
# BOT
# ======================================================
bot = commands.Bot(
    command_prefix=get_prefix,
    intents=intents,
    help_command=None
)


# ======================================================
# ON READY (HYBRID SYNC FIX)
# ======================================================
@bot.event
async def on_ready():
    print("\n===== BOT STARTED =====")
    print(f"Logged in as {bot.user}")
    print("=======================\n")

    try:
        # 🔥 FAST GUILD SYNC (instant updates)
        guild = discord.Object(id=GUILD_ID)
        guild_synced = await bot.tree.sync(guild=guild)
        print(f"Guild Synced Commands: {len(guild_synced)} ⚡")

        # 🌍 GLOBAL SYNC (shows all commands properly)
        global_synced = await bot.tree.sync()
        print(f"Global Synced Commands: {len(global_synced)} 🌍")

    except Exception as e:
        print("SYNC ERROR:", e)


# ======================================================
# ERROR HANDLER
# ======================================================
@bot.event
async def on_app_command_error(interaction: discord.Interaction, error):
    print("COMMAND ERROR:", error)

    try:
        if interaction.response.is_done():
            await interaction.followup.send(
                f"❌ Error: {error}",
                ephemeral=True
            )
        else:
            await interaction.response.send_message(
                f"❌ Error: {error}",
                ephemeral=True
            )
    except:
        pass


# ======================================================
# DEBUG INTERACTION LOG
# ======================================================
@bot.event
async def on_interaction(interaction: discord.Interaction):
    print(f"Interaction: {interaction.type} | {interaction.data}")


# ======================================================
# EXTENSIONS LOADER
# ======================================================
async def load_extensions():

    extensions = ["moderation", "timeout", "ban"]

    for ext in extensions:
        try:
            await bot.load_extension(ext)
            print(f"{ext} ✅ loaded")
        except Exception as e:
            print(f"{ext} ❌ failed")
            print("ERROR:", e)


# ======================================================
# START BOT
# ======================================================
async def main():
    async with bot:
        await load_extensions()
        await bot.start(TOKEN)


asyncio.run(main())
