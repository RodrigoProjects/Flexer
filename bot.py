import os
import codecs

from error_handler import CommandErrorHandler
from scraper_cmds import Scraper
from general_cmds import General

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

# Classe responsável por tratar de erros.
bot.add_cog(CommandErrorHandler(bot))

# Classes com os comandos separados por categoria.

bot.add_cog(Scraper(bot)) # Comandos de dar Scrap em lojas na internet.
bot.add_cog(General(bot)) # Comandos gerais de um servidor.

# client = discord.Client()

# Iniciar o bot.
bot.run(TOKEN)
