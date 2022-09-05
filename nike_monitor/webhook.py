from typing import Any

from discord_webhook import DiscordEmbed, DiscordWebhook

from .release import Release


def send_webhook(webhook_url: str, release: Release):
    """
    > The function takes a webhook URL and a release object as arguments, and sends a Discord webhook to
    the URL with the release object's data
    
    :param webhook_url: The webhook URL you got from Discord
    :type webhook_url: str
    :param release: Release
    :type release: Release
    """
    webhook = DiscordWebhook(
        url=webhook_url
    ) 
    embed = DiscordEmbed(color="92A9BD")
    embed.set_thumbnail(url=release.image)
    embed.add_embed_field(
        name="**Product Name**", 
        value=f"[{release.title}]({release.url})", 
        inline=False
    )
    embed.add_embed_field(
        name="**Stock Levels**", 
        value="\n".join(release.sizes_with_stock), 
        inline=True
    )
    embed.add_embed_field(
        name="**SKU**", 
        value=release.sku, 
        inline=True
    )
    embed.add_embed_field(
        name="**Launch Type**", 
        value=release.type, 
        inline=True
    )
    embed.add_embed_field(
        name="**Launch Date**", 
        value=release.date, 
        inline=True
    )
    embed.add_embed_field(
        name="**Price**", 
        value=f"{release.price} {release.currency}", 
        inline=True
    )
    embed.add_embed_field(
        name="**Exclusive Access**", 
        value=release.exclusive_access, 
        inline=True
    )
    embed.set_footer(
        text="Tim Solutions makes difference", 
        icon_url="https://i.imgur.com/8KANDeK.jpg"
    )
    embed.set_timestamp()
    webhook.add_embed(embed)
    response = webhook.execute()
