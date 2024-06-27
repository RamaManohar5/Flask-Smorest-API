import requests
from dotenv import load_dotenv
import os

load_dotenv()

DOMAIN = os.getenv("MAILGUN_DOMAIN")

def send_simple_message(to, subject, body):
    api_key = os.getenv("MAILGUN_API_KEY")
    return requests.post(
		f"https://api.mailgun.net/v3/{DOMAIN}/messages",
		auth=("api", api_key),
		data={"from": f"RamaManohar <mailgun@{DOMAIN}>",
			"to": [to],
			"subject": subject,
			"text": body})


def send_user_registration_message(email, username):
    return send_simple_message(
        email,
        "successfully registered",
        f"Hi {username}, you have successfully signed up to the stores REST API"
    )
