# number, img_path, label_path, save_img_path, save_label_path
import json
import os
import glob
import math

from tqdm import tqdm
from PIL import Image as PILImage

# src는 커스텀 전 데이터의 경로
# dest는 커스텀 후 이동할 데이터의 경로

### PM : 13 ~ 19 -> 오토바이 0
### PM : 20 ~ 27 -> 자전거 1
### PM : 28 ~ 39 -> 킥보드 2

class Custom_dataset(): # 단일 파일 경로를 input으로 받는다.

    '''save_img_path, save_label_path 경로 끝에 '/' 붙여야 함 '''
    
    def __init__(self, number, img_path, label_path, save_img_path, save_label_path): 
        self.number = number
        
        self.img_path = img_path
        self.label_path = label_path
        
        self.img_name = self.img_path.split('\\')[-1].split('.j')[0] # 이미지 파일명 ( 확장자 x )
        self.label_name = self.label_path.split('\\')[-1].split('.j')[0] # json 파일명 ( 확장자 x )
        
        self.save_img_path = save_img_path
        self.save_label_path = save_label_path
        
        self.width = 640 # Yolo v7x가 받는 사이즈로 고정 
        self.height = 640 # Yolo v7x가 받는 사이즈로 고정
                
    # read_json
    def read_json(self):
        if self.img_name == self.label_name:
            converted_annotation = []
            with open (self.label_path, "r") as f:
                data = json.load(f)
                raw_width = float(data['description']['imageWidth'])
                raw_height = float(data['description']['imageHeight'])
                annotation = data['annotations']['PM']
            
            if len(annotation) == 0:
                return None, None, None
            
            elif len(annotation) == 1:
                pmcode = int(annotation[0]['PM_code'])
                bbox = annotation[0]['points']
                
                # convert
                pmcode = self.convert_pmcode(pmcode)
                bbox = self.convert_bbox(bbox, raw_width, raw_height)
                
                converted_annotation.append(pmcode)
                converted_annotation += bbox
                return converted_annotation, pmcode, len(annotation)
            
            elif len(annotation) > 1 :
                for anno in annotation:
                    pmcode = int(anno['PM_code'])
                    bbox = anno['points']
                    # convert
                    pmcode = [self.convert_pmcode(pmcode)]
                    bbox = self.convert_bbox(bbox, raw_width, raw_height)
                    pmcode += bbox # [pmcode, x, y, w,h] 형태의 리스트
                    
                    converted_annotation.append(pmcode)
                return converted_annotation, pmcode[0], len(annotation) # 객체가 몇 개인지의 정보
        else:
            return 0

    def convert_pmcode(self, pmcode):
        if 13 <= pmcode <= 19:
            return 0
        elif 20 <= pmcode <=27:
            return 1
        elif 28 <= pmcode <= 39:
            return 2
        
    def convert_bbox(self, bbox, raw_width, raw_height):
        # 0~1 상대값으로 바꿔야함
        w = bbox[2] / raw_width
        h = bbox[3] / raw_height
        x = (bbox[0] / raw_width) + (w/2) # 좌상단값이 아닌 중앙값
        y = (bbox[1] / raw_height) + (h/2) # 좌상단값이 아닌 중앙값
        
        return [x,y,w,h]
                
    def img_resize(self, save_img_path):
        img = PILImage.open(self.img_path)
        img = img.resize((self.width, self.height), PILImage.BICUBIC)
        img.save(save_img_path)
        return True
                
    def run(self):
        if self.img_name == self.label_name:
            converted_annotation, pmcode, annotation_len = self.read_json()
                
            if pmcode == 0:
                cls = 'motorcycle'
            elif pmcode == 1:
                cls = 'bicycle'
            else:
                cls = 'kickboard'
              
            with open(self.save_label_path + '{}_{}.txt'.format(self.number, cls), "w") as f:
                # 객체가 없을 때
                if annotation_len == 0:
                    print('객체가 없습니다.')
                    return 0
                # 객체가 1개일때  
                elif annotation_len == 1:
                    c = int(converted_annotation[0])
                    x = float(converted_annotation[1])
                    y = float(converted_annotation[2])
                    w = float(converted_annotation[3])
                    h = float(converted_annotation[4])
                    f.write(f'{c} {x} {y} {w} {h}')
                    
                    # resizing 속도를 못 쫒아가서 if문 필요
                    if self.img_resize(self.save_img_path+'{}_{}.jpg'.format(self.number, cls)) == True:
                        print(cls,self.number,'번째 파일 컨버팅 완료되었습니다. 객체 {}개'.format(annotation_len))
                        return 1
                    
           # 객체가 2개 이상일때         
                elif annotation_len > 1: # 객체가 2개 이상일때
                    for row in converted_annotation:
                        c = int(row[0])
                        x = float(row[1])
                        y = float(row[2])
                        w = float(row[3])
                        h = float(row[4])
                        f.write(f'{c} {x} {y} {w} {h}\n')
                    
                    # resizing 속도를 못 쫒아가서 if문 필요
                    if self.img_resize(self.save_img_path+'{}_{}.jpg'.format(self.number, cls)) == True:
                        print(cls,self.number,'번째 파일 컨버팅 완료되었습니다. 객체 {}개'.format(annotation_len))
                        return 1
        else:
            print('이미지 파일과 라벨 파일이 일치하지 않습니다.')
            return 0