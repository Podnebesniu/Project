import disnake
from disnake.ext import commands
import random
import datetime

class News(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name='новости', description='Новости для сервера')
    async def news(self, ctx):
        # Define some news items
        news_items = [
            "**Новость 1:** Сегодня мы проводим турнир по Counter-Strike 2. Присоединяйтесь!",
            "**Новость 2:** На сервере появился новый канал для мемов. Заходите и общайтесь!",
            "**Новость 3:** [Имя пользователя] только что получил(а) [Достижение]! Поздравляем!",
            "**Новость 4:** Запланировано голосование по [Тема] в ближайшее время. Подписывайтесь на обновления!"
        ]

        # Choose a random news item
        chosen_news = random.choice(news_items)

        # Get the current time
        current_time = datetime.datetime.now().strftime("%H:%M")

        # Get a random member
        random_member = random.choice(ctx.guild.members)  # Choose a random member from the guild

        embed = disnake.Embed(title="Новости Podnebesniu Squad", color=0x2F3136)
        embed.description = f"{chosen_news}\n" \
                           f"Добро пожаловать на дискорд сервер **Podnebesniu Squad**!\n" \
                           f"Надеюсь вы с кайфом проведете время.\n\n" \
                           f"**Текущее время:** {current_time}\n\n" \
                           f"**Привет от:** {random_member.mention}!"  # Mention a random member
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(News(bot))