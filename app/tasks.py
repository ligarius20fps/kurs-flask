import os
from dotenv import load_dotenv
import requests
import jinja2

load_dotenv()
DOMAIN = os.getenv("MAILGUN_DOMAIN")
template_loader = jinja2.FileSystemLoader("templates")
template_env = jinja2.Environment(loader=template_loader)

def render_template(template_filename, **context):
    return template_env.get_template(template_filename).render(**context)

def send_simple_message(to, subject, body, html):
    return requests.post(
        f"https://api.mailgun.net/v3/{DOMAIN}/messages",
        auth=("api", os.getenv("MAILGUN_API_KEY")),
        data={"from": f"mati <mailgun@{DOMAIN}>",
            "to": [to],
            "subject": subject,
            "text": body,
            "html": html})

def send_registration_message(email, username):
    send_simple_message(
                to=email,
                subject="Successfully signed up",
                body=f"Hello, {username} and welcome to stores REST API",
                html=render_template("email/welcome.html", username=username)
            )