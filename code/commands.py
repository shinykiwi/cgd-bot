import asyncio
import datetime
import interactions
from interactions import Intents
from discord import Attachment, Role
from interactions import ComponentContext
from interactions.ext.wait_for import wait_for_component, setup
from interactions.ext.paginator import Paginator, Page

bot = interactions.Client(token="MTA1NDQzMTA1NDIzODMyNjg1NA.GHB8eb.C5XsQ3LtPdTwNS3GmGR_0PAsPwXiBbRQpH8ZDE",
                          intents=Intents.DEFAULT | Intents.GUILD_MESSAGE_CONTENT)

setup(bot)


# Submits an emoji to the channel for voting
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

# Creates a new custom embed based on user input
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
                image: Attachment = None, thumbnail: Attachment = None, color: str = None):
    c = int("5865F2", 16)

    if color:
        if color.startswith("#"):
            c = int(color[1:], 16)

    new_embed = interactions.Embed(
        title=title,
        description=description,
        color=c,
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


@bot.command(
    name="reaction_role",
    description="Adds a reaction role onto the message.",
    scope=1054436256676860054,
    options=[
        interactions.Option(
            name="message_id",
            description="The ID of the message you want to add the reaction role to.",
            type=interactions.OptionType.STRING,
            required=True,
        ),
        interactions.Option(
            name="emoji",
            description="The emoji you want to add to the message that triggers the role adding.",
            type=interactions.OptionType.STRING,
            required=True,
        ),
        interactions.Option(
            name="role",
            description="The role you want to give to the user when they react.",
            type=interactions.OptionType.ROLE,
            required=True,
        ),
    ],
)
async def reaction_role(ctx: interactions.CommandContext, message_id: int, emoji: str, role: Role):
    await ctx.send("Done!")


@bot.command(
    name="calendar",
    description="Shows this semester's most up to date calendar.",
    scope=1054436256676860054,
)
async def calendar(ctx: interactions.CommandContext):
    pages = [
        Page(
            embeds=interactions.Embed(
                title="January",
                description="Last updated: <t:1671394504:R>",
                image=interactions.EmbedImageStruct(
                    url="https://cdn.discordapp.com/attachments/1054436257259847752/1054493897176395896/image.png"),
                color=int("5865F2", 16),
            ),

        )
    ]

    await ctx.send(embeds=embed)

# Edits an existing embed's title and/or description
@bot.command(
    name="edit_embed",
    description="Edit an existing embed's content.",
    scope=1054436256676860054,
    options=[
        interactions.Option(
            name="message_id",
            description="Right click a message and click \'Copy ID\'",
            type=interactions.OptionType.STRING,
            required=True,
        ),
        interactions.Option(
            name="title",
            description="Change the title.",
            type=interactions.OptionType.STRING,
            required=False,
        ),
        interactions.Option(
            name="description",
            description="Change the description.",
            type=interactions.OptionType.STRING,
            required=False,
        )
    ]
)
async def edit_embed(ctx: interactions.CommandContext, message_id: str, title: str = None, description: str = None):
    message = await ctx.channel.get_message(int(message_id))
    membed = message.embeds[0]

    if not(title or description):
        await ctx.send("You did not specify any fields to edit! Please use the command again. ❌", ephemeral=True)
    else:
        if title:
            membed.title = title
        if description:
            membed.description = description
        await message.edit(embeds=membed)
        await ctx.send("Embed edited! ✅", ephemeral=True)


bot.start()
