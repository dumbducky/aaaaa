from django.shortcuts import render
from django.http import HttpResponse
from urllib import request
from ast import literal_eval
from ducky.templates.ducky.bot_stuff import log, OAuth
client_secret = OAuth.client_secret
from discord.ext import ipc
import asyncio
import psycopg2
from psycopg2 import sql
import json
from ducky.constants import db_name, db_password, db_user, db_host, ipc_password

try:
	loopeydoopeywuackey = asyncio.get_event_loop()
	ipc_client = ipc.Client(secret_key=ipc_password)
except RuntimeError:
	pass # useless until live stats added... then panic

cxn = psycopg2.connect(
    host=db_host,
    database=db_name,
    user=db_user,
    password=db_password)

cur = cxn.cursor()
def base(request):
	try:
		user_json = literal_eval(request.COOKIES.get('user_json'))
	except ValueError:
		user_json = None
	return {"user_json": user_json}

def index(request):
	try:
		user_json = literal_eval(request.COOKIES.get('user_json'))
	except ValueError:
		code = request.GET.get("code")
		if code:
			access_token = OAuth.get_access_token(code)
			user_json = OAuth.get_user_json(access_token)
			response = render(request, "ducky/home.html", {"user_json": user_json})
			response.set_cookie("user_json", user_json)
		else:
			response = render(request, "ducky/home.html", {"user_json": None})
		return response
	return render(request, "ducky/home.html", {"user_json": user_json})
	
def cog(request, cog_name):
	json = base(request)
	return render(request, f"ducky/cogs/{cog_name}.html", json)

def administration(request):
	return cog(request, "administration")

def automod(request):
	return cog(request, "automod")

def bot(request):
	return cog(request, "bot")

def conversion(request):
	return cog(request, "conversion")

def files(request):
	return cog(request, "files")

def info(request):
	return cog(request, "info")

def logging(request):
	return cog(request, "logging")

def moderation(request):
	return cog(request, "moderation")

def roles(request):
	return cog(request, "roles")

def server(request):
	return cog(request, "server")

def stats(request):
	return cog(request, "stats")

def time(request):
	return cog(request, "time")

def tracking(request):
	return cog(request, "tracking")

def users(request):
	return cog(request, "users")

def utils(request):
	return cog(request, "utils")

def warn(request):
	return cog(request, "warn")

def server_select(request):
	arg_json = base(request)
	guilds = request.session.get('guilds')
	used_guilds = []
	try:
		user_json = literal_eval(request.COOKIES.get("user_json"))
	except ValueError: # if somehow the user isnt logged in
		return render(request, "ducky/error.html", {"error": "unauthorized_guilds"})
	for guild in guilds:
		try:
			if loopeydoopeywuackey.run_until_complete(ipc_client.request(
			"manage_guild_bool",
			guild_id=guild['id'],
			user_id=user_json['id'])):
				used_guilds.append(guild)
		except TypeError: # if i cant access guilds
			return render(request, "ducky/error.html", {"error": "unauthorized_guilds"})
	arg_json['guilds'] = used_guilds
	return render(request, "ducky/server_select.html", arg_json)

def config(request):
	json = base(request)
	json['guild_id'] = request.session.get('guild_id')
	return render(request, "ducky/config.html", json)

def api_cookie(request):
	request.session['guild_id'] = request.POST[request.POST['title']]
	return HttpResponse("Django bitches if i dont return a HttpResponse object so here it is")

def api_logging(request):
	log_type = request.POST['log_type']
	log_bool = request.POST['log_bool']
	guild_id = request.POST['guild_id']
	log_bool = True if log_bool == "true" else False
	dumb_dict = {
		"deletes": "message_deletions",
		"edits": "message_edits",
		"roles": "role_changes",
		"names": "name_updates",
		"voice": "voice_state_updates",
		"avatars": "avatar_changes",
		"moderation": "bans", 
		"channels": "channel_updates",
		"leaves": "leaves",
		"joins": "joins",
		"server": "server_updates",
		"emojis": "emojis",
		"invites": "discord_invites"
	}
	log_type = dumb_dict[log_type]
	cur.execute(
    sql.SQL("UPDATE logging SET {} = (%s) WHERE server_id = (%s)")
        .format(sql.Identifier(log_type)),
    	[log_bool, guild_id])
	cxn.commit()
	return HttpResponse("Why are you looking at this... I'm just inserting the data into a db...")

async def testing(req):
	return await ipc_client.request("testing")

def log_out(req):
	print("stuff")
	response = HttpResponse("stuff")
	try:
		del req.session['guilds']
	except KeyError:
		pass
	response.delete_cookie('user_json')
	return response