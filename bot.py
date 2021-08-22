import discord
from app import app

intents = discord.Intents()
intents.members = True
intents.guild_messages = True
intents.guilds = True
intents.dm_messages = True

client = discord.Client()


@client.event
async def on_member_join(member):
    embed = discord.Embed()
    embed.title = "Authorization"
    embed.description = f"서버에서 활동 권한을 얻으시려면 [여기]({app.config['web']})를 클릭해 권한을 얻으세요."
    # embed.colour = discord.Colour
    try:
        await member.send(embed=embed)
    except:
        pass
#
client.run(app.config["ODc4OTQ0MDE2ODQ5MzA5Njk2.YSIiZw.v8yuM3WREtDaiac7wi_yP7IRz14"])
