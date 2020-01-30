import os
import pkgutil
import codecs

from PCdiga import PCdiga

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
SITES = ['PCdiga']

bot = commands.Bot(command_prefix='!')

# client = discord.Client()

@bot.command(name='pcdiga', help='Mostra os preços e outras informações dos produtos escolhidos.')
async def pcdiga(ctx):
    try:
        scraper = PCdiga('pcdiga_links.txt')
        scraper.request()
        await ctx.channel.purge()
        for product_str in scraper.result2Discord():
            await ctx.send(product_str)
        
    except Exception:
        await ctx.send('Problema no ficheiro dos links! (Talvez esteja vazio)')

@bot.command(name='clear', help='Comando que apaga todas as mensagens do bot.')
async def clear(ctx, amount=1000):
    holder = await ctx.channel.purge(limit=int(amount) + 1)
    await ctx.send(f'Foram Apagadas **{len(holder)}** mensagens :envelope:')

@bot.command(name='get_links', help='Comando que mostra os links a serem usados e nome dos mesmos no comando !pcdiga.')
async def get_links(ctx, site_name=None):
    site_name = site_name.lower() if site_name is not None else site_name

    if site_name == 'pcdiga':
        with codecs.open('pcdiga_links.txt','r','utf-8') as f:
            lines = f.readlines()
            res = '```\n'
            for num, line in enumerate(lines):
                res += f'{num + 1} - {line[23:]}'

            await ctx.send('**LINKS:** (https://www.pcdiga.com/)\n' + res + '```')
    else:
        sites = ', '.join(list(map(lambda strr: f'  -> **{strr}**\n', SITES)))
        await ctx.send(f'**Nome do site em falta!** (!get_links <nome_do_site>)\n*Opções:*\n{sites}')
        



bot.run(TOKEN)
