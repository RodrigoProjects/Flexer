import os
import codecs

from PCdiga import PCdiga
from error_handler import CommandErrorHandler
from scraper_cmds import Scraper

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
SITES = ['pcdiga']

bot = commands.Bot(command_prefix='!')

# Classe responsável por tratar de erros.
bot.add_cog(CommandErrorHandler(bot))

# Classes com os comandos separados por categoria.
bot.add_cog(Scraper(bot))


# client = discord.Client()

# Iniciar o bot.
bot.run(TOKEN)
