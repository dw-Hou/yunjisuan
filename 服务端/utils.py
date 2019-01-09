#!/usr/bin/env python
#-*- encoding:utf-8


import cv2
from dic import color_dictionary
#  from matplotlib import patches

def rectangle_detect_image(img,res,path):
    for d in res:
        position = d[2]
        name=d[0]
        print(name)
        name=name.decode("utf-8")
        print(name)
        width = position[2]
        height = position[3]
        center_x = position[0]
        center_y = position[1]
        x1 = round(center_x - width/2)
        y1=round(center_y+height/2)
        x2=round(center_x+width/2)
        y2=round(center_y-height/2)
        bottom_left_y = center_y - (height/2)
        #  rect = patches.Rectangle((bottom_left_x, bottom_left_y), width, height, lingwidth=1, edgecolor='r', facecolor='none')
        if(name in color_dictionary):
            color=color_dictionary[name]
            cv2.rectangle(img,(x1,y1),(x2,y2),color,3)
        else:
            cv2.rectangle(img,(x1, y1),(x2, y2),(255,0,0),3)
        cv2.putText(img,str(name),(x1,y2),cv2.FONT_HERSHEY_COMPLEX_SMALL,1.0,(0,191,255))
    print("ok")  
    cv2.imwrite(path,img)
