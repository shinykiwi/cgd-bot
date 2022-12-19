import asyncio
import datetime

import interactions
from discord import Attachment
from interactions import ComponentContext
from interactions.ext.wait_for import wait_for_component, setup

bot = interactions.Client(token="MTA1NDQzMTA1NDIzODMyNjg1NA.GHB8eb.C5XsQ3LtPdTwNS3GmGR_0PAsPwXiBbRQpH8ZDE")

setup(bot)


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


@bot.command(
    name="embed",
    description="Creates an embed with your info.",
    scope=1054436256676860054,
    options=[
        interactions.Option(
            name="title",
            description="The title of the embed.",
            type=interactions.OptionType.STRING,
            required=True,
        ),
        interactions.Option(
            name="description",
            description="The description of the embed.",
            type=interactions.OptionType.STRING,
            required=True,
        ),
        interactions.Option(
            name="show_author",
            description="Whether or not to show the author of the embed.",
            type=interactions.OptionType.BOOLEAN,
            required=True,
        ),
        interactions.Option(
            name="color",
            description="The color in hex code of the embed.",
            type=interactions.OptionType.STRING,
            required=False,
        ),
        interactions.Option(
            name="image",
            description="The main image of the embed to show on bottom. (Optional)",
            type=interactions.OptionType.ATTACHMENT,
            required=False,
        ),
        interactions.Option(
            name="thumbnail",
            description="The upper-right corner image (Optional).",
            type=interactions.OptionType.ATTACHMENT,
            required=False,
        )
    ],
)
async def embed(ctx: interactions.CommandContext, title: str, description: str, show_author: bool,
                image: Attachment = None, thumbnail: Attachment = None, color: str = None, ):
    if color:
        color.startswith("#")
        color = int(color[1:], 16)
    else:
        color = int("5865F2", 16),

    new_embed = interactions.Embed(
        title=title,
        description=description,
        color=color,
        image=interactions.EmbedImageStruct(url=image.url) if image else None,
        author=interactions.EmbedAuthor(
            name=ctx.author.name,
            icon_url=f"https://cdn.discordapp.com/avatars/{ctx.author.id}/{ctx.author.avatar}.png"
        ) if show_author else None,
        thumbnail=interactions.EmbedImageStruct(url=thumbnail.url) if thumbnail else None
    )

    comps = [
        interactions.Button(style=interactions.ButtonStyle.SUCCESS, label="Yes, post it!", custom_id="yes"),
        interactions.Button(style=interactions.ButtonStyle.DANGER, label="No", custom_id="no"),
    ]

    await ctx.send("Is this how you want it to look?", embeds=new_embed, components=comps, ephemeral=True)

    async def check(button_ctx: ComponentContext):
        if int(button_ctx.author.user.id) == int(button_ctx.author.user.id):
            # Returning true if the correct player clicked the button
            return True

        return False

    try:
        button_ctx: ComponentContext = await bot.wait_for_component(
            components=comps, check=check, timeout=60
        )
        if button_ctx.custom_id == "yes":
            await button_ctx.send(embeds=new_embed)
        elif button_ctx.custom_id == "no":
            await button_ctx.send("Okay, I won't post it. Please use the command `/embed` to redo it.")
    except asyncio.TimeoutError:
        await ctx.send("You took too long to respond!", ephemeral=True)
        return


bot.start()
