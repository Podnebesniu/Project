from disnake.ext import commands
import disnake

class Avatar(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name='аватар', description='Посмотреть аватарки')
    async def avatar(self, interaction, member: disnake.Member = None):
        user = member or interaction.author
        embed = disnake.Embed(title=f"Аватар {user.name}", color=0x2f3136)
        embed.set_image(url=user.display_avatar.url)
        embed.set_footer(text=f"ID: {user.id}")

        if user.avatar is not None:
            embed.description = "Пользователь использует кастомный аватар."
        else:
            embed.description = "Пользователь использует стандартный аватар Discord."

        embed.add_field(name="Просмотреть в полном размере", value=f"[Открыть в браузере]({user.display_avatar.url})", inline=False) 

        await interaction.response.send_message(embed=embed)

    @commands.slash_command(name='сервер_аватар', description='Посмотреть аватар сервера')
    async def server_avatar(self, interaction):
        embed = disnake.Embed(title=f"Аватар сервера {interaction.guild.name}", color=0x2f3136)
        embed.set_footer(text=f"ID: {interaction.guild.id}")

        # Check if the server has a custom icon
        if interaction.guild.icon is not None:
            embed.set_image(url=interaction.guild.icon.url)
            embed.description = "Сервер использует кастомный аватар."
        else:
            embed.description = "Сервер не использует кастомный аватар."

        embed.add_field(name="Просмотреть в полном размере", value=f"[Открыть в браузере]({interaction.guild.icon.url})", inline=False) 

        await interaction.response.send_message(embed=embed)

    @avatar.error
    async def avatar_error(self, interaction, error):
        if isinstance(error, commands.MemberNotFound):
            embed = disnake.Embed(title="Ошибка", description="Пользователь не найден.", color=0xFF3333)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            print(f"Ошибка в команде /аватар: {error}")

def setup(bot):
    bot.add_cog(Avatar(bot))