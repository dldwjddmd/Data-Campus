from common.types import *
from camera.assets import cameraStoreConfig

import io
import base64
import numpy as np
from pathlib import Path
from PIL import Image as PILImage

async def make_frame_name(video:Video, frame_id:int)->Path:
    return str(cameraStoreConfig['paths']['frames'] / video.title / (video.title + "_" + str(frame_id)))


async def make_bytes_from_img(img:PILImage): 
    bytesImg = np.array(img, dtype=np.uint8).tobytes()
    bytesImg = base64.b64encode(bytesImg)

    return bytesImg


async def make_img_from_bytes(bytesImg: bytes, width:int, height: int):
    bytesImg = base64.b64decode(bytesImg)
    imgArr = np.frombuffer(bytesImg, dtype=np.uint8).reshape(width, height, -1)
    img = PILImage.fromarray(imgArr)
    return img
