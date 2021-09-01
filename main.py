# Modified by smartbuilds.io
# Date: 27.09.20
# Desc: This web application serves a motion JPEG stream
# main.py
# import the necessary packages
import os
import math
import time
import threading
from multiprocessing import Process, Queue
from timeit import default_timer as timer
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.responses import Response
from camera import VideoCamera
from dotenv import load_dotenv

load_dotenv()

capture_rate = os.getenv('CAPTURE_RATE', 3)

lock = threading.Lock()

# App Globals (do not edit)
app = FastAPI(docs_url=None, redoc_url=None)

templates = Jinja2Templates(directory="templates")

camera = VideoCamera(flip=False)  # flip pi camera if upside down.

t = None


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get('/video_feed')
async def video_feed():
    return StreamingResponse(generate(), media_type="multipart/x-mixed-replace;boundary=frame")


def generate():
    global camera, lock
    # loop over frames from the output stream
    while True:
        # wait until the lock is acquired
        with lock:
            frame = camera.get_frame()
        # yield the output frame in the byte format
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
               bytearray(frame) + b'\r\n')


def start_stream():
    global camera
    print('Start stream')

    capture_start = timer()
    while True:
        capture_end = int(math.floor(timer() - capture_start))
        if capture_end >= capture_rate:
            print('Should write a frame %0.03f' % capture_end)
            dirPath = 'templates/'+time.strftime("%Y-%m-%d")

            if not os.path.isdir(dirPath):
                print('The directory is not present. Creating a new one..')
                os.mkdir(dirPath)
            with lock:
                mr = open(dirPath+'/'+time.strftime("%H-%M-%S")+".jpg", 'wb+')
                mr.write(camera.get_frame())
                mr.close()
            capture_start = timer()


@app.on_event("startup")
async def startup_event():
    t = threading.Thread(target=start_stream, )
    t.start()
    #p = Process(target=start_stream)
    # p.start()


@app.on_event("shutdown")
def shutdown_event():
    t.stop()
