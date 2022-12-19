import datetime

import interactions
from discord import Attachment

bot = interactions.Client(token="MTA1NDQzMTA1NDIzODMyNjg1NA.GF9ecw.RoCGzzKxTqvf0dMA7I_hHKARyASQ5mlWkJDabk")


@bot.command(
    name="submit_emoji",
    description="Creates an embed with your info.",
    scope=1054436256676860054,
    options=[
        interactions.Option(
            name="name",
            description="The name of the emoji you want to submit.",
            type=interactions.OptionType.STRING,
            required=True,
        ),
        interactions.Option(
            name="emoji",
            description="The image or gif of the emoji you want to submit.",
            type=interactions.OptionType.ATTACHMENT,
            required=True,
        ),
    ],
)
async def submit_emoji(ctx: interactions.CommandContext, name: str, emoji: Attachment):
    embed = interactions.Embed(
        title=name,
        description=f"Submitted by {ctx.author.mention}",
        image=interactions.EmbedImageStruct(url=emoji.url),
        color=int("5865F2", 16),
        author=interactions.EmbedAuthor(
            name=ctx.author.name,
            icon_url=f"https://cdn.discordapp.com/avatars/{ctx.author.id}/{ctx.author.avatar}.png"
        )
    )

    await ctx.send(embeds=embed)

    await ctx.message.create_reaction("✅")
    await ctx.message.create_reaction("❌")



bot.start()
