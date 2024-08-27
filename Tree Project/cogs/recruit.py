import disnake
from disnake.ext import commands

class RecruitmentModal(disnake.ui.Modal):
    def __init__(self):
        components = [
            disnake.ui.TextInput(
                label="Ваше имя",
                placeholder="Введите ваше настоящее имя",
                custom_id="name",
                style=disnake.TextInputStyle.short,
                max_length=100,
            ),
            disnake.ui.TextInput(
                label="Почему именно вы?",
                placeholder="Введите причину",
                custom_id="reason",
                style=disnake.TextInputStyle.paragraph,
                min_length=10,
                max_length=500,
            ),
            disnake.ui.TextInput(
                label='Расскажите о себе.',
                placeholder='О себе',
                custom_id='about',
                style=disnake.TextInputStyle.paragraph,
                min_length=15,
                max_length=500,
            )
        ]
        super().__init__(title="Заявка в рекруты", custom_id="recruitment_modal", components=components)

    async def callback(self, interaction: disnake.ModalInteraction):
        name = interaction.text_values["name"]
        reason = interaction.text_values["reason"]
        about = interaction.text_values["about"]

        embed_user = disnake.Embed(color=0x2F3136, title="Заявка отправлена!")
        embed_user.description = f"{interaction.author.mention}, Благодарим вас за **заявку**! \n" \
                                 f"Если вы нам **подходите**, администрация **свяжется** с вами в ближайшее время."
        embed_user.set_thumbnail(url=interaction.author.display_avatar.url)
        await interaction.response.send_message(embed=embed_user, ephemeral=True)

        channel = interaction.guild.get_channel(1208524885782044732)
        if channel:
            embed_channel = disnake.Embed(color=0x2F3136, title="Новая заявка на должность рекрута")
            embed_channel.description = f"**Ваше имя:** {name}\n" \
                                        f"**Дискорд:** {interaction.author.mention}\n" \
                                        f"**Причина:** {reason}\n" \
                                        f"**О себе:** {about}"
            view = disnake.ui.View()
            view.add_item(disnake.ui.Button(label="Принять", style=disnake.ButtonStyle.green, custom_id=f"accept_recruit_{interaction.author.id}"))
            view.add_item(disnake.ui.Button(label="Отказать", style=disnake.ButtonStyle.red, custom_id=f"deny_recruit_{interaction.author.id}"))
            await channel.send(embed=embed_channel, view=view)

class Recruitment(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name='рекрутинг', description='Для набора в команду сервера')
    @commands.has_guild_permissions(administrator=True)
    async def recruit(self, inter: disnake.ApplicationCommandInteraction):
        view = disnake.ui.View(timeout=None)
        view.add_item(disnake.ui.Button(label="Заполнить заявку", custom_id="recruit_button"))

        embed = disnake.Embed(color=0x2F3136)
        embed.set_author(name="Заявка в рекруты")
        embed.description = 'Заявка в команду дискорд сервера.'

        await inter.response.send_message(embed=embed, view=view)

    @commands.Cog.listener()
    async def on_button_click(self, inter: disnake.MessageInteraction):
        if inter.component.custom_id == "recruit_button":
            await inter.response.send_modal(RecruitmentModal())
        elif inter.component.custom_id.startswith("accept_recruit_"):
            user_id = int(inter.component.custom_id.split("_")[2])
            user = inter.guild.get_member(user_id)
            if user:
                role = disnake.utils.get(inter.guild.roles, name="Рекрут")
                if role:
                    await user.add_roles(role)
                    await inter.response.send_message(f"Роль {role.name} успешно выдана пользователю {user.mention}!", ephemeral=True)
                    await inter.message.edit(view=None)
                else:
                    await inter.response.send_message("Роль 'Рекрут' не найдена.", ephemeral=True)
            else:
                await inter.response.send_message("Пользователь не найден.", ephemeral=True)
        elif inter.component.custom_id.startswith("deny_recruit_"):
            await inter.response.send_message("Заявка отклонена.", ephemeral=True)
            await inter.message.edit(view=None)

    @recruit.error
    async def recruiterror(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = disnake.Embed(description="У вас недостаточна прав для использования команды", color=0xFF3333)
            await ctx.respond(embed=embed, ephemeral=True)
        else:
            print("Ошибка")

def setup(bot):
    bot.add_cog(Recruitment(bot))