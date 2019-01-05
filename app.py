import flask
import glob
import os
import pathlib
import socket
import urllib

IMAGEFOLDER="/home/oivvio/Dropbox/familjen/bildspel/"
PORT=5000

app = flask.Flask(__name__)

# def get_my_local_ip():
#     s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     s.connect(("8.8.8.8", 80))
#     result = s.getsockname()[0]
#     s.close()
#     return result



def get_image_urls(folder):
    os.chdir(folder)
    files =  glob.glob('**/*', recursive=True)
    files = [f for f in files if pathlib.Path(f).suffix.lower() in [".jpg", ".jpeg"]]
    
    return [f"/image/{urllib.parse.quote(file)}" for file in files]


@app.route("/")
def base():
    return  flask.render_template("base.html")



@app.route("/images")
def images():
    """A json list of files """
    return flask.jsonify(get_image_urls(IMAGEFOLDER))

@app.route("/image/<path:path>")
def image(path):
    return flask.send_from_directory(IMAGEFOLDER, path)
