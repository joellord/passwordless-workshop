from flask import Flask, jsonify, Response
import os
from api_auth_header import AuthError, requires_auth
from flask_cors import CORS
from randopeep import clickbait

app = Flask(__name__)
CORS(app)


@app.errorhandler(AuthError)
def handle_auth_error(ex):
    # response = jsonify(ex.error)
    # response.status_code = ex.status_code
    # return response
    return Response(str(ex.error), ex.status_code, {})

@app.route("/headline")
def headline():
    return clickbait.headline()

@app.route("/protected/headline")
@requires_auth
def protected_headline():
    return clickbait.headline("Joel Lord")


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8888))
    print("Auth server started on port %d " % port)
    app.run(host='0.0.0.0', port=port, debug=True)
