from .category import *

from pytz import timezone
from datetime import datetime


class ObjectConfig:
    title = "ObjectSchema"
    schema_extra = {
        "example":
            {
                'category'    : 'bicycle, motorcycle, kickboard',
                'probability' : 0.5, 
                'center'      : ['x', 'y'],
                'width'       : '[0.0, 1.0]',
                'height'      :  '[0.0, 1.0',
                'risk'        :  '0: low, 1: mid, 2: high'
            },
    }


class ImageConfig:
    title = "ImageSchema"
    schema_extra = {
        "example":
            {
                'src'      : 'record001',
                'id'       : '1',
                'title'    : 'record001_1.jpeg',
                'captured' : datetime.now(timezone('Asia/Seoul')),
                'width'    : 640,
                'height'   : 640,
                'risked'   : ['object1', 'object2'],
                "data"     : "3-channel Image Array [0 - 255] channel values",

            },
    }

class LogConfig:
    title = "LogSchema"
    schema_extra = {
        "example": 
            {
                "recorded": datetime.now(timezone('Asia/Seoul')),
                "objects" : ['object1(risk = 2)', 'object2(risk = 1)', 'object3(risk = 2)'],
                "risked"  : [0, 2],
                "risk"    : "The highest risk in the scene" 
            },
    }

class FrameConfig:
    title = "FrameSchema"
    schema_extra = {
        "example":
            {
                "id" : 0,
                "captured": datetime.now(timezone('Asia/Seoul')),
            }
    }

class VideoConfig:
    title = "VideoConfig"
    schema_extra = {
        "example":
            {
                "mode"  : "RGB",
                "title" : "default",
                "duration" : "{start: start-time, end: end-time}",
                "width" : 320,
                "height": 320,
                "frames": "['frame1', 'frame2', ...]"
            }
    }