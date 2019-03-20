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

#users should have the format {id, username, password, email}
users = [
]

magic_links = {}

@app.route("/authorize", methods=["POST"])
def authorize():
    content = request.json

    # Validate the request


    # Find the user in the DB


    # Get the callback


    # Create the magic link


    # Add to Magic Link "DB"


    # Expire links


    # Send the email


    return "OK"


@app.route("/login/<magic_link>", methods=["GET"])
def login(magic_link):
    # Find the matching user and callback


    # Destroy magic link (single use)


    # Create a JWT


    # Redirect User

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
