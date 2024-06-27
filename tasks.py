import os
import requests
from dotenv import load_dotenv
from settings import REDIS_URL,QUEUES

# redis and rq for tasks management
import redis
from rq import Queue

import jinja2

load_dotenv()

# Establish connection to Redis
connection = redis.from_url(REDIS_URL)
# Initialize Queue for emails
queue = Queue(QUEUES[0], connection=connection)
DOMAIN = os.getenv("MAILGUN_DOMAIN")

template_loader = jinja2.FileSystemLoader("templates")
template_env = jinja2.environment(loader=template_loader)


def render_template(template_filename, **context):
    return template_env.get_template(template_filename).render(**context)

def send_simple_message(to, subject, body, html):
    api_key = os.getenv("MAILGUN_API_KEY")
    print("came to simple message")
    return requests.post(
        f"https://api.mailgun.net/v3/{DOMAIN}/messages",
        auth=("api", api_key),
        data={
            "from": f"RamaManohar <mailgun@{DOMAIN}>",
            "to": [to],
            "subject": subject,
            "text": body,
            "html" : html,
        }
    )

def send_user_registration_message(email, username):
    print("came to nested user registration message")
    send_simple_message(
        email,
        "Successfully registered",
        f"Hi {username}, you have successfully signed up to the stores REST API",
        render_template("email/registration.html", username=username),
    )
