from invoke import task
import pychromecast


@task
def list_chromecasts(ctx):
    """List chromecasts on network"""
    print("Finding chromecasts. This might take a while!\n")
    casts = pychromecast.get_chromecasts()
    for cast in casts:
        print(f"[{cast.device.friendly_name}] [{cast.device.uuid}]")


@task
def display_image(ctx, uuid):
    """Display image to chromecasts with uuid uuid"""    
    print("Finding chromecasts. This might take a while!\n")

    casts = pychromecast.get_chromecasts()



    try:
        cast = [cast for cast in casts if cast.device.uuid.__str__() == uuid][0]
    except BaseException as e:
        print(e)

    breakpoint()
