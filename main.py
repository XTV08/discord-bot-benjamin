import discord
import datetime
import asyncio
from discord.ext import commands
from discord.ext import tasks
from pytz import timezone

intents = discord.Intents.all()
activity = discord.Activity(name="a hacking competition for monkeys", type=5)

bot = commands.Bot(command_prefix='!', intents=intents, activity=activity)

normal_count = {}
relic_count = {}
banner_count = {}

count_channel_id = 1057306342475452426
count_message_id = ''
notification_channel_id = 1012487621534023783
rules_channel_id = 1049794978722885662
rules_message_id = 1057309461976461362

#######################################################
### BOT COMMANDS ###

@bot.command(name='set_normal')
@commands.has_any_role('Leader', 'Assistant Mayor')
async def set_normal(ctx, user: discord.Member, new_score):
    "Sets a specific normal tiles score for a person, requires the discord nickname of this person as argument and the new score. I.e. [!set_normal -T- 1]"

    # check if the right channel and message exists
    if count_channel_id == '' or count_message_id == '':
        await ctx.send('Uhh, guys? There is no scoreboard!')
        return
    
    user_id = user.id
    if user_id in normal_count:
        normal_count[user_id] = int(new_score)
    await ctx.send(f'{user.display_name} now has {normal_count[user_id]} normal tiles.')

    # Update initial message with the new counts
    channel = bot.get_channel(count_channel_id)
    message = await channel.fetch_message(count_message_id)
    content = create_message_content()
    await message.edit(content=content)

@bot.command(name='set_relic')
@commands.has_any_role('Leader', 'Assistant Mayor')
async def set_relic(ctx, user: discord.Member, new_score):
    "Sets a specific relic tiles score for a person, requires the discord nickname of this person as argument and the new score. I.e. [!set_relic -T- 2]"

    # check if the right channel and message exists
    if count_channel_id == '' or count_message_id == '':
        await ctx.send('Uhh, guys? There is no scoreboard!')
        return
    
    user_id = user.id
    if user_id in relic_count:
        relic_count[user_id] = int(new_score)
    await ctx.send(f'{user.display_name} now has {relic_count[user_id]} relic tiles.')

    # Update initial message with the new counts
    channel = bot.get_channel(count_channel_id)
    message = await channel.fetch_message(count_message_id)
    content = create_message_content()
    await message.edit(content=content)

@bot.command(name='set_banner')
@commands.has_any_role('Leader', 'Assistant Mayor')
async def set_banner(ctx, user: discord.Member, new_score):
    "Sets a specific banner tiles score for a person, requires the discord nickname of this person as argument and the new score. I.e. [!set_banner -T- 5]"

    # check if the right channel and message exists
    if count_channel_id == '' or count_message_id == '':
        await ctx.send('Uhh, guys? There is no scoreboard!')
        return
    
    user_id = user.id
    if user_id in banner_count:
        banner_count[user_id] = int(new_score)
    await ctx.send(f'{user.display_name} now has {banner_count[user_id]} banner tiles.')

    # Update initial message with the new counts
    channel = bot.get_channel(count_channel_id)
    message = await channel.fetch_message(count_message_id)
    content = create_message_content()
    await message.edit(content=content)

@bot.command(name='reset_tiles')
@commands.has_any_role('Leader', 'Assistant Mayor')
async def reset_tiles(ctx):
    "Resets the tile scores (= 0) for everyone. I.e. [!reset_tiles]"

    # check if the right channel and message exists
    if count_channel_id == '' or count_message_id == '':
        await ctx.send('Uhh, guys? There is no scoreboard!')
        return
    
    # Set the initial counts for each emoji to 0 for every user in the server
    for user in bot.guilds[0].members:
        if user.bot:
            continue
        normal_count[user.id] = 0
        relic_count[user.id] = 0
        banner_count[user.id] = 0

    # Update initial message with the new counts
    channel = bot.get_channel(count_channel_id)
    message = await channel.fetch_message(count_message_id)
    content = create_message_content()
    await message.edit(content=content)

    await ctx.send('Have you tried turning it off and on again? The tiles have been reset!')

@bot.command(name='terminate')
@commands.is_owner()
async def terminate(ctx):
    "Kills @Benjamin. Only to be used by the leader."

    # close the bot
    await ctx.send('Game over, man!')
    await ctx.bot.close()

@bot.command(name='rules')
@commands.has_any_role('Leader', 'Assistant Mayor')
async def rules(ctx, new_description):
    "Edits the rules message in the #rules channel. (Use with care)"

    # Edit the rules
    channel = bot.get_channel(rules_channel_id)
    message = await channel.fetch_message(1057309461976461362)
    embed=discord.Embed(title="RULES", description=new_description, color=0x05f435)
    message = await message.edit(embed=embed)

@bot.command(name='announcement')
@commands.has_any_role('Leader', 'Assistant Mayor')
async def announcement(ctx, description):
    "Creates an announcement in the same channel where this command is used, requires a description as first argument. I.e. [!announcement \"This is an announcement\"]"

    # Create an announcement
    embed=discord.Embed(title="ANNOUNCEMENT", description=description, color=0x03f3f3)
    await ctx.send(embed=embed)

@bot.command(name='poll')
@commands.has_any_role('Leader', 'Assistant Mayor')
async def poll(ctx, description, reaction1=None, reaction2=None, reaction3=None, reaction4=None, reaction5=None):
    "Creates a poll in the same channel where this command is used, requires a description as first argument and emojis (reactions) as other arguments (up to 5). I.e. [!poll \"Do you like candy?\" ✅ ❌]"

    # Create a poll
    embed=discord.Embed(title="POLL", description=description, color=0x949ad0)
    message = await ctx.send(embed=embed)
    await message.add_reaction(reaction1)
    await message.add_reaction(reaction2)
    await message.add_reaction(reaction3)
    await message.add_reaction(reaction4)
    await message.add_reaction(reaction5)

@bot.command(name='instructions_scoreboard')
@commands.has_any_role('Leader', 'Assistant Mayor')
async def instructions_scoreboard(ctx):
    "Creates a message with the instructions of the tile scoreboard in the same channel where this command is used. I.e. [!instructions_scoreboard]"

    embed=discord.Embed(title="INSTRUCTIONS", description="\n\nPlease react to the score message of the bot with the tile you have recently captured: \n\n1. Normal tile (<:normal:1054800249861972059>)\n2. Relic tile (<:relic:1054800272121151518>)\n3. Banner tile (<:banner:1054800296930451617>)\n\nAfter you have reacted with a tile, please wait until the bot has automatically removed your reaction and added the tile to your name. You can then react again if you have captured multiple tiles of the same type. Each normal tile counts as 1 and each relic/banner tile counts as 2 in the tile score system. \n\n**NOTE:\nYOU ARE RESPONSIBLE TO KEEP TRACK OF YOUR OWN SCORE, IF THERE IS A MISTAKE, PLEASE CONTACT THE LEADER OR AN ASSISTANT MAYOR TO CORRECT YOUR SCORE.**\n", color=0xed0202)
    await ctx.send(embed=embed)

@bot.command(name='scoreboard')
@commands.has_any_role('Leader', 'Assistant Mayor')
async def scoreboard(ctx):
    "Creates a new scoreboard in the same channel where this command is used. I.e. [!scoreboard]"

    # Create a new scoreboard
    # Create the initial message with the reactions
    message = await ctx.send("React to this message with an emote:")
    await message.add_reaction("<:normal:1054800249861972059>")
    await message.add_reaction("<:relic:1054800272121151518>")
    await message.add_reaction("<:banner:1054800296930451617>")

    # Set the initial counts for each emoji to 0 for every user in the server
    for user in bot.guilds[0].members:
        if user.bot:
            continue
        normal_count[user.id] = 0
        relic_count[user.id] = 0
        banner_count[user.id] = 0

    # Update the message with the initial counts for each user and get ID
    content = create_message_content()
    await message.edit(content=content)
    global count_message_id
    count_message_id = message.id
    global count_channel_id
    count_channel_id = message.channel.id

@bot.command(name='recount_scoreboard')
@commands.has_any_role('Leader', 'Assistant Mayor')
async def recount_scoreboard(ctx, new_message_id):
    "Sets a specific message as tile scoreboard, requires message ID as argument. I.e. [!recount_scoreboard 0123456789]"

    # check if there is a right channel
    global count_channel_id
    if count_channel_id == '':
        await ctx.send('Uhh, guys? There is no scoreboard!')
        return

    # Update initial message
    channel = bot.get_channel(count_channel_id)
    message = await channel.fetch_message(new_message_id)
    
    # Create a new scoreboard
    # Create the initial message with the reactions
    await message.edit(content="React to this message with an emote:")
    await message.add_reaction("<:normal:1054800249861972059>")
    await message.add_reaction("<:relic:1054800272121151518>")
    await message.add_reaction("<:banner:1054800296930451617>")

    # Update the message with the current counts for each user and get ID
    content = create_message_content()
    await message.edit(content=content)
    global count_message_id
    count_message_id = message.id
    count_channel_id = message.channel.id

    # Send message when successful
    await ctx.send("Have you tried turning it off and on again? I should count properly now!")

###################################################################################
### EVENTS ###

@bot.event
async def on_reaction_add(reaction, user):
    if user.bot:
        return
    
    # Only track reactions in the channel of the counts
    if reaction.message.id != count_message_id:
        return

    # Increment the count for the appropriate emoji
    if str(reaction.emoji) == "<:normal:1054800249861972059>":
        normal_count[user.id] += 1
    elif str(reaction.emoji) == "<:relic:1054800272121151518>":
        relic_count[user.id] += 1
    elif str(reaction.emoji) == "<:banner:1054800296930451617>":
        banner_count[user.id] += 1

    # Update the message with the new counts
    content = create_message_content()
    await reaction.message.edit(content=content)

    # Remove the reaction, so the user can react again
    await reaction.message.remove_reaction(reaction, user)

####################################################################################
### FUNCTIONS ###

def create_message_content():
    # Create a string with the counts for each user
    content = ""
    for user in bot.guilds[0].members:
        # Skip the bot
        if user.bot:
            continue
        if normal_count[user.id] >= 0:
            content += f"```asciidoc\n[{user.display_name}]\nNormal tiles: {normal_count[user.id]} \nRelic tiles: {relic_count[user.id]} \nBanner tiles: {banner_count[user.id]} \nTile score: {normal_count[user.id]+2*(relic_count[user.id]+banner_count[user.id])}\n\n\n```"
        else:   # a new user joins the server
            normal_count[user.id] = 0
            relic_count[user.id] = 0
            banner_count[user.id] = 0
            content += f"```asciidoc\n[{user.display_name}]\nNormal tiles: {normal_count[user.id]} \nRelic tiles: {relic_count[user.id]} \nBanner tiles: {banner_count[user.id]} \nTile score: {normal_count[user.id]+2*(relic_count[user.id]+banner_count[user.id])}\n\n\n```"
    return content

async def send_scheduled_message():
  message_time = datetime.datetime(2023,
                                   5,
                                   16,
                                   19,
                                   00,
                                   00,
                                   tzinfo=timezone('EST'))
  while True:
    # Calculate the time until the next scheduled message
    now = datetime.datetime.now(timezone('EST'))
    time_until_message = message_time - now

    # If it's time to send the message, do it and reset the tile score
    if time_until_message.total_seconds() <= 0:
        channel = bot.get_channel(notification_channel_id)
        await channel.send(
        "@everyone \n\n```md\n❗❗ ***ATTENTION*** ❗❗\n\nContested Territory has started again!\nYou can now open CT and use all your tickets. Let's get top 25! 💪``` \n"
        )
        
        # reset tiles
        # Set the initial counts for each emoji to 0 for every user in the server
        for user in bot.guilds[0].members:
            if user.bot:
                continue
            normal_count[user.id] = 0
            relic_count[user.id] = 0
            banner_count[user.id] = 0

        # Update initial message with the new counts
        global count_channel_id
        score_channel = bot.get_channel(count_channel_id)
        # Create a new scoreboard
        # Create the initial message with the reactions
        message = await score_channel.send("React to this message with an emote:")
        await message.add_reaction("<:normal:1054800249861972059>")
        await message.add_reaction("<:relic:1054800272121151518>")
        await message.add_reaction("<:banner:1054800296930451617>")

        # Update the message with the initial counts for each user and get ID
        content = create_message_content()
        await message.edit(content=content)
        global count_message_id
        count_message_id = message.id
        count_channel_id = message.channel.id

        # Calculate the time for the next scheduled message
        message_time += datetime.timedelta(weeks=2)

    # Wait for one minute before checking again
    await asyncio.sleep(60)
    print('beep...')

#################################################################################
### ON_READY ###

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    print(datetime.datetime.now(timezone('EST')))

    # send scheduled message
    await send_scheduled_message()

#################################################################################

TOKEN = DISCORD_API_TOKEN

bot.run(TOKEN)
