import flask
import glob
import os
import pathlib
import socket
import urllib
from random import shuffle

from flask import request
from loguru import logger
from gevent.pywsgi import WSGIServer

LOG_FILE="/var/log/ccss.log"
logger.add(LOG_FILE, enqueue=True, retention="10 days", backtrace=True)

try:
    IMAGEFOLDER = int(os.environ["CCSS_IMAGEFOLDER"])
except BaseException:
    IMAGEFOLDER = "/opt/ccss_imagefolder"

try:
    PORT = int(os.environ["CCSS_PORT"])
except BaseException:
    PORT = 5000

app = flask.Flask(__name__)


def get_image_urls(folder):
    os.chdir(folder)
    files = glob.glob("**/*", recursive=True)
    files = [
        f for f in files if pathlib.Path(f).suffix.lower() in [".jpg", ".jpeg", ".png"]
    ]
    shuffle(files)

    return [f"/image/{urllib.parse.quote(file)}" for file in files]


@app.route("/")
def base():
    logger.debug(request.remote_addr)
    return flask.render_template("base.html")


@app.route("/status")
def status():
    logger.debug(request.remote_addr)
    resp = flask.jsonify(success=True)
    resp.status_code = 200
    return resp


@app.route("/images")
def images():
    """A json list of files """
    logger.debug(request.remote_addr)
    return flask.jsonify(get_image_urls(IMAGEFOLDER))
    # return flask.jsonify(["/image/IMG_2436.JPG"] * 10)


@app.route("/image/<path:path>")
def image(path):
    logger.debug(request.remote_addr + ":" + path)
    return flask.send_from_directory(IMAGEFOLDER, path)


# Start the server
http_server = WSGIServer(('', PORT), app)
http_server.serve_forever()
