# Modified by smartbuilds.io
# Date: 27.09.20
# Desc: This web application serves a motion JPEG stream
# main.py
# import the necessary packages
from pydantic import BaseModel
import os
import math
import time
import threading
from multiprocessing import Process, Queue
from timeit import default_timer as timer
from fastapi import FastAPI, Request
from typing import List, Optional
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

from camera import VideoCamera
from dotenv import load_dotenv

load_dotenv()


class StatusType(BaseModel):
    status: bool


class ImagesType(BaseModel):
    images: List[str] = []


origins = [
    "http://localhost",
    "http://localhost:8080",
]


capture_rate = int(os.getenv('CAPTURE_RATE', 60))
basePath = os.getenv('CAPTURE_DIR', 'recording')

lock = threading.Lock()

# App Globals (do not edit)
app = FastAPI(docs_url=None, redoc_url=None)
api = FastAPI(title="Sol de Noche", version='0.0.1')
api.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


templates = Jinja2Templates(directory="dist")

camera = VideoCamera(flip=False)  # flip pi camera if upside down.

recording = False

t = None


def rec_walk(dir):
    files = []
    contents = os.listdir(dir)
    for item in contents:
        if os.path.isdir(dir+'/'+item):
            files.extend(rec_walk(dir+'/'+item))
        else:
            files.append(dir+'/'+item)
    return files


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
    global camera, recording
    print('Start stream ' + str(recording))
    while True:
        if recording:
            print('Should write a frame in %0.03ds' % capture_rate)
            dirPath = basePath+"/"+time.strftime("%Y-%m-%d")

            if not os.path.isdir(dirPath):
                print('The directory is not present. Creating a new one..')
                os.mkdir(dirPath)
            with lock:
                mr = open(dirPath+'/'+time.strftime("%H-%M")+".jpg", 'wb+')
                mr.write(camera.get_frame())
                mr.close()
            time.sleep(capture_rate)


@api.get("/status",)
async def status():
    global recording
    return recording


@api.post("/status",)
async def status(status: StatusType):
    global recording
    recording = status.status
    return recording


@api.get("/images", response_model=ImagesType)
async def images():
    response = ImagesType(images=rec_walk(basePath))

    return response

app.mount("/api", api)

# Static files configuration
app.mount("/css", StaticFiles(directory="dist/css"), name="static")
app.mount("/img", StaticFiles(directory="dist/img"), name="static")
app.mount("/js", StaticFiles(directory="dist/js"), name="static")
app.mount("/fonts", StaticFiles(directory="dist/fonts"), name="static")
app.mount("/recording", StaticFiles(directory=basePath), name="static")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get('/video_feed')
async def video_feed():
    return StreamingResponse(generate(), media_type="multipart/x-mixed-replace;boundary=frame")


@app.on_event("startup")
async def startup_event():
    print('Do nothing')
    t = threading.Thread(target=start_stream, )
    t.start()


@app.on_event("shutdown")
async def shutdown_event():
    print('Do nothing')
    t.stop()
