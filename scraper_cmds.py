import os
import codecs

from PCdiga import PCdiga

import discord
from discord.ext import commands

SITES = ['pcdiga']


class Scraper(commands.Cog):
    '''Comandos responsavéis por dar scrap em várias lojas na Internet'''
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='pcdiga', help='Mostra os preços e outras informações dos produtos escolhidos.')
    async def pcdiga(self, ctx):
        try:
            scraper = PCdiga('pcdiga_links.txt')
            scraper.request()
            await ctx.channel.purge()
            for product_str in scraper.result2Embed():
                await ctx.send(embed=product_str.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url))
            
        except Exception:
            await ctx.send('Problema no ficheiro dos links! (Talvez esteja vazio)')


    @commands.command(name='get_links', help='Comando que mostra os links a serem usados e nome dos mesmos em qualquer loja suportada.')
    async def get_links(self, ctx, site_name : str = None ):
        site_name = site_name.lower() if site_name is not None else site_name

        if site_name == 'pcdiga':
            with codecs.open('pcdiga_links.txt','r','utf-8') as f:
                lines = f.readlines()
                res = '```\n'
                if len(lines) == 0:
                    await ctx.send(f'Ficheiro de links **{site_name}** está vazio!')
                    return
                for num, line in enumerate(lines):
                    res += f'{num + 1} - {line[23:]}'

                await ctx.send('**LINKS:** (https://www.pcdiga.com/)\n' + res + '```')
        else:
            sites = ', '.join(list(map(lambda strr: f'  -> **{strr}**\n', SITES)))
            await ctx.send(f'**Nome do site em falta!** (!get_links <nome_do_site>)\n*Opções:*\n{sites}')

    @commands.command(name='rm_link', help='Comando que remove um link a ser usado numa loja')
    async def rm_link(self, ctx, site_name : str = None, line : int = None):

        if line == None and site_name == None:
            await ctx.send('**Nome do site e número de linhas não fornecido!**')
            return
        elif line == None:
            await ctx.send('**Número da linha não fornecido!**')
            return

        site_name = site_name.lower() if site_name is not None else site_name
        
        if site_name in SITES:
            with codecs.open(f'{site_name}_links.txt','r','utf-8') as fr:
                lines = fr.readlines()
                if len(lines) == 0 or line > len(lines):
                    await ctx.send(f'Linha **{line}** não existe no ficheiro ou ficheiro vazio!')
                    return
                line_removed = lines.pop(line - 1)
            
            with codecs.open(f'{site_name}_links.txt','w','utf-8') as fw:
                for ln in lines:
                    fw.write(ln)

        else:
            sites = ', '.join(list(map(lambda strr: f'  -> **{strr}**\n', SITES)))
            await ctx.send(f'**Nome do site em falta ou mal escrito!** (!rm_link <nome_do_site> <linha>)\n*Opções:*\n{sites}')
            return
        
        await ctx.send(f'Linha **{line}** - **{line_removed[23:]}** removida do ficheiro **{site_name}**.')
