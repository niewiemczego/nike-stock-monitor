from typing import Dict
from discord_webhook import DiscordWebhook, DiscordEmbed
import time

def send_webhook(release_data: Dict):
    for _, release in enumerate(release_data.items()):
        webhook = DiscordWebhook(
            url="YOUR DISCORD WEBHOOK URL" 
        ) 
        embed = DiscordEmbed(color="92A9BD")
        embed.set_thumbnail(url=release[1]['image'])
        embed.add_embed_field(
            name="**Product Name**", 
            value=release[1]['title'], 
            inline=False
        )
        embed.add_embed_field(
            name="**Stock Levels**", 
            value="\n".join(release[1]['sizes']), 
            inline=True
        )
        embed.add_embed_field(
            name="**SKU**", 
            value=release[0], 
            inline=True
        )
        embed.add_embed_field(
            name="**Launch Type**", 
            value=release[1]['releaseType'], 
            inline=True
        )
        embed.add_embed_field(
            name="**Launch Date**", 
            value=release[1]['releaseDate'], 
            inline=True
        )
        embed.add_embed_field(
            name="**Price**", 
            value=f"{release[1]['price']} {release[1]['currency']}", 
            inline=True
        )
        embed.add_embed_field(
            name="**Exclusive Access**", 
            value=release[1]['exclusiveAccess'], 
            inline=True
        )
        # CHANGE FOR YOUR NEEDS
        embed.set_footer(
            text="Tim Solutions makes difference", 
            icon_url="https://i.imgur.com/8KANDeK.jpg"
        )
        embed.set_timestamp()
        webhook.add_embed(embed)
        response = webhook.execute()
        time.sleep(1)