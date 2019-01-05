import http.server
import os
import socketserver
import socket
import glob
import threading
import time
import urllib
from flask import Flask

from invoke import task
import pychromecast
from pychromecast.controllers.dashcast import DashCastController


def _get_my_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    result = s.getsockname()[0]
    s.close()
    return result

def _get_cast(uuid):
    print("Finding chromecasts. This might take a while!\n")
    
    casts = pychromecast.get_chromecasts()

    try:
        cast = [cast for cast in casts if cast.device.uuid.__str__() == uuid][0]
    except BaseException as e:
        cast = None
        print(e)

    return cast
    
    
@task
def list_chromecasts(ctx):
    """List chromecasts on network"""
    print("Finding chromecasts. This might take a while!\n")
    casts = pychromecast.get_chromecasts()
    for cast in casts:
        print(f"[{cast.device.friendly_name}] [{cast.device.uuid}]")


@task
def slideshow(ctx, folder, uuid):
    # Move to the folder with the images
    os.chdir(folder)
    
    # Get our current ip
    ip = _get_my_local_ip()

    # Get all the files (that are jpg)
    files = glob.glob('**/*.jpg', recursive=True)

    # Get an handle on the chromecast 
    cast = _get_cast(uuid)
    cast.wait()
    media_controller = cast.media_controller

    # Start up a webserver
    Handler = http.server.SimpleHTTPRequestHandler

    with socketserver.TCPServer((ip, 0), Handler) as httpd:
        port = httpd.socket.getsockname()[1]
        print(f"serving at http://{ip}:{port}")
        urls = [f"http://{ip}:{port}/{file}" for file in files]
        
        threading.Thread(target=httpd.serve_forever).start()

        while True:
            for url in urls:
                print(url)                
                media_controller.play_media(url, 'image/jpeg')
                time.sleep(10)


@task
def loadslideshow(ctx, uuid):
    # Move to the folder with the images
    # Get our current ip
    ip = _get_my_local_ip()

    # Get a handle on the chromecast 
    cast = _get_cast(uuid)
    cast.wait()

    dcc = DashCastController()
    cast.register_handler(dcc)

    dcc.load_url(f"http://{ip}:5000")
    breakpoint()


                
@task
def build_js(ctx, pty=True):

    cmd = "./node_modules/.bin/tsc -w  --project tsconfig.json"
    ctx.run(cmd, pty=pty)

        
