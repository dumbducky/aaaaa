import discord
from discord.ext import commands
import requests
from ...constants import client_secret, client_id

class OAuth():
	client_id = client_id
	client_secret = client_secret
	scope = "identify%20guilds"
	redirect_uri = "http://localhost:8000"
	discord_login_url = f"https://discord.com/api/oauth2/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code&scope={scope}"
	discord_token_url = "https://discord.com/api/oauth2/token"
	discord_api_url = "https://discordapp.com/api"

	def __init__(self, bot = None):
		if bot is None:
			pass
		else:
			self.bot = bot

	@staticmethod
	def get_access_token(code):
		payload = {
			"client_id": OAuth.client_id,
			"client_secret": OAuth.client_secret,
			"grant_type": "authorization_code",
			"code": code,
			"redirect_uri": OAuth.redirect_uri,
			"scope": OAuth.scope
		}

		headers = {
   			'Content-Type': 'application/x-www-form-urlencoded'
 		}

		access_token = requests.post(url=OAuth.discord_token_url, data=payload, headers=headers)
		json = access_token.json()
		return json.get("access_token")

	@staticmethod
	def get_user_json(access_token):
		url = OAuth.discord_api_url+"/users/@me"

		headers = {
			"Authorization": f"Bearer {access_token}"
		}

		user_object = requests.get(url=url, headers=headers)
		user_json = user_object.json()

		return user_json

	@staticmethod
	def get_user_guilds(access_token):
		url = OAuth.discord_api_url+"/users/@me/guilds"

		headers = {
			"Authorization": f"Bearer {access_token}"
		}

		guilds_object = requests.get(url=url, headers=headers)
		guilds = guilds_object.json()
		return guilds



async def log(pg, log_type, log_bool):
	query = """UPDATE logging
	SET message_edits = $2
	WHERE server_id = 805638877762420786"""
	await pg.execute(query, log_type, log_bool)
