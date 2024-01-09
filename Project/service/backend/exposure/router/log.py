from fastapi import APIRouter, Response, status
from datetime import datetime

from common.types import *
from model.utils.mymodel import MyModel

from camera.utils.mycamera import MyCamera

model = MyModel()
camera = MyCamera()

router = APIRouter(prefix='/log', tags=['log'],)

@router.post('/{title}/start', response_model = Log)
async def start_log(title, response:Response):
    """
    Start Log id는 현재 Video의 가장 최신 Frame id이다.
    Log는 지금부터 찍히는 것이므로!
    """
    global model
    global camera

    if title != camera.video.title:
        response.status_code = status.HTTP_404_NOT_FOUND
        return None
    else:
        log = await model.start_log(title)
        log.id = camera.video.frames[-1].id if len(camera.video.frames) > 0 else 0
        return log

@router.post('/{title}/end', response_model=Log)
async def end_log(title, savedTitle:str, response:Response):
    """
    지금까지 기록된 Log를 저장하고, Dummy Log를 반환한다.
    """
    global model
    global camera

    if not model.isConnected:
        response.status_code = status.HTTP_404_NOT_FOUND
        return None     

    if title != model.logSrc:
        response.status_code = status.HTTP_404_NOT_FOUND
        return None
    else:
        await model.end_log(title, savedTitle)
        return Log(src=savedTitle, id = -1, recorded=datetime.now(), objects=[], risked=[], risk=RiskCategory.LOW)

@router.post('/{title}/save', response_model=None)
async def save_log(title, response:Response):
    """
    Memory 상에 해당 Source의 Log가 없다면, 404 Error를 반환한다.
    """
    global model
    global camera

    if not model.isConnected:
        response.status_code = status.HTTP_404_NOT_FOUND
        return None     

    if not await model.save_log(title):
        response.status_code = status.HTTP_404_NOT_FOUND
    return None

@router.post('/{title}/prediction', response_model=Log)
async def predict(title:str, img:Image, response:Response):
    """
    수신된 Image에 대해 Prediction 수행
    """
    global model
    global camera

    if not model.isConnected:
        response.status_code = status.HTTP_404_NOT_FOUND
        return None     

    if title != model.logSrc:
        response.status_code = status.HTTP_404_NOT_FOUND
        return None
    else:
        # print("Enter\n\n\n\n\n\n\n\n\n\n")
        log:Log = await model.write(img)
        # print("ENd\n\n\n\n\n\n\n\n\n\n")
        return log

@router.get('/{title}/{id}', response_model=Log)
async def get_an_log(title:str, id:int, response:Response):
    global model
    global camera

    if not model.isConnected:
        response.status_code = status.HTTP_404_NOT_FOUND
        return None     

    if title != model.logSrc:
        response.status_code = status.HTTP_404_NOT_FOUND
        return None
    else:
        try:
            log = await model.get_log(title, id)
            return log
        except FileNotFoundError:
            response.status_code = status.HTTP_404_NOT_FOUND
            return None 