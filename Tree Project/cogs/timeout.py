import datetime
import disnake
from disnake.ext import commands

class Timeout(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name='таймаут', description='Выдать таймаут')
    @commands.has_guild_permissions(administrator=True)
    async def timeout(self, interaction, member: disnake.Member, time: str, reason: str):
        try:
            time_parts = time.split()
            minutes = int(time_parts[0])
            unit = time_parts[1] if len(time_parts) > 1 else "minutes"

            if unit == "minutes":
                time = datetime.datetime.now() + datetime.timedelta(minutes=minutes)
            elif unit == "hours":
                time = datetime.datetime.now() + datetime.timedelta(hours=minutes)
            else:
                raise ValueError("Invalid time unit. Use 'minutes' or 'hours'.")
            await member.timeout(reason=reason, until=time)
            cool_time = disnake.utils.format_dt(time, style="R")
            embed = disnake.Embed(title="Timeout", description=f"{member.mention} получил таймаут. Таймаут закончится {cool_time}", color=disnake.Color.green())
            await interaction.response.send_message(embed=embed, ephemeral=True)

        except ValueError as e:
            embed = disnake.Embed(title="Ошибка", description=f"Неправильный формат времени. Используйте 'minutes' или 'hours'. Например: `/таймаут @user 10 minutes` или `/таймаут @user 2 hours`", color=disnake.Color.red())
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @commands.slash_command(name='снять', description='Снять таймаут')
    @commands.has_guild_permissions(administrator=True)
    async def untimeout(self, interaction, member: disnake.Member):
        await member.timeout(reason=None, until=None)
        await interaction.response.send_message(f"Снят таймаут с {member.mention}", ephemeral=True)

    @timeout.error
    async def timeouterror(self, interaction, error):
        if isinstance(error, commands.MissingPermissions):
            embed = disnake.Embed(description="У вас нету прав чтобы использовать эту команду")
            await interaction.response.send_message(embed = embed, ephemeral=True)
        else:
            print('Ошибка')


def setup(bot):
    bot.add_cog(Timeout(bot))