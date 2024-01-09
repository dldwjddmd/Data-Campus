from .config import *
from .category import *

import json
from dummyData import dummyStoreConfig

import base64
from typing import List, Tuple, Optional, Dict
from pydantic import root_validator, validator, Field, BaseModel
from pydantic.dataclasses import dataclass

from pytz import timezone
from datetime import datetime

"""
datetime이 Json serialize 될 때, bottleneck이 발생한다(5-6 secs)
datetime을 받는 날짜 형식을 str 형식으로 바꾸어 이 현상을 완화한다(1-2 secs)
"""

# @dataclass(config=ObjectConfig)
class Object(BaseModel):
    """
    Detectable Object Model
    All values are relative coordinates nomalized in [0.0, 1.0]
    Probability is the probs of predction
    """
    category: ObjectCategory
    probability: float
    center: Tuple[float, float]
    width : float
    height: float
    risk  : RiskCategory 

    @validator('width', 'height', 'probability', 'center', each_item=True)
    def check_size(cls, v):
        if v < 0.0 or v > 1.0:
            raise ValueError("Unnormalized values")
        else:
            return v

    class Config:
        title = "ObjectSchema"
        dummy = None
        if dummyStoreConfig['paths']['Object'].exists():
            with open(dummyStoreConfig['paths']['Object'], 'r') as fd:
                dummy = json.load(fd)
        schema_extra = {
            "example":   dummy
        }

# @dataclass(config=ImageConfig)
class Image(BaseModel):
    """
    src is the name of video(also unique!) \n
    id is an unique value in each video \n
    title is an unique file name formatted like src_id.jpeg \n
    data is the unnormalized image array
    captured is captured time(time-zone is Asia/Seoul) \n
    Width and Height are the number of pixels \n
    Risked are the highest risked objects \n
    """
    captured: datetime
    width: int
    height: int
    risked: List[Object]

    src: str
    id: int
    data: bytes
    title: Optional[str] = None

    @root_validator(pre = True)
    def set_title(cls, vals):
        src, id = vals.get('src'), vals.get('id')
        vals['title'] = src + '_' + str(id) + '.jpeg'
        return vals

    @validator('captured')
    def check_tz(cls, v:datetime):
        KST = timezone('Asia/Seoul')
        return v.astimezone(KST)

    class Config:
        title = "ImageSchema"
        dummy = None
        if dummyStoreConfig['paths']['Image'].exists():
            with open(dummyStoreConfig['paths']['Image'], 'r') as fd:
                dummy = json.load(fd)
        schema_extra = {
            "example":   dummy
        }

# @dataclass(config=LogConfig)
class Log(BaseModel):
    """
    Src is the associated video \n
    id is an unique value in each video \n
    Recorded is a recorded time \n
    Objects are all tracked objects \n
    Risked are the highest riskable objects's indice \n
    Risk is a total risk of the scene
    """
    src: str 
    id: int
    recorded: datetime
    objects: List[Object]
    risked: List[int]
    risk: RiskCategory

    @validator('recorded')
    def check_tz(cls, v:datetime):
        KST = timezone('Asia/Seoul')
        return v.astimezone(KST)

    class Config:
        title = "LogSchema"
        dummy = None
        if dummyStoreConfig['paths']['Log'].exists():
            with open(dummyStoreConfig['paths']['Log'], 'r') as fd:
                dummy = json.load(fd)
        schema_extra = {
            "example":   dummy
        }

# @dataclass(config=FrameConfig)
class Frame(BaseModel):
    """
    Raw Video Frame Type
    """
    id       : int = Field(..., description="Unique Frame Number")
    captured : datetime = Field(..., description="Captured time")

    @validator('captured')
    def check_tz(cls, v:datetime):
        KST = timezone('Asia/Seoul')
        return v.astimezone(KST)

    class Config:
        title = "FrameSchema"
        dummy = None
        if dummyStoreConfig['paths']['Frame'].exists():
            with open(dummyStoreConfig['paths']['Frame'], 'r') as fd:
                dummy = json.load(fd)
        schema_extra = {
            "example":   dummy
        }

# @dataclass(config=VideoConfig)
class Video(BaseModel):
    """
    Raw Video Annotation Type
    """
    mode       : str = Field(..., description="Image mode like RGB or BGR") 
    title      : str = Field(..., description="video name")
    format     : str = Field(..., description="Image format like jpeg")
    duration   : Dict[str, datetime] = Field(..., description="start and end timestamp")
    
    width      : int = Field(..., description="Frame width")
    height     : int = Field(..., description="Frame height")
    
    frames     : List[Frame] = Field([], description="Video frames")

    @validator('duration')
    def check_duration(cls, v:Dict[str, datetime]):
        if set(v.keys()) != set({'start', 'end'}):
            raise ValueError("duration MUST have only start and end keys")
        
        KST = timezone('Asia/Seoul')
        v['start'] = v['start'].astimezone(KST)
        v['end'] = v['end'].astimezone(KST)

        if v['start'] > v['end']:
            raise ValueError("Start is later than End")

        return v

    class Config:
        title = "VideoConfig"
        dummy = None
        if dummyStoreConfig['paths']['Video'].exists():
            with open(dummyStoreConfig['paths']['Video'], 'r') as fd:
                dummy = json.load(fd)
        schema_extra = {
            "example":   dummy
        }