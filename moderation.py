import discord
from discord.ext import commands
from discord import app_commands
import re
from datetime import timedelta

import json
from datetime import datetime
from zoneinfo import ZoneInfo

from config import DEFAULT_PREFIX


# ==========================================================
# COMMON FUNCTIONS
# ==========================================================
def get_footer():
    now = datetime.now(ZoneInfo("Asia/Karachi"))
    return f"BOT Made by NOBITA • {now.strftime('%d %b %Y • %I:%M:%S %p')}"



def create_embed(title, description="", color=discord.Color.blurple()):
    embed = discord.Embed(
        title=title,
        description=description,
        color=color,
        
    )

    embed.set_footer(text=get_footer())

    return embed


# ==========================================================
# COG
# ==========================================================

class Moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # ======================================================
    # PREFIX COMMAND
    # ======================================================

    @commands.has_permissions(administrator=True)
    @commands.command(name="setprefix")
    async def prefix_command(self, ctx, prefix: str):

        try:
            with open("prefixes.json", "r") as f:
                prefixes = json.load(f)
        except:
            prefixes = {}

        prefixes[str(ctx.guild.id)] = prefix

        with open("prefixes.json", "w") as f:
            json.dump(prefixes, f, indent=4)

        embed = create_embed(
            "✅ Prefix Updated",
            f"New Prefix: `{prefix}`",
            discord.Color.green()
        )

        await ctx.send(embed=embed)

    # ======================================================
    # SLASH COMMAND
    # ======================================================

    @app_commands.command(
        name="setprefix",
        description="Change the bot prefix."
    )
    @app_commands.checks.has_permissions(administrator=True)
    async def prefix_slash(
        self,
        interaction: discord.Interaction,
        prefix: str
    ):

        try:
            with open("prefixes.json", "r") as f:
                prefixes = json.load(f)
        except:
            prefixes = {}

        prefixes[str(interaction.guild.id)] = prefix

        with open("prefixes.json", "w") as f:
            json.dump(prefixes, f, indent=4)

        embed = create_embed(
            "✅ Prefix Updated",
            f"New Prefix: `{prefix}`",
            discord.Color.green()
        )

        await interaction.response.send_message(embed=embed)

    # ======================================================
    # PING (PREFIX)
    # ======================================================

    @commands.command(name="ping")
    async def ping_prefix(self, ctx):

        latency = round(self.bot.latency * 1000)

        embed = create_embed(
            "🏓 Pong!",
            f"**Bot Latency:** `{latency} ms`",
            discord.Color.green()
        )

        embed.set_author(
            name="Bot Ping",
            icon_url=self.bot.user.display_avatar.url
        )

        await ctx.send(embed=embed)

    # ======================================================
    # PING (SLASH)
    # ======================================================

    @app_commands.command(
        name="ping",
        description="Shows the bot latency."
    )
    async def ping_slash(
        self,
        interaction: discord.Interaction
    ):

        latency = round(self.bot.latency * 1000)

        embed = create_embed(
            "🏓 Pong!",
            f"**Bot Latency:** `{latency} ms`",
            discord.Color.green()
        )

        embed.set_author(
            name="Bot Ping",
            icon_url=self.bot.user.display_avatar.url
        )

        await interaction.response.send_message(embed=embed)
            # ======================================================
    # COMMAND 02 - WARN
    # ======================================================

    @app_commands.command(
        name="warn",
        description="Warn a member."
    )
    @app_commands.describe(
        member="Member to warn",
        reason="Reason for the warning"
    )
    @app_commands.checks.has_permissions(manage_messages=True)
    async def warn(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        reason: str
    ):

        if member.bot:
            embed = create_embed(
                "❌ Error",
                "You cannot warn bots.",
                discord.Color.red()
            )
            return await interaction.response.send_message(
                embed=embed,
                ephemeral=True
            )

        if member == interaction.user:
            embed = create_embed(
                "❌ Error",
                "You cannot warn yourself.",
                discord.Color.red()
            )
            return await interaction.response.send_message(
                embed=embed,
                ephemeral=True
            )

        try:
            with open("data/warnings.json", "r") as f:
                warnings = json.load(f)
        except:
            warnings = {}

        user_id = str(member.id)

        if user_id not in warnings:
            warnings[user_id] = []

        warning = {
            "reason": reason,
            "moderator": interaction.user.name,
            "server": interaction.guild.name,
            "date": datetime.now().strftime("%d %b %Y | %I:%M:%S %p")
        }

        warnings[user_id].append(warning)

        with open("data/warnings.json", "w") as f:
            json.dump(warnings, f, indent=4)

        dm_embed = discord.Embed(
            title="⚠️ You Have Been Warned",
            color=discord.Color.orange()
        )

        dm_embed.add_field(
            name="Server",
            value=interaction.guild.name,
            inline=False
        )

        dm_embed.add_field(
            name="Reason",
            value=reason,
            inline=False
        )

        dm_embed.add_field(
            name="Moderator",
            value=interaction.user.name,
            inline=False
        )

        dm_embed.add_field(
            name="Date",
            value=datetime.now().strftime("%d %b %Y | %I:%M:%S %p"),
            inline=False
        )

        dm_embed.set_thumbnail(
            url=interaction.guild.icon.url if interaction.guild.icon else member.display_avatar.url
        )

        dm_embed.set_footer(text=get_footer())
                # =========================
        # SEND WARNING DM (NO MODERATOR)
        # =========================
        dm_embed = discord.Embed(
            title="⚠️ You Have Been Warned",
            color=discord.Color.orange()
        )

        dm_embed.add_field(
            name="Server",
            value=interaction.guild.name,
            inline=False
        )

        dm_embed.add_field(
            name="Reason",
            value=reason,
            inline=False
        )

        dm_embed.add_field(
            name="Date",
            value=datetime.now().strftime("%d %b %Y | %I:%M:%S %p"),
            inline=False
        )

        dm_embed.set_thumbnail(
            url=interaction.guild.icon.url if interaction.guild.icon else member.display_avatar.url
        )

        dm_embed.set_footer(text=get_footer())

        try:
            await member.send(embed=dm_embed)
        except discord.Forbidden:
            pass  # user DMs off

        # =========================
        # SERVER CONFIRMATION MESSAGE
        # =========================
        confirm_embed = create_embed(
            "⚠️ Warning Issued",
            f"{member.mention} has been warned successfully.",
            discord.Color.orange()
        )

        confirm_embed.add_field(
            name="Server",
            value=interaction.guild.name,
            inline=False
        )

        confirm_embed.add_field(
            name="Reason",
            value=reason,
            inline=False
        )

        confirm_embed.add_field(
            name="Moderator",
            value=interaction.user.mention,
            inline=False
        )

        confirm_embed.add_field(
            name="Total Warnings",
            value=str(len(warnings[user_id])),
            inline=False
        )

        await interaction.response.send_message(embed=confirm_embed)
    @app_commands.command(
        name="warnings",
        description="View warnings for a user or everyone in the server."
    )
    @app_commands.describe(user="Leave empty to view all warnings.")
    async def warnings(
        self,
        interaction: discord.Interaction,
        user: discord.Member = None
    ):
        try:
            with open("data/warnings.json", "r") as f:
                warnings_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            warnings_data = {}

        # Show warnings for a specific user
        if user is not None:
            user_warnings = warnings_data.get(str(user.id), [])

            embed = create_embed(
    "User Warnings",
    "",
    discord.Color.orange()
            )
            embed.add_field(
                name="User",
                value=user.mention,
                inline=False
            )
            embed.add_field(
                name="Total Warnings",
                value=str(len(user_warnings)),
                inline=False
            )

            await interaction.response.send_message(embed=embed)
            return

        # Show all users with warnings
        embed = create_embed(
    "Server Warnings",
    "",
    discord.Color.red()
)

        found = False

        for user_id, warn_list in warnings_data.items():
            member = interaction.guild.get_member(int(user_id))
            if member:
                embed.add_field(
                    name=member.display_name,
                    value=f"⚠️ {len(warn_list)} warning(s)",
                    inline=False
                )
                found = True

        if not found:
            embed.description = "No warnings found."

        await interaction.response.send_message(embed=embed)
    @app_commands.command(
        name="clearwarnings",
        description="Clear all warnings of a member."
    )
    @app_commands.describe(member="Member whose warnings will be cleared")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def clearwarnings(
        self,
        interaction: discord.Interaction,
        member: discord.Member
    ):
        try:
            with open("data/warnings.json", "r") as f:
                warnings_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            warnings_data = {}

        user_id = str(member.id)

        if user_id not in warnings_data or len(warnings_data[user_id]) == 0:
            embed = create_embed(
                "❌ No Warnings",
                f"{member.mention} has no warnings to clear.",
                discord.Color.red()
            )
            return await interaction.response.send_message(
                embed=embed,
                ephemeral=True
            )

        total_warnings = len(warnings_data[user_id])

        del warnings_data[user_id]

        with open("data/warnings.json", "w") as f:
            json.dump(warnings_data, f, indent=4)

        embed = create_embed(
            "✅ Warnings Cleared",
            f"Successfully cleared **{total_warnings}** warning(s) from {member.mention}.",
            discord.Color.green()
        )

        embed.add_field(
            name="Member",
            value=member.mention,
            inline=False
        )

        embed.add_field(
            name="Moderator",
            value=interaction.user.mention,
            inline=False
        )

        embed.add_field(
            name="Warnings Removed",
            value=str(total_warnings),
            inline=False
        )

        await interaction.response.send_message(embed=embed)
        
 # =================================
    # ADD NEW COMMANDS BELOW THIS LINE
    # ======================================================

    # Example:
    # /serverinfo
    # /avatar
    # /restart
    # /ban
    # /kick
    # /timeout
    # /purge
    # /embed
    #
    # Every new command will be added above the setup function.


# ==========================================================
# SETUP
# ==========================================================

async def setup(bot):
    await bot.add_cog(Moderation(bot))
