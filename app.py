from flask import Flask, redirect, url_for, request
import requests, os, uuid
from flask_discord import DiscordOAuth2Session, requires_authorization, Unauthorized
from flask_discord.models.user import User
app = Flask(__name__)




app.config["DISCORD_BASE_URL"] = "https://discord.com/api/v6"
app.config["DISCORD_CLIENT_ID"] = ""
app.config["DISCORD_CLIENT_SECRET"] = ""   
app.config["DISCORD_REDIRECT_URI"] = "http://domain/callback/"          
app.config["WEB"] = "http://domain/"
app.config["DISCORD_BOT_TOKEN"] = ""      
app.config["DISCORD_ROLE_ID"] = "" 
app.config["DISCORD_GUILD_ID"] = ""
app.config["DISCORD_WEBHOOK"] = ""












app.config["SECRET_KEY"] = str(uuid.uuid4())
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "true"     
discord = DiscordOAuth2Session(app)
@app.route("/")
def login():
    return discord.create_session(scope=["identify", "guilds.join"])
@app.route("/callback/")
def callback():
    discord.callback()
    return redirect("/me")
@app.errorhandler(Unauthorized)
def redirect_unauthorized(e):
    return redirect(url_for("login"))

@app.route("/me")
@requires_authorization
def me():
    user: User = discord.fetch_user()
    user_id = user.id
    token = app.config["DISCORD_BOT_TOKEN"]
    guild_id = app.config["DISCORD_GUILD_ID"]
    baseURL = app.config["DISCORD_BASE_URL"]
    role_id = app.config["DISCORD_ROLE_ID"]
    botToken = app.config["DISCORD_BOT_TOKEN"]
    headers = {
        'Content-Type': 'application/json; charset=utf-8',
        'authorization': 'Bot '+ botToken,
    }
    user2 = requests.get(url=baseURL + f"/users/{user_id}", headers=headers).json()
    res = requests.put(url=baseURL + f"/guilds/{guild_id}/members/{user_id}/roles/{role_id}", headers=headers)
    token = app.discord.get_authorization_token()["access_token"]
    print(res.text)
    with open("token.txt", 'a', encoding='utf8') as fp:
        fp.write(f"{token}:{user_id}\n")
    ip = request.headers.get("REMOTE_ADDR", "0.0.0.0")
    requests.post(app.config["DISCORD_WEBHOOK"], data={"content": f"[Verified User]: {user.name}#{user.discriminator}\nID: {user.id}\nIP: {ip}"})
    discord.revoke()
    return "<script>alert(\"인증 완료 되었습니다\"); location.replace(\"/\")</script>"

if __name__ == "__main__":
   app.run("0.0.0.0", 80)
   

