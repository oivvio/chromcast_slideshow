import os
import socket
import glob
import subprocess
import sys
import time

from invoke import task
from loguru import logger
from pychromecast.controllers.dashcast import DashCastController

import pychromecast


logger.add("/var/log/ccss.log")
logger.add(sys.stderr)


def _get_my_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    result = s.getsockname()[0]
    s.close()
    return result


def _get_cast(uuid_or_name):
    msg = "Finding chromecasts. This might take a while!\n"
    logger.debug(msg)

    casts = pychromecast.get_chromecasts()

    try:
        cast = [
            cast
            for cast in casts
            if uuid_or_name in [cast.device.uuid.__str__(), cast.device.friendly_name]
        ][0]
    except BaseException as e:
        cast = None
        logger.debug(e)

    return cast


def _host_up(host):
    """
    Returns True if host (str) responds to a ping request.
    Remember that a host may not respond to a ping (ICMP) request even if the host name is valid.
    """
    # Building the command. Ex: "ping -c 1 google.com"
    command = ["ping", "-c", "1", host]

    # Pinging
    return subprocess.call(command, stdout=open(os.devnull, "wb")) == 0


@task
def list_chromecasts(ctx):
    """List chromecasts on network"""
    logger.debug("Finding chromecasts. This might take a while!")
    casts = pychromecast.get_chromecasts()
    for cast in casts:
        logger.debug(f"[{cast.device.friendly_name}] [{cast.device.uuid}]")


@task
def runslideshow(ctx, uuid_or_name):
    APP_ID_BACKDROP = "E8C28D3C"

    while True:
        try:
            # Get a handle on the chromecast
            cast = _get_cast(uuid_or_name)
            # TODO this might return None
            cast.wait()

            logger.debug(f"Found {uuid_or_name}")

            while True:

                # Check if the ChromeCast is alive at all
                if _host_up(cast.host):
                    logger.debug(f"{uuid_or_name} is up")

                    # Check if the ChromeCast is running the
                    # default Backdrop app
                    if cast.status.app_id == APP_ID_BACKDROP:
                        logger.debug(f"Takeover")

                        # Get our ip
                        IP = _get_my_local_ip()

                        # Start casting our slideshow
                        dcc = DashCastController()
                        cast.register_handler(dcc)
                        dcc.load_url(f"http://{IP}:5000")
                # Hang back
                time.sleep(1)

        except BaseException as e:
            raise e
        # Hang back
        time.sleep(1)


@task
def build_js(ctx, pty=True):

    cmd = "./node_modules/.bin/tsc -w  --project tsconfig.json"
    ctx.run(cmd, pty=pty)
