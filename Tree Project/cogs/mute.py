import disnake
from disnake.ext import commands
import datetime
import asyncio

class VoiceMute(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name='мут', description='Выдать мут участнику в голосовом канале')
    @commands.has_guild_permissions(mute_members=True, administrator=True)
    async def mute(self, interaction, member: disnake.Member, reason: str = None):
        if not member.voice:
            await interaction.response.send_message(f"{member.mention} не находится в голосовом канале.", ephemeral=True)
            return

        if member.voice.mute:
            await interaction.response.send_message(f"{member.mention} уже замучен.", ephemeral=True)
            return

        await member.edit(mute=True, reason=reason)
        await interaction.response.send_message(f"{member.mention} был замучен в голосовом канале. {reason if reason else ''}", ephemeral=True)

    @commands.slash_command(name='размут', description='Снять мут с участника в голосовом канале')
    @commands.has_guild_permissions(mute_members=True, administrator=True)
    async def unmute(self, interaction, member: disnake.Member):
        if not member.voice:
            await interaction.response.send_message(f"{member.mention} не находится в голосовом канале.", ephemeral=True)
            return

        if not member.voice.mute:
            await interaction.response.send_message(f"{member.mention} уже размучен.", ephemeral=True)
            return

        await member.edit(mute=False)
        await interaction.response.send_message(f"{member.mention} был размучен.", ephemeral=True)

    @commands.slash_command(name='временный_мут', description='Выдать временный мут в голосовом канале')
    @commands.has_guild_permissions(mute_members=True, administrator=True)
    async def temp_mute(self, interaction, member: disnake.Member, duration: str, reason: str = None):
        if not member.voice:
            await interaction.response.send_message(f"{member.mention} не находится в голосовом канале.", ephemeral=True)
            return

        if member.voice.mute:
            await interaction.response.send_message(f"{member.mention} уже замучен.", ephemeral=True)
            return

        try:
            duration_parts = duration.split()
            duration_value = int(duration_parts[0])
            duration_unit = duration_parts[1] if len(duration_parts) > 1 else "seconds"

            if duration_unit == "seconds":
                seconds = duration_value
            elif duration_unit == "minutes":
                seconds = duration_value * 60
            elif duration_unit == "hours":
                seconds = duration_value * 3600
            else:
                raise ValueError("Invalid time unit. Use 'seconds', 'minutes', or 'hours'.")

            await member.edit(mute=True, reason=reason)
            await interaction.response.send_message(f"{member.mention} был замучен в голосовом канале на {duration} секунд. Причина: {reason if reason else ''}", ephemeral=True)
            await asyncio.sleep(seconds)
            await member.edit(mute=False)

        except ValueError as e:
            await interaction.response.send_message(f"Неправильный формат времени. Используйте 'seconds', 'minutes', или 'hours'. Например: `/временный_мут @username 10 seconds` или `/временный_мут @username 2 minutes`", ephemeral=True)

def setup(bot):
    bot.add_cog(VoiceMute(bot))