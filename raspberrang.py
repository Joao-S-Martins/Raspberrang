#!/usr/bin/env python3

import datetime as dt
from gpiozero import LED, Button
import io
import logging
import picamera
from signal import pause
import subprocess
from time import sleep
from utils.loggerinitializer import *

initialize_logger('./logs')
logging.info('Logging initialized')

camera = picamera.PiCamera()
camera.rotation = 180
# camera.led = False
stream = None
trigger = False

led = LED(13)
btn = Button(23)
# 18 rx
# 24 tx

def snapshot():
    # TODO (joao) Take & save a snapshot
    camera.start_preview(alpha=128)
    sleep(5)
    camera.capture('./pics/test_image.jpg')
    camera.stop_preview()
    return

def write_stream():
    logging.info('Writing video')
    # with stream.lock:
    camera.stop_recording()
    # Find the first header frame in the video
    for frame in stream.frames:
        if frame.header:
            stream.seek(frame.position)
            break
    # Write the rest of the stream to disk
    file_name = './vids/%s.h264' % get_timestamp()
    with io.open(file_name, 'wb') as output:
        output.write(stream.read())
        logging.info('%s written' % file_name)
    start_stream()
        
def start_stream():
    logging.info('Starting stream')
    global stream
    global trigger
    stream = picamera.PiCameraCircularIO(camera, seconds=2)
    camera.start_recording(stream, format='h264')
    logging.info("Stream started")
    try:
        while True:
            logging.info("trigger is %s" % trigger)
            camera.wait_recording(1)
            if btn.is_pressed:
                logging.info("trigger was true")
                trigger = False
                # Keep recording for 1 second and only then write the
                # stream to disk
                camera.wait_recording(1)
                write_stream()
    finally:
        camera.stop_recording()

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

def get_timestamp():
    n = dt.datetime.now()
    return '%d-%d-%d-%d:%d:%d' % (n.year, n.month, n.day, n.hour, n.minute, n.second)

def listen():
    # TODO (joao) Listen for signal and interpret
    return

def btn_change():
    logging.info("btn change")

def triggered():
    btn.is_pressed()

def on_btn_press():
    logging.info("btn pressed")
    global trigger
    trigger = True # This will cause the video to save and stop

logging.info("Raspberang started")
start_stream()

# btn.when_pressed = on_btn_press
# btn.when_released = btn_change

led.blink()

pause()
