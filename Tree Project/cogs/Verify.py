import disnake
from disnake.ext import commands


class VerifyModal(disnake.ui.Modal):
    def __init__(self, code):
        self.code = code
        components = [
            disnake.ui.TextInput(label="Введите код", placeholder=self.code, custom_id="code")
        ]
        super().__init__(title="Верификация", components=components, custom_id="verify_modal")

    async def callback(self, interaction: disnake.ModalInteraction) -> None:
        if self.code == int(interaction.text_values["code"]):
            role = interaction.guild.get_role(1208526721565859890)
            await interaction.author.remove_roles(role)
            await interaction.response.send_message("Вы успешно прошли верификацию!", ephemeral=True)
        else:
            await interaction.response.send_message("Неверный код!", ephemeral=True)


class ButtonView(disnake.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @disnake.ui.button(label="Верификация", style=disnake.ButtonStyle.grey, custom_id="button1")
    async def button1(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        import random
        code = random.randint(1000, 9999)
        await interaction.response.send_modal(VerifyModal(code))


class Verify(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.persistents_views_added = False

    @commands.command()
    @commands.has_guild_permissions(administrator=True)
    async def verify(self, ctx):
        embed = disnake.Embed(color=0x2F3136)
        embed.set_image(url='https://i.imgur.com/2vWxaNL.png')
        await ctx.send(embed=embed, view=ButtonView())

    @commands.Cog.listener()
    async def on_connect(self):
        if self.persistents_views_added:
            return

        self.bot.add_view(ButtonView(), message_id=1222796921135960084)

    @verify.error
    async def verifyerror(self, interaction, error):
        if isinstance(error, commands.MissingPermissions):
            embed = disnake.Embed(description='У вас недостаточна прав для использования этой команды')
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            print('Ошибка')


def setup(bot):
    bot.add_cog(Verify(bot))
