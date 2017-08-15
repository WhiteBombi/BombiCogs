import discord
from discord.ext import commands

from datetime import datetime

class Countdown:

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def countdown(self, deadline, link, *, eventname):
        '''Shows time remaining for an event.

           Usage: [p]countdown YYMMDDHHMM(Year, Month, Day, Hour, Minute) https://goo.gl Event name

           Calculation will use GMT time, so adjust your time machine reading skills accordingly.

           Hint: Designed to work with aliases. Example:
           !alias add nextstream countdown 1801011200 http://www.twitch.tv/whitebombo Next stream
           !nextstream
           '''

        def Timer(deadline):
            '''Gives the time remaining until <target> (YYMMDDHHMM)'''

            deadline = str(deadline)

            now = datetime.now()
            deadline = datetime(
                int(deadline[:2]) + 2000, #Year
                int(deadline[2:4]),       #Month
                int(deadline[4:6]),       #Day
                int(deadline[6:8]),       #Hour
                int(deadline[8:10])       #Minute
                )
            if deadline < now:
                return None

            togo = deadline - now
            togo = togo.total_seconds()

            togo = (
                str(int(togo / 3600 / 24)) + ' days ',
                str(int(togo / 3600) % 24) + ' hours ',
                str(int((togo % 3600) / 60)) + ' minutes ',
                str(int(togo % 60)) + ' seconds',
                )

            output = ''
            for i in togo:
                '''Pass forward max two populated strings from togo to output.'''
                if (int(i[:2]) is not 0) and (len(output) <= 14):
                    output += i

            return output

        '''Final output'''
        timer = Timer(deadline)
        if timer is None:
            await self.bot.say('{} is happening! {}'.format(eventname, link))
        else:
            await self.bot.say('{} will happen in {}'.format(eventname, Timer(deadline)))

def setup(bot):
    bot.add_cog(Countdown(bot))
