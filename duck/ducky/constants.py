import json
with open("ducky/secrets.json", "r") as f:
	secrets = json.load(f)
db_password = secrets['db']['password']
db_host = secrets['db']['host']
db_name = secrets['db']['name']
db_user = secrets['db']['user']
db_port = secrets['db']['port']
client_secret = secrets['client secret']
secret_key = secrets['secret key']
client_id = secrets['client id']
ipc_password = secrets['ipc password']
