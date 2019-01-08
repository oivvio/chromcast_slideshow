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

CCSS_PORT = 5000

LOG_FILE="/var/log/ccss.log"

logger.add(LOG_FILE, enqueue=True, retention="10 days", backtrace=True)

logger.add(sys.stderr)

def write_pidfile(filename):
    pid = str(os.getpid())
    f = open(filename, 'w')
    f.write(pid)
    f.close()


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
    if len(casts) == 0:
        logger.debug(f"get_chromecasts returned nothing")

    for cast in casts:
        logger.debug(
            f"Cast listing: '{cast.device.friendly_name}' '{cast.device.uuid.__str__()}'"
        )
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
    APP_ID_DASHCAST = "84912283"

    PID_FILE="/tmp/ccss_slideshow.pid"
    write_pidfile(PID_FILE)
    while True:
        try:
            # Get a handle on the chromecast
            cast = _get_cast(uuid_or_name)

            if cast:
                cast.wait()

                logger.debug(f"Found '{uuid_or_name}'")

                while True:

                    # Check if the ChromeCast is alive at all
                    if _host_up(cast.host):
                        logger.debug(f"'{uuid_or_name}' is up")

                        # Check if the ChromeCast is running the
                        # default Backdrop app
                        if cast.status.app_id == APP_ID_BACKDROP:
                            logger.debug(
                                f"'{uuid_or_name}' is running Backdrop.  Try to start slide show."
                            )

                            # Get our ip
                            IP = _get_my_local_ip()

                            # Start casting our slideshow
                            dcc = DashCastController()
                            cast.register_handler(dcc)
                            dcc.load_url(f"http://{IP}:{CCSS_PORT}")
                        elif cast.status.app_id == APP_ID_DASHCAST:
                            logger.debug(
                                f"'{uuid_or_name}' is already running Dashcast."
                            )
                        else:
                            logger.debug(
                                f"'{uuid_or_name}' is running {cast.status.display_name}"
                            )
                    else:
                        logger.debug(f"'{uuid_or_name}' does not respond to ping")
                    # Hang back
                    time.sleep(5)

        except BaseException as e:
            raise e
        # Hang back
        time.sleep(5)

@task
def flask(ctx, pty=True, port=CCSS_PORT):
    """Start the application that serves the slideshow """
    cmd = f"CCSS_PORT={port} python app.py"
    ctx.run(cmd, pty=pty)
    
    
@task
def build_js(ctx, pty=True):

    cmd = "./node_modules/.bin/tsc -w  --project tsconfig.json"
    ctx.run(cmd, pty=pty)
