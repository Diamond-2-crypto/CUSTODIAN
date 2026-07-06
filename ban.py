import discord
from discord import app_commands
from discord.ext import commands
from datetime import datetime
from zoneinfo import ZoneInfo

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
        color=color
    )
    embed.set_footer(text=get_footer())
    return embed


class BanSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ==========================================================
    # KICK COMMAND
    # ==========================================================
    @app_commands.command(name="kick", description="Kick a member")
    @app_commands.checks.has_permissions(kick_members=True)
    async def kick(self, interaction: discord.Interaction, member: discord.Member, reason: str = None):

        reason_text = reason or "No reason provided"

        try:
            # 🔥 DM EMBED
            try:
                dm_embed = create_embed(
                    "👢 You Were Kicked",
                    f"You were kicked from **{interaction.guild.name}**\n\n📌 Reason: {reason_text}",
                    discord.Color.orange()
                )
                await member.send(embed=dm_embed)
            except:
                pass

            await member.kick(reason=reason_text)

            # SERVER EMBED
            embed = create_embed(
                "👢 Member Kicked",
                f"{member.mention} has been kicked\n\n📌 Reason: {reason_text}",
                discord.Color.orange()
            )

            await interaction.response.send_message(embed=embed, ephemeral=True)

        except Exception as e:
            await interaction.response.send_message(f"❌ Error: {e}", ephemeral=True)

    # ==========================================================
    # BAN COMMAND
    # ==========================================================
    @app_commands.command(name="ban", description="Ban a member")
    @app_commands.checks.has_permissions(ban_members=True)
    async def ban(self, interaction: discord.Interaction, member: discord.Member, reason: str = None):

        reason_text = reason or "No reason provided"

        try:
            # 🔥 DM EMBED
            try:
                dm_embed = create_embed(
                    "🔨 You Were Banned",
                    f"You were banned from **{interaction.guild.name}**\n\n📌 Reason: {reason_text}",
                    discord.Color.red()
                )
                await member.send(embed=dm_embed)
            except:
                pass

            await member.ban(reason=reason_text)

            # SERVER EMBED
            embed = create_embed(
                "🔨 Member Banned",
                f"{member.mention} has been banned\n\n📌 Reason: {reason_text}",
                discord.Color.red()
            )

            await interaction.response.send_message(embed=embed, ephemeral=True)

        except Exception as e:
            await interaction.response.send_message(f"❌ Error: {e}", ephemeral=True)

    # ==========================================================
    # UNBAN COMMAND
    # ==========================================================
    @app_commands.command(name="unban", description="Unban a user")
    @app_commands.checks.has_permissions(ban_members=True)
    async def unban(self, interaction: discord.Interaction, user: discord.User, reason: str = None):

        reason_text = reason or "No reason provided"

        try:
            await interaction.guild.unban(user, reason=reason_text)

            # 🔥 DM EMBED
            try:
                dm_embed = create_embed(
                    "♻️ You Were Unbanned",
                    f"You were unbanned from **{interaction.guild.name}**\n\n📌 Reason: {reason_text}",
                    discord.Color.green()
                )
                await user.send(embed=dm_embed)
            except:
                pass

            # SERVER EMBED
            embed = create_embed(
                "♻️ User Unbanned",
                f"{user.mention} has been unbanned\n\n📌 Reason: {reason_text}",
                discord.Color.green()
            )

            await interaction.response.send_message(embed=embed, ephemeral=True)

        except Exception as e:
            await interaction.response.send_message(f"❌ Error: {e}", ephemeral=True)


async def setup(bot):
    await bot.add_cog(BanSystem(bot))
