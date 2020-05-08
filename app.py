from flask import Flask, request, redirect, Response
from flask_cors import CORS
import requests

app = Flask(__name__)
cors = CORS(app, resources={r"/i94/*": {"origins": "http://www.sptcalc.com"}})
SITE_NAME = 'http://proxy.sptcalc.com/'

@app.route('/', methods=['GET'])
def index():
    return ('', 204)

@app.route('/i94', methods=['POST'])
def proxy():
    resp = requests.post('https://i94.cbp.dhs.gov/I94/services/app/v1.0/search/adis/history', json=request.get_json())
    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
    headers = [(name, value) for (name, value) in resp.raw.headers.items() if name.lower() not in excluded_headers]
    response = Response(resp.content, resp.status_code, headers)
    return response

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=8000)
