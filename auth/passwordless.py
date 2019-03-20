from flask import Flask, request, abort, redirect
from flask_cors import CORS
from threading import Timer
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jose import jwt
import smtplib
import uuid
import credentials
import os

app = Flask(__name__)
CORS(app)

port = int(os.environ.get('PORT', 8080))

users = [
    {"id": 1, "username": "joellord", "password": "joellord", "email": "joel.lord@auth0.com"},
    {"id": 2, "username": "guest", "password": "guest", "email": "guest@example.com"},
    {"id": 3, "username": "joellord2", "password": "password", "email": "joelphy@gmail.com"}
]

magic_links = {}

@app.route("/authorize", methods=["POST"])
def authorize():
    content = request.json

    # Validate the request
    if not content["email"]:
        abort(400)

    # Find the user in the DB
    user = next(user for user in users if user["email"] == content["email"])
    if not user:
        print("User not found, but let's not tell the user")
        abort(200)

    # Get the callback
    callback = content["callback"]

    # Create the magic link
    magic_link = str(uuid.uuid4())

    # Add to Magic Link "DB"
    magic_links[magic_link] = {"user": user, "callback": callback}

    # Expire links
    Timer(30, detroy_magic_link, [magic_link]).start()

    # Send the email
    server = smtplib.SMTP_SSL(credentials.SMTP_SERVER, credentials.SMTP_PORT)
    server.login(credentials.EMAIL_ADDRESS, credentials.EMAIL_PASSWORD)

    msg = MIMEMultipart()
    msg["From"] = credentials.EMAIL_ADDRESS
    msg["To"] = user["email"]
    msg["Subject"] = "Your magic link"

    msg.attach(MIMEText("🧙‍️ http://localhost:%d/login/%s" % (port, magic_link)))

    server.send_message(msg)

    print("Magic link is on its way!")
    print(magic_links)
    return "OK"


@app.route("/login/<magic_link>", methods=["GET"])
def login(magic_link):
    # Find the matching user and callback
    try:
        data = magic_links[magic_link]

    except KeyError:
        abort(401)

    # Destroy magic link (single use)
    detroy_magic_link(magic_link)

    # Create a JWT
    token = jwt.encode({
        "sub": str(data["user"]["id"]),
        "email": data["user"]["email"],
        "aud": "my-random-clickbait-api",
        "iss": "my-small-auth-server"
    }, "my-super-secret-key", algorithm="HS256")

    # Redirect User
    redirect_url = data["callback"] + "/#access_token=" + token
    return redirect(redirect_url, 302)


def detroy_magic_link(link):
    try:
        del magic_links[link]

    except KeyError:
        print("Key was already deleted, user had logged in.")

    return True


if __name__ == '__main__':
    print("Auth server started on port %d " % port)
    app.run(host='0.0.0.0', port=port, debug=True)
