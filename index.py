from add_background.AddBackground import AddBackground
from matplotlib import pyplot as plt 
import numpy as np

image_dir = "images/non_grayscale_paragraphs"
inkml_dir = "InkData_line"
background_dir = "ocr_background/old_paper_background"

total_images = AddBackground(bg_dir=background_dir, inkml_dir=inkml_dir, img_dir=image_dir).stack_multiple_background()
print(total_images)