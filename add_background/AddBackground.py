import cv2 as cv 
import numpy as np 
import xml.etree.ElementTree as ET
from coordinates.Coordinates import TCoordinate
from traces.Trace import TTrace
from trace_groups.TraceGroups import TTraceGroup
from pathlib import Path
import os
import gc
import random

class AddBackground:
    def __init__(self, bg_dir, inkml_dir, img_dir, thickness=2):
        # bg_dir: direction to the folder containing the background images
        # inkml_dir: direction to the folder containing the inkml files
        # img_dir: direction to the folder which will contain the addded-background images

        self.bg_dir = Path(bg_dir)
        self.inkml_dir = Path(inkml_dir)
        self.img_dir = img_dir
        
        self.thickness = thickness

    def parsing(self, inkml_file, size):
        tree = ET.parse(inkml_file)
        root = tree.getroot()

        traceGroups = []
        # gathering traceGroup elements
        for traceGroup in root.findall("traceGroup"):
            traceGroups.append(traceGroup)
        
        TraceGroups = []
        for traceGroup in traceGroups:
            traces = []
            for trace in traceGroup.findall("trace"):
                coordinates = TCoordinate(trace.text)
                trace = TTrace(trace.get("id"), coordinates)
                traces.append(trace)
            truth = traceGroup.find("annotationXML").find("Tg_Truth").text
            TraceGroup = TTraceGroup(traceGroup.get("id"), truth, traces, size=size, thickness=self.thickness)
            TraceGroups.append(TraceGroup)
        
        return TraceGroups 

    def stack_backgrounds(self):
        # paper_bg_dir: Path object - direction to folder containing paper backgrounds 

        # file names of these background images
        bg_images = list(self.bg_dir.glob("*.jpg"))
        # file names for inkml files
        inkml_files = list(self.inkml_dir.glob("*.inkml"))
        
        # parsing inkml files
        numbering = 0
        # fix the width and height of the background images
        bg_w = 1024 # pixels
        bg_h = int(1.5 * bg_w)
        num_bg = len(bg_images)
        for inkml_file in inkml_files:
            traceGroups = self.parsing(inkml_file, (int(bg_w*0.6), bg_h))
            for traceGroup in traceGroups:
                # get the image of text 
                txt_img = traceGroup.create_image()
                txt_h, txt_w, _ = txt_img.shape
                # step per 10 pixels 
                steps_y = int(bg_h / txt_h)
                for step_y in range(steps_y):
                    # get the background image 
                    bg_index = random.randint(0, num_bg-1)
                    bg_file_name = bg_images[bg_index]
                    bg_img = cv.imread(str(bg_file_name))
                    bg_img = cv.resize(bg_img, (bg_w, bg_h))
                    # stack the background
                    new_img = bg_img[step_y*txt_h:txt_h + txt_h*step_y, int(bg_w*0.2):txt_w + int(bg_w*0.2), :]
                    new_img = np.where(np.equal(txt_img, np.array(0)), txt_img, new_img)
                    cv.imshow("image", new_img / 255)
                    cv.waitKey(100)
                    # save image
                    numbering += 1
                    img_file = os.path.join(self.img_dir, "{}.png".format(numbering))
                    # cv.imwrite(img_file, new_img)

        return numbering