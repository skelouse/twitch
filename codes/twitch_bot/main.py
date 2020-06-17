
from twitchio.ext import commands
import config




class Bot(commands.Bot):

    def __init__(self):
        super().__init__(irc_token=config.irc_token, client_id=config.client_id, nick=config.nick, prefix=config.prefix,
                         initial_channels=config.channels)

    # Events don't need decorators when subclassed
    async def event_ready(self):
        print(f'Ready | {self.nick}')

    async def event_message(self, message):
        print(message.content)
        await self.handle_commands(message)

    # Commands use a different decorator
    @commands.command(name='test')
    async def my_command(self, ctx):
        await ctx.send(f'Hello {ctx.author.name}!')


bot = Bot()
bot.run()