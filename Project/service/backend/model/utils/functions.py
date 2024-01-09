
from model.assets import modelStoreConfig

from pathlib import Path

from common.types import *
from datetime import datetime

from typing import List, Tuple
from pydantic import BaseModel

class BBOX(BaseModel):
    minX: float
    maxX: float
    minY: float
    maxY: float
    width: float
    height: float

###1. IOU => 같은 오브젝트인지 판단하기
async def get_iou(obj1:Object, obj2:Object)->bool:
    bbox1 = await get_bbox(obj1)
    bbox2 = await get_bbox(obj2)

    intersecBbox = await get_intersection(bbox1, bbox2)

    if intersecBbox.width > 0 and intersecBbox.height > 0:
        intersectionArea = intersecBbox.width * intersecBbox.height
        box1Area = bbox1.width * bbox1.height
        box2Area = bbox1.width * bbox2.height
        unionArea = box1Area + box2Area - intersectionArea

        return intersectionArea / unionArea
    else:
        return 0.0 # 겹치지 않으면, 0!
    
async def get_bbox(obj:Object)->BBOX:
    """
    minX, maxX, minY, maxY 반환!
    """
    minX = obj.center[0] - 0.5 * obj.width
    maxX = obj.center[0] + 0.5 * obj.width
    minY = obj.center[1] - 0.5 * obj.height
    maxY = obj.center[1] + 0.5 * obj.height
    width = maxX - minX + 1
    height = maxY - minY + 1

    return {"minX": minX, "maxX": maxX, "minY": minY, "maxY": maxY, "width": width, "height": height}

async def get_intersection(bbox1:BBOX, bbox2:BBOX)-> BBOX:
    minX = max(bbox1.minX, bbox2.minX)
    maxX = min(bbox1.maxX, bbox2.maxX)
    minY = max(bbox1.minY, bbox2.minY)
    maxY = min(bbox1.maxY, bbox2.maxY)

    width = maxX - minX + 1
    height = maxY - minY + 1

    return {"minX": minX, "maxX": maxX, "minY": minY, "maxY": maxY, "width": width, "height": height}


async def is_same(obj1:Object, obj2:Object, thresh = 0.5)->bool:
    if obj1.category == obj2.category and await get_iou(obj1, obj2) > thresh:
            return True
    else:
            return False


async def calculate_risk(objs:List[Object], alpha=0.5)->RiskCategory:
    """
    크기와 접근 정도를 고려하여 위험도를 판단한다.
    크기 : 가장 최근 이미지를 9등분 하여 차지하는 면적이 한칸씩 증가할 떼, 위험도 상승
    점근 정도 : 상대적으로 다가오면 +1, 정지하면 0.5, 멀어지면 0.0(이전 10개의 프레임의 같은 Object를 입력으로 받는다.)
    alpha를 조절해 크기와 접근 정도의 비율을 조정한다.

    최종 Risk는 [0, 1]로 정규화되며 이를 3단계로 구분해 반환한다.
    """

    latestObj = objs[-1]
    size = latestObj.width * latestObj.height

    risk = alpha * size + (1 - alpha) * get_gradient(objs)

    if risk < 1 / 3:
        return RiskCategory.LOW
    elif risk < 2 / 3:
        return RiskCategory.MID
    else:
        return RiskCategory.HIGH

async def get_gradient(objs:List[Object]):
    prvSize = objs[0].width * objs[0].height
    curSize = 0.0
    grad = 0.0
    alpha = 0.5
    for obj in objs[1:]:
        curSize = obj.width * obj.height
        grad = alpha * grad + (1 - alpha) * (curSize - prvSize)

        prvSize = curSize
    
    if grad > 0.01:
        return 1.0
    elif grad < -0.01:
        return 0.0
    else:
        return 0.5
    
async def find_sameObjects(logs:List[Log]) -> List[List[Object]]:
    """
    로그가 저장된 프레임마다 동일한 Object들을 찾아서 시간순으로 정렬한다.(0: 가장 오래된 것, -1: 가장 최신)
    각 로그에 저장된 오브젝트는 model prediction 단계에서 서로 다른 Object라고 판단된 것이다!!
    바로 이전 프레임과 비교하여 같은 물체인지를 판단한다.
    """
    sameObjects:List[List[Object]] = [[obj] for obj in logs[0].objects] # Init

    for log in logs[1:]:
        for currentObj in log.objects:
            isExist = False
            for objList in sameObjects:
                if len(objList) != 0 and await is_same(objList[-1], currentObj):
                    objList.append(currentObj)
                    isExist = True
                    break
            if not isExist:
                sameObjects.append([currentObj]) # 새로운 Object의 등장
    return sameObjects



async def make_log_name(src:str, id:int)->Path:
    return modelStoreConfig['paths']['logs'] / src / (src + '_' + str(id) + '.json')
