import discord
from discord import app_commands
from discord.ext import commands
from datetime import timedelta, datetime
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


class Timeout(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # =========================
    # TIMEOUT
    # =========================
    @app_commands.command(name="timeout", description="Timeout a member")
    @app_commands.checks.has_permissions(moderate_members=True)
    async def timeout(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        minutes: int,
        reason: str = None
    ):

        reason_text = reason or "No reason provided"

        try:
            await member.timeout(timedelta(minutes=minutes), reason=reason_text)

            # ================= SERVER EMBED =================
            embed = create_embed(
                "⛔ Member Timed Out",
                f"{member.mention} timed out for **{minutes} minutes**\n\n📌 Reason: {reason_text}",
                discord.Color.red()
            )

            await interaction.response.send_message(embed=embed, ephemeral=True)

            # ================= DM EMBED (FIXED) =================
            try:
                dm_embed = create_embed(
                    "⛔ You Have Been Timed Out",
                    f"You were timed out in **{interaction.guild.name}**\n\n"
                    f"🕒 Duration: {minutes} minutes\n"
                    f"📌 Reason: {reason_text}",
                    discord.Color.red()
                )

                await member.send(embed=dm_embed)

            except:
                pass

        except Exception as e:
            await interaction.response.send_message(f"❌ Error: {e}", ephemeral=True)

    # =========================
    # UNTIMEOUT
    # =========================
    @app_commands.command(name="untimeout", description="Remove timeout from a member")
    @app_commands.checks.has_permissions(moderate_members=True)
    async def untimeout(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        reason: str = None
    ):

        reason_text = reason or "No reason provided"

        try:
            await member.timeout(None, reason=reason_text)

            # ================= SERVER EMBED =================
            embed = create_embed(
                "✅ Timeout Removed",
                f"{member.mention} is now unmuted\n\n📌 Reason: {reason_text}",
                discord.Color.green()
            )

            await interaction.response.send_message(embed=embed, ephemeral=True)

            # ================= DM EMBED (FIXED) =================
            try:
                dm_embed = create_embed(
                    "✅ Timeout Removed",
                    f"You are now unmuted in **{interaction.guild.name}**\n\n"
                    f"📌 Reason: {reason_text}",
                    discord.Color.green()
                )

                await member.send(embed=dm_embed)

            except:
                pass

        except Exception as e:
            await interaction.response.send_message(f"❌ Error: {e}", ephemeral=True)


async def setup(bot):
    await bot.add_cog(Timeout(bot))
