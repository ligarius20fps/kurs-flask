import os
from dotenv import load_dotenv
import requests

load_dotenv()
DOMAIN = os.getenv("MAILGUN_DOMAIN")
def send_simple_message(to, subject, body):
    return requests.post(
		f"https://api.mailgun.net/v3/{DOMAIN}/messages",
		auth=("api", os.getenv("MAILGUN_API_KEY")),
		data={"from": f"mati <mailgun@{DOMAIN}>",
			"to": [to],
			"subject": subject,
			"text": body})

def send_registration_message(email, username):
	send_simple_message(
				to=email,
				subject="Successfully signed up",
				body=f"Hello, {username} and welcome to stores REST API"
			)