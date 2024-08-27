import disnake
from disnake.ext import commands


class Ban(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name='забанить', description='Выдать бан пользователю')
    @commands.has_guild_permissions(administrator=True)
    async def ban(self, ctx, user: disnake.User, *, reason=None):
        try:
            await ctx.guild.ban(user, reason=reason)
            await ctx.respond(f"Бан {user.mention}", ephemeral=True)
        except disnake.HTTPException as e:
            if e.code == 50013:
                await ctx.respond(f"Не могу забанить этого пользователя.", ephemeral=True)
            else:
                await ctx.respond(f"Произошла ошибка при попытке забанить пользователя. {e}", ephemeral=True)

    @commands.slash_command(name='разбанить', description='Разбанить пользователя')
    @commands.has_guild_permissions(administrator=True)
    async def unban(self, ctx, user: disnake.User):
        try:
            await ctx.guild.unban(user)
            await ctx.respond(f"Разбанен {user.mention}", ephemeral=True)
        except disnake.HTTPException as e:
            await ctx.respond(f"Произошла ошибка при попытке разбанить пользователя. {e}", ephemeral=True)

    @commands.slash_command(name='инфо_бана', description='Информация о бане пользователя')
    @commands.has_guild_permissions(administrator=True)
    async def ban_info(self, ctx, user: disnake.User):
        try:
            ban_entry = await ctx.guild.fetch_ban(user)
            embed = disnake.Embed(
                title=f"Информация о бане {user}",
                description=f"Причина: {ban_entry.reason}",
                color=0xFF3333
            )
            await ctx.respond(embed=embed, ephemeral=True)
        except disnake.HTTPException as e:
            await ctx.respond(f"Не удалось получить информацию о бане. {e}", ephemeral=True)
        except disnake.NotFound:
            await ctx.respond(f"Этот пользователь не забанен.", ephemeral=True)

    @ban.error
    async def banerror(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = disnake.Embed(description="У вас недостаточно прав для использования команды", color=0xFF3333)
            await ctx.respond(embed=embed, ephemeral=True)
        else: 
            print('Error')


def setup(bot):
    bot.add_cog(Ban(bot))