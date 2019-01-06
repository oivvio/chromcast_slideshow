import flask
import glob
import os
import pathlib
import socket
import urllib

from flask import request
from loguru import logger

logger.add("/var/log/ccss.log")

IMAGEFOLDER = "/home/oivvio/Dropbox/familjen/bildspel/"
PORT = 5000

app = flask.Flask(__name__)


def get_image_urls(folder):
    os.chdir(folder)
    files = glob.glob("**/*", recursive=True)
    files = [
        f for f in files if pathlib.Path(f).suffix.lower() in [".jpg", ".jpeg", ".png"]
    ]

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


@app.route("/image/<path:path>")
def image(path):
    logger.debug(request.remote_addr + ":" + path)
    return flask.send_from_directory(IMAGEFOLDER, path)
