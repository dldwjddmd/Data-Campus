from common.types import *
from camera.utils.mycamera import MyCamera
from model.utils.mymodel import MyModel

from typing import Dict

from fastapi import APIRouter, Response, status

router = APIRouter(prefix='/video', tags=['video'])

model = MyModel()
camera = MyCamera()


@router.post('/{title}/start', response_model=Video)
async def start_video(title, response:Response):
    """
    Video 시작! 메모리에 Video를 새롭게 올린다.
    Model이 640 x 640 x 3 이미지로 훈련되어 있기에 해당 크기로 설정한다.
    """
    global model
    global camera

    await camera.start_video(title, 640, 640)

    return camera.video


@router.post('/{title}/end', response_model=Video)
async def end_video(title, savedTitle:str, response:Response):
    global model
    global camera

    if not camera.isConnected:
        response.status_code = status.HTTP_404_NOT_FOUND
        return None

    if title != camera.video.title:
        response.status_code = status.HTTP_404_NOT_FOUND
        return None
    else:
        await camera.end_video(savedTitle)
        return camera.video


@router.post('/{title}/save', response_model=bool)
async def save_frame(title:str, img: Image, response:Response):
    """
    전송된 이미지를 저장한다. 저장하지 못했다면 False를 반환한다.
    """
    global model
    global camera

    if not camera.isConnected:
        response.status_code = status.HTTP_404_NOT_FOUND
        return None

    if camera.video.title != title or img.src != camera.video.title:
        response.status_code = status.HTTP_404_NOT_FOUND
        return None
    else:
        return await camera.save_frame(img)


@router.get('/{title}/streaming', response_model=Image)
async def get_stream(title:str, response:Response):
    """
    사진을 찍어서 보내주기!
    """
    global model
    global camera

    if not camera.isConnected:
        response.status_code = status.HTTP_404_NOT_FOUND
        return None

    if title != camera.video.title:
        response.status_code = status.HTTP_404_NOT_FOUND
        return None
    else:
        img:Image = await camera.capture()
        return img

@router.get('/{title}/{id}', response_model=Image)
async def get_an_image(title:str, id:int, response:Response):
    global model
    global camera

    if not camera.isConnected:
        response.status_code = status.HTTP_404_NOT_FOUND
        return None

    if title != camera.video.title:
        response.status_code = status.HTTP_404_NOT_FOUND
        return None
    else:
        try:
            img:Image = await camera.get_frame(id)
            return img
        except FileNotFoundError:
            response.status_code = status.HTTP_404_NOT_FOUND
            return None