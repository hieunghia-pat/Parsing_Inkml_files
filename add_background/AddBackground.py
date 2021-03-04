import cv2 as cv 
import numpy as np 
import pandas as pd
import xml.etree.ElementTree as ET
from coordinates.Coordinates import TCoordinate
from traces.Trace import TTrace
from trace_groups.TraceGroups import TTraceGroup
from pathlib import Path
import os
from random import randint

class AddBackground:
    def __init__(self, bg_dir, inkml_dir, img_dir):
        # bg_dir: direction to the folder containing the background images
        # inkml_dir: direction to the folder containing the inkml files
        # img_dir: direction to the folder which will contain the addded-background images

        self.bg_dir = Path(bg_dir)
        self.inkml_dir = Path(inkml_dir)
        self.img_dir = img_dir

    def parsing(self, inkml_file, max_width, width):
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
            TraceGroup = TTraceGroup(traceGroup.get("id"), truth, traces, max_width, width)
            TraceGroups.append(TraceGroup)
        
        return TraceGroups 

    def get_variant_color(self, img):
        # normalize the image
        tmp_img = img.astype(float) / 255.0
        # get the variant colors
        variants = 1 / (1 + np.exp(0.24 - 0.6*tmp_img))
        # reset the range of img 
        img = img.astype(float) * variants

        return img.astype(int)

    # deprecated method 
    def stack_backgrounds(self):
        # paper_bg_dir: Path object - direction to folder containing paper backgrounds 

        # file names of these background images
        bg_images = list(self.bg_dir.glob("*.jpg"))
        # file names for inkml files
        inkml_files = list(self.inkml_dir.glob("*.inkml"))
        
        # parsing inkml files
        numbering = 0
        # fix the width and height of the background images
        # bg_w = 1024 - 2048 - 4096
        bg_w = 1024 # pixels
        num_bg = len(bg_images)
        for inkml_file in inkml_files:
            traceGroups = self.parsing(inkml_file, bg_w)
            for traceGroup in traceGroups:
                # get the image of text 
                txt_img = traceGroup.create_image()
                txt_h, txt_w, _ = txt_img.shape
                # get the background image 
                bg_index = randint(0, num_bg-1)
                bg_file_name = bg_images[bg_index]
                bg_img = cv.imread(str(bg_file_name))
                bg_h, ori_bg_w, _ = bg_img.shape
                scale = ori_bg_w / bg_h
                bg_h = int(bg_w * scale)
                bg_img = cv.resize(bg_img, (bg_w, bg_h))
                steps_y = int(bg_h / txt_h)
                for step_y in range(steps_y):
                    # stack the background
                    new_img = bg_img[step_y*txt_h:txt_h + txt_h*step_y, :, :]
                    new_img = np.where(np.not_equal(txt_img, np.array(255)), new_img - self.get_variant_color(new_img) + txt_img, new_img)
                    cv.imshow("image", cv.resize(new_img, (500, 500)) / 255)
                    cv.waitKey(500)
                    # save image
                    numbering += 1
                    img_file = os.path.join(self.img_dir, "{}.png".format(numbering))
                    # cv.imwrite(img_file, new_img)

        return numbering

    def texts_statistic(self):
        inkml_files = list(self.inkml_dir.glob("*.inkml"))
        max_w = 0
        for inkml_file in inkml_files: 
            TraceGroups = self.parsing(inkml_file, 0, 0)
            for TraceGroup in TraceGroups:
                w, _ = TraceGroup.get_size()
                max_w = w if w > max_w else max_w

        return max_w

    def make_indent(self, image, width):
        img_h, img_w, img_c = image.shape
        delta_w = width - img_w 
        indent = randint(100, delta_w-100)
        # create the indent
        img = np.ones(shape=(img_h, width, img_c)) * 255
        img[:, indent:indent+img_w, :] = image

        return img

    def stack_multiple_background(self, min_txt=1, max_txt=5, get_txt_rep=1, method="show"):
        # min_txt: minimum number of text images to stack on top of the background 
        # max_txt: maximum number of text images to stack on top of the background
        # get_txt_rep: get the text images get_txt_rep times to stack on top of a background

        # this method will stack multiple texts on each background image, so we require a portrait background image 
        # file names of these background images
        bg_images = list(self.bg_dir.glob("*.jpg"))
        # file names for inkml files
        inkml_files = list(self.inkml_dir.glob("*.inkml"))

        def construct_document(bg_image, txt_images, spaces, bg_w):
            # get the size and set the width and height of background to the new value
            bg_h, ori_bg_w, _ = bg_image.shape
            scale = ori_bg_w / bg_h
            bg_h = int(bg_w / scale)
            # anchor array to initialize the image
            img = np.ones(shape=(1, bg_w, 3)) * 255
            # array for saving the ground truth
            txts = ""
            for txt_idx in range(len(txt_images)):
                txt_image, txt = txt_images[txt_idx].create_image()
                txts += "{}".format(txt)
                # get random space 
                relative_space = int(spaces[randint(0, len(spaces)-1)] * bg_h)
                # get random indent
                txt_image = self.make_indent(txt_image, bg_w)
                space_above = np.ones(shape=(relative_space, bg_w, 3)) * 255
                img = np.concatenate([img, space_above, txt_image], axis=0)

            # adding space at the bottom
            space_bottom = np.ones(shape=(randint(1, 50), bg_w, 3)) * 255
            img = np.concatenate([img, space_bottom], axis=0)

            # resize the background to fit the text image 
            bg_image = cv.resize(bg_image, (bg_w, bg_h), interpolation=cv.INTER_LINEAR)
            img_h = img.shape[0]
            if bg_h > img_h:
                delta_h = bg_h - img_h
                indent_h = randint(0, delta_h)
                bg_image = bg_image[indent_h:indent_h+img_h, :, :]
            else:
                bg_image = cv.resize(bg_image, (img.shape[1], img.shape[0]), interpolation=cv.INTER_LINEAR)
            # stack the texts on top of the background
            img = np.where(np.not_equal(img, np.array(255)), bg_image - self.get_variant_color(bg_image) + img, bg_image)
            
            return img, txts
        
        print("Prepairing ...")
        # parsing inkml files
        numbering = 0
        bg_w = 1024
        txt_max_w = self.texts_statistic()
        variant_space = [0.02, 0.05, 0.07]
        print("Processing ...")

        gt_texts = {"image_id": [], "text": []}
        # for each background image
        for bg_file in bg_images:
            bg_img = cv.imread(str(bg_file))
            for _ in range(get_txt_rep):
                texts = []
                for _ in range(randint(min_txt, max_txt)):
                    inkml_file = inkml_files[randint(0, len(inkml_files)-1)]
                    TraceGroups = self.parsing(inkml_file, txt_max_w, bg_w)
                    # get a text 
                    texts.append(TraceGroups[randint(0, len(TraceGroups)-1)])
                new_img, gt_txt = construct_document(bg_img, texts, variant_space, bg_w + 200)
                numbering += 1

                if method == "show":
                    print("\n{}".format(gt_txt))
                    cv.imshow("image", new_img / 255)
                    cv.waitKey(1000)
                    print("=======================")
                else: 
                    # save the image
                    img_file = "{}.jpg".format(numbering)
                    cv.imwrite(os.path.join(self.img_dir, img_file), new_img)
                    # write the ground truth text to csv file
                    gt_texts["image_id"].append(img_file)
                    gt_texts["text"].append(gt_txt)

        if method == "save":
            pd.DataFrame(gt_texts).to_csv(os.path.join(self.img_dir, "ground_truth.csv"))

        print("Process completed.")

        return numbering