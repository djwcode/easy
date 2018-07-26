import os
import psycopg2
from datetime import datetime
import discord
from discord.ext import commands
from settings import token
import sys
import traceback


DATABASE_URL = os.environ['DATABASE_URL']

# Loading cogs (Help must always be last)
initial_extensions = ['cogs.Chat',
                      'cogs.Bot',
                      'cogs.Owner',
                      'cogs.General',
                      'cogs.Challonge',
                      'cogs.Help']

bot = commands.Bot(command_prefix='w.')
bot.remove_command("help")


if __name__ == '__main__':
    for extension in initial_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print(f'Failed to load extension {extension}.', file=sys.stderr)
            traceback.print_exc()


@bot.event
async def on_message(message):
    # logging
    time = str(message.created_at.replace(microsecond=0))
    user = str(message.author)
    msg = message.clean_content
    if isinstance(message.channel, discord.TextChannel):
        channel = message.channel.name
        server = message.guild.name
    elif isinstance(message.channel, discord.DMChannel):
        channel = str(message.channel.recipient)
        server = "DMChannel"
    print("UTC" + time + "| " + server + "| " + channel + "| " + user + ": " + msg)
    if not message.author.bot:
        if message.content.lower() in ('what are you', 'what r u', 'wat are u', 'wat r you', 'what r you', 'what are u', 'wat are you', 'wat r u'):
            await message.channel.send("AN IDIOT SANDWICH :bread::sob::bread:")

        if "shrug" in message.content.lower():
            await message.channel.send("¯\\_(ツ)_/¯")

        if "sosig" in message.content.lower():
            embed = discord.Embed(color=0x48d1cc)
            embed.set_image(url="https://static.tumblr.com/90c42824de11581fb88945e0988e7510/gsvg9km/c9kov82iq/tumblr_static_tumblr_static__640.png")
            await message.channel.send(embed=embed)
    await bot.process_commands(message)


@bot.event
async def on_connect():
    connect_time = str(datetime.utcnow().replace(microsecond=0))
    print("-------------------")
    print(connect_time)
    print("Connected")
    print("-------------------")

    create_tournaments_table = """ CREATE TABLE IF NOT EXISTS tournaments (
                                        ID int PRIMARY KEY,
                                        url text NOT NULL,
                                        name text NOT NULL,
                                        creator_id text NOT NULL,
                                        admins text
                                        ); """

    # conn = psycopg2.connect(database='willabot_db')
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    c = conn.cursor()
    c.execute(create_tournaments_table)
    conn.commit()
    conn.close()


@bot.event
async def on_ready():
    ready_time = str(datetime.utcnow().replace(microsecond=0))
    print("-------------------")
    print(ready_time)
    print("Version: " + discord.__version__)
    print("Logged in as")
    print(bot.user.name)
    print(bot.user.id)
    print("-------------------")
    game = discord.Game("w.help")
    await bot.change_presence(status=discord.Status.online, activity=game)


bot.run(token)