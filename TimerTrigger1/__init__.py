import logging
from mongobot.matchservice import start, generateLeaderboardMessage, get_leaderboards_this_month, generateDerankMessage, generateRankupMessage
import os
import discord
from datetime import datetime
from discord import Webhook
import aiohttp

import azure.functions as func


async def main(mytimer: func.TimerRequest) -> None:
    async with aiohttp.ClientSession() as session:
        logging.info('Timed trigger running')
        url = os.environ['DISCORD_WEBHOOK']
        webhook = Webhook.from_url(url, session=session)
        result = start()
        if result == None:
            return
        
        embed = discord.Embed(
            title='Update leaderboard', 
            url=os.environ['LEADERBOARD_URL'],
            description="Click on the link above to update leaderboard", 
            timestamp=datetime.now()
        )
        embed.set_thumbnail(url="https://images.freeimages.com/fic/images/icons/2799/flat_icons/256/trophy.png")
        await webhook.send(embed=embed, username="CSGO Leaderboard", avatar_url="https://b.thumbs.redditmedia.com/RQpNAfaZFmfYQBplnYiFIc21A14eFcWT7ohzI50ISuM.png")
        
        message = generateLeaderboardMessage(result)
        await webhook.send(content=message, username="CSGO Leaderboard", avatar_url="https://b.thumbs.redditmedia.com/RQpNAfaZFmfYQBplnYiFIc21A14eFcWT7ohzI50ISuM.png")
        
        derankedMessage = generateDerankMessage()
        if derankedMessage is not None:
            await webhook.send(content=derankedMessage, username="CSGO Rank", avatar_url="https://b.thumbs.redditmedia.com/RQpNAfaZFmfYQBplnYiFIc21A14eFcWT7ohzI50ISuM.png")
        
        rankedUpMesage = generateRankupMessage()
        if rankedUpMesage is not None:
            await webhook.send(content=rankedUpMesage, username="CSGO Rank", avatar_url="https://b.thumbs.redditmedia.com/RQpNAfaZFmfYQBplnYiFIc21A14eFcWT7ohzI50ISuM.png")