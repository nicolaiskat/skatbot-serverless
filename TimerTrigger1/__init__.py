import datetime
import logging
import discord
from discord import Webhook
import aiohttp

import azure.functions as func


async def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()
    
    async with aiohttp.ClientSession() as session:
        url = 'https://discord.com/api/webhooks/1109643464481714188/7Lw0nJm9MeSiFQMlqo9-2h1eINuhIQ3irqIxWFn59Ue3ewRCFau7mnu_qbVrt3Xz9W__'
        webhook = Webhook.from_url(url, session=session)
        embed = discord.Embed(title='This is a title')
        await webhook.send(embed=embed)
            
    if mytimer.past_due:
        logging.info('The timer is past due!')

    logging.info('Python timer trigger function ran at %s', utc_timestamp)