from gpiozero import LED, Button
import logging
from picamera import PiCamera
from signal import pause
import subprocess
from time import sleep

camera = PiCamera()
camera.rotation = 180

led = LED(13)
btn = Button(23)
# 18 rx
# 24 tx

'''
btn.when_pressed = led.on
btn.when_released = led.off
'''

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
     
# create console handler and set level to info
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

def snapshot():
    # TODO (joao) Take & save a snapshot
    camera.start_preview(alpha=128)
    sleep(5)
    camera.capture('./pics/test_image.jpg')
    camera.stop_preview()
    return

def record(sec=2):
    # TODO (joao) Record & save a video clip
    camera.start_preview()
    camera.start_recording('./vids/test_video.h264')
    sleep(sec)
    camera.stop_recording()
    camera.stop_preview()
    return

def get_name(suffix=''):
    # TODO (joao) return working filename with suffix appended
    # maybe this shoukd be a generator so the same timestamp gets used repeatedly
    return '' # Return timestamp_suffix with the timestamp being the same during thebwhoke cycle

def reverse_vid(path):
    # TODO (joao) Save a reversed copy of the video. Maybe use ffmpeg.
    return

def concat_vid(vids=[]):
    # TODO (joao) concat vids in the order given and save it
    return

def upload(path, msg=''):
    # TODO (joao) Post to Instagram or Twitter or upload to cloud
    return

def listen():
    # TODO (joao) Listen for signal and interpret
    return

logging.info("started")

def btn_change():
    logging.info("btn change")

btn.when_pressed = record
btn.when_released = btn_change

led.blink()

pause()
