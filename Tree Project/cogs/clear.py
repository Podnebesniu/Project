import disnake
from disnake.ext import commands
from disnake.ui import Button, View

class Clear(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name='очистить', description='Очищает старые сообщеня')
    @commands.has_guild_permissions(administrator=True)
    async def clear(self, interaction, amount: int): 
        class ConfirmView(View):
            def __init__(self):
                super().__init__()
                self.value = None

            @disnake.ui.button(label="Подтвердить", style=disnake.ButtonStyle.green)
            async def confirm(self, button, interaction):
                self.value = True
                for child in self.children:
                    child.disabled = True
                await interaction.response.edit_message(view=self)
                self.stop()

            @disnake.ui.button(label="Отмена", style=disnake.ButtonStyle.red)
            async def cancel(self, button, interaction):
                self.value = False
                for child in self.children:
                    child.disabled = True
                await interaction.response.edit_message(view=self)
                self.stop()

        view = ConfirmView()

        embed = disnake.Embed(title="Подтверждение", description=f"Вы уверены, что хотите удалить {amount} сообщений?", color=0xff0000)
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

        await view.wait()

        if view.value is True:
            await interaction.channel.purge(limit=amount + 1)
            embed = disnake.Embed(title="Clear", description=f"Удалил {amount} сообщений", color=0x00ff00)
            embed.set_thumbnail(url=self.bot.user.avatar.url)
            await interaction.edit_original_message(embed=embed, view=None)
        else:
            embed = disnake.Embed(description="Очистка сообщений отменена.", color=0x00ff00)
            await interaction.edit_original_message(embed=embed, view=None)

    @clear.error
    async def clearerror(self, interaction, error):
        if isinstance(error, commands.MissingPermissions):
            embed = disnake.Embed(description="У вас недостаточна прав для использование этой команды")
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            print(f"Error during clear command: {error}")
            embed = disnake.Embed(description="Произошла ошибка при выполнении команды. Попробуйте позже.")
            await interaction.response.send_message(embed=embed, ephemeral=True) 


def setup(bot):
    bot.add_cog(Clear(bot))