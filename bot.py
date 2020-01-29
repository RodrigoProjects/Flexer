import os
import pkgutil

from PCdiga import PCdiga

# from pcdiga_scraper.PCdiga import PCdiga



import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

# client = discord.Client()

@bot.command(name='pcdiga', help='Mostra os preços e outras informações dos produtos escolhidos.')
async def pcdiga(ctx):
    try:
        scraper = PCdiga('pcdiga_links.txt')
        scraper.request()
        for product_str in scraper.result2Discord():
            await ctx.send(product_str)
        
    except Exception:
        await ctx.send('Problema no ficheiro dos links! (Talvez esteja vazio)')


bot.run(TOKEN)
