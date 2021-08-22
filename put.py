import requests, app

guild_id = ""


botToken = app.app.config["DISCORD_BOT_TOKEN"]
headers = {
    'Content-Type': 'application/json; charset=utf-8',
    'authorization': 'Bot '+ botToken,
}
with open("token.txt", "r", encoding='utf8') as fp: t = fp.read().split("\n")
for i in t:
    try:
            
        i = i.split(":")
        res = requests.put(f"https://discord.com/api/v6/guilds/{guild_id}/members/{i[1]}", json={'access_token': i[0]}, headers=headers)
        print(res.text)
    except:
        pass
print("End")