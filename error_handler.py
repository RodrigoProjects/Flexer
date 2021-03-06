import traceback
import sys
from discord.ext import commands
import discord

class CommandErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """The event triggered when an error is raised while invoking a command.
        ctx   : Context
        error : Exception"""

        # This prevents any commands with local handlers being handled here in on_command_error.
        if hasattr(ctx.command, 'on_error'):
            return
        
        ignored = (commands.CommandNotFound)
        
        # Allows us to check for original exceptions raised and sent to CommandInvokeError.
        # If nothing is found. We keep the exception passed to on_command_error.
        error = getattr(error, 'original', error)
        
        # Anything in ignored will return and prevent anything happening.
        if isinstance(error, ignored):
            return

        elif isinstance(error, commands.DisabledCommand):
            return await ctx.send(f'**{ctx.command}** está desativado.')

        elif isinstance(error, commands.NoPrivateMessage):
            try:
                return await ctx.author.send(f'**{ctx.command}** não pode ser usado em mensagens privadas.')
            except:
                pass
        
        elif isinstance(error, commands.UserInputError):
            if ctx.command.qualified_name == 'rm_link':  # Check if the command being invoked is 'tag list'
                return await ctx.send('O segundo argumento tem de ser um número **inteiro** maior que zero (número da linha).')
            elif ctx.command.qualified_name == 'clear':
                return await ctx.send('O número de mensagens a apagar tem ser um **Inteiro** ou **Vazio**.')

        # For this error example we check to see where it came from...
        elif isinstance(error, commands.BadArgument):
            if ctx.command.qualified_name == 'rm_links':  # Check if the command being invoked is 'tag list'
                return await ctx.send('O número de linhas tem de ser um número **inteiro** maior que zero.')

        # All other Errors not returned come here... And we can just print the default TraceBack.
        print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
    
    