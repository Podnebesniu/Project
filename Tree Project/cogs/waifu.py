from disnake.ext import commands
import disnake
import random
import aiohttp

class Waifu(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name='вайфу', description='Показывает случайную вайфу')
    async def waifu(self, interaction: disnake.ApplicationCommandInteraction):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://api.waifu.pics/sfw/waifu') as resp:
                if resp.status == 200:
                    data = await resp.json()
                    image_url = data['url']

                    embed = disnake.Embed(title=f"Твоя вайфу:", color=0xffa500)
                    embed.set_image(url=image_url)
                    await interaction.response.send_message(embed=embed, ephemeral=True) 
                else:
                    await interaction.response.send_message("Ошибка при получении изображения. Попробуйте ещё раз.", ephemeral=True) 

def setup(bot):
    bot.add_cog(Waifu(bot))