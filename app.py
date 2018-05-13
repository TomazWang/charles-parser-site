import json

import os
from flask import Flask, Response, request, send_from_directory, current_app

from main.dev.chl_parser import charles_parser


ROOT_URL = 'http://127.0.0.1:5000'

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/dev/charles_parser', methods=['POST'])
def route_charles_parser():
    json_dict = request.get_json()

    file_url = json_dict['file_url']
    parse_result = charles_parser.from_url(file_url)
    parse_result.url = '{}/downloads/{}'.format(ROOT_URL, parse_result.file_name)

    json_str = json.dumps(parse_result.__dict__)

    return Response(json_str, mimetype="application/json")


@app.route('/downloads/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    download_dir = charles_parser.DOWNLAOD_DIR
    downdloads = os.path.join(current_app.root_path, download_dir)
    return send_from_directory(directory=downdloads, filename=filename)


if __name__ == '__main__':
    app.run()
