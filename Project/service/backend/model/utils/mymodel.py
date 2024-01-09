from common.types import *
from common.utils import *
from model.assets import modelStoreConfig

from YOLOv5n.models.common import DetectMultiBackend
from YOLOv5n.utils.general import non_max_suppression, xyxy2xywh


from .functions import *

import os
import json
import shutil
import subprocess
from datetime import datetime

import base64

import torch
import numpy as np



class MyModel(metaclass=Singleton):
    """
    YOLOv5n 사용!
    """
    def __init__(self, maxRecord=10):
        """
        maxRecord : 몇 개의 Log를 메모리에 기억하고, 사용할 것인지!
        """
        self._logs:List[Log] = []
        self.maxRecord = maxRecord
        self._isConnected = False

        # print("\n\n\n\n\n\n\n",modelStoreConfig['data'] )
        self._device = torch.device("cpu")

        self._model = DetectMultiBackend(modelStoreConfig['weights']['best'], device=self._device, \
            dnn=False, data=modelStoreConfig['data'])
        # torch.save(model, '../yolov5_bear-team/our_last_model.pt')
        # self._model = torch.load(modelStoreConfig['weights']['best'],map_location=self._device, )
        self._model.eval()

    @property
    def logs(self):
        return self._logs

    @property
    def logSrc(self):
        if len(self.logs) == 0:
            return ""
        else:
            return self.logs[0].src

    @property
    def isConnected(self):
        return self._isConnected

    async def add_log(self, log:Log)->None:
        """
        Log가 한계까지 쌓이면 디스크에 저장하고, 가장 오래된 로그를 삭제한다.
        Memory 상에 있는 Log는 항상 같은 Src Video이다!!
        """
        
        if len(self.logs) != 0:
            if self.logs[0].src != log.src:
                await self.save_log(self.logs[0].src, removed=True)
            else:
                await self.save_log(self.logs[0], removed=False)

        if len(self.logs) == self.maxRecord:
            self.logs.pop(0)
        
        self.logs.append(log)
        return None

    async def start_log(self, title) -> Log:
        log = Log(src=title, id = 0, recorded=datetime.now(), objects=[], risked=[], risk=RiskCategory.LOW)
    
        if (modelStoreConfig["paths"]['logs'] / title).exists():
            shutil.rmtree(modelStoreConfig['paths']['logs'] / title)
        os.makedirs(modelStoreConfig['paths']['logs'] / title, exist_ok=True)
        
        await self.add_log(log)

        self._isConnected = True
        return log

    async def end_log(self, src:str, savedSrc:str) -> None:
        """
        메모리에 있는 Log들을 모두 저장하고, 메모리를 비운다.
        이후, log의 src를 savedSrc로 바꾼다.
        """
        await self.save_log(src, removed=True)
        subprocess.run(['mv', modelStoreConfig['paths']['logs'] / src, modelStoreConfig['paths']['logs'] / savedSrc])
        
        self._isConnected = False
        return None

    async def save_log(self, src:str, removed=False) -> bool:
        """
        메모리에 있는 Log를 모두 저장한다.
        removed=True라면 Memory를 비운다.
        만약 현재 Log의 src가 지정된 src가 아니라면 False를 반환한다.
        """

        for log in self.logs:
            name = await make_log_name(log.src, log.id)
            with open(name, 'w') as fd:
                fd.write(log.json())

        if removed:
            self._logs = []
        
        if len(self.logs) != 0 and self.logs[0].src != src:
            return False
        else:
            return True


    async def write(self, img:Image)-> Log:
        """
        Model을 돌려 Log를 기록하고 반환하기
        RGBA -> RGB Channel로 변경하여 Model에 넣는다.
        id는 Image의 Id와 동일하다.
        Log를 돌려받으면 호출한 쪽에서 Image에 위험한 Object들을 넣고, Log와 Image를 함께 Client에 준다.
        Image의 Risk를 사용하지 않는다. 어차피 로그랑 중복!
        """
        
        data = np.frombuffer(base64.b64decode(img.data), dtype=np.uint8).reshape(img.width, img.height, -1)[..., :3]
        objList:List[Object] = await self._run(data)
        # print("\n\n\n\n\n\n\n", objList, "\n\n\n\n\n\n\n")
        log = Log(src=img.src, id=img.id, recorded=img.captured, objects=objList, risked=[], risk=RiskCategory.LOW)

        await self.add_log(log)
        sameObjects: List[List[Object]] = await find_sameObjects(self.logs)

        highest:RiskCategory = RiskCategory.LOW
        for objects in sameObjects:
            """
            마지막 Object가 가장 최신 프레임!
            """
            risk = calculate_risk(objects)
            objects[-1].risk = risk

            if highest < risk:
                highest = risk
        
        log.risk = highest
        for idx, obj in enumerate(log.objects):
            if obj.risk == log.risk:
                log.risked.append(idx)

        return log

    @torch.no_grad()
    async def _run(self, img:np.ndarray):
        """
        Return [category, props, center_x, center_y, w, h]
        상대좌표!
        Image : [640, 640, 3]
        한장씩 처리한다.
        """
        
        maxDet = 500
        classes = None
        confThreshold = 0.25
        iouThreshold = 0.5
        agnosticNMS = False

        img = np.transpose(img, [2, 0, 1]) # WHC -> CWH
        img = np.ascontiguousarray(img)
        img = torch.from_numpy(img).to(torch.float32).to(self._device)
        img /= 255.0

        img = img[None] # Bach 차원 추가하기
        
        pred = self._model(img)
        pred = non_max_suppression(pred, confThreshold, iouThreshold, classes, agnosticNMS, max_det=maxDet)[0]
        # print("\n\n\n\n\n\n\n", pred, "\n\n\n\n\n\n")
        gn = torch.tensor(img.shape)[[1, 0, 1, 0]] # Normalize whwh

        inferences:List[Object] = []
        for *xyxy, prob, predCategory in reversed(pred):
            xywh = (xyxy2xywh(torch.tensor(xyxy).view(1, 4)) / gn).view(-1)  # normalized xywh
            
            objCategory:ObjectCategory = ObjectCategory.BICYCLE # Default
            for category in ObjectCategory:
                if int(category) == int(predCategory):
                    objCategory = category
                    break
            
            object = Object(category=objCategory, probability=float(prob), center=xywh[:2], width=xywh[2], height=xywh[3], risk=RiskCategory.LOW)

            inferences.append(object)
        return inferences

    async def get_log(self, src:str, id: int) -> Log:
        """
        1. Memory에 있는 Log인지 확인한다.
        2. Memory에 없다면, 저장된 로그를 불러온다.
           2-1. 불러온 로그를 메모리에 저장하고, src를 검사한다.
        """
        for log in self.logs:
            if log.src == src and log.id == id:
                return log
            else:
                continue
        
        logPath = await make_log_name(src, id)
        if not logPath.exists():
            raise FileNotFoundError
        else:
            with open(logPath, 'r') as fd:
                log = Log(**json.load(fd))
                await self.add_log(log)
                return log

    