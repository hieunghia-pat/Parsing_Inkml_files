from add_background.AddBackground import AddBackground
import numpy as np

image_dir = "images/non_grayscale_lines"
inkml_dir = "InkData_line"
background_dir = "ocr_background/ocr_background"

total_images = AddBackground(bg_dir=background_dir, inkml_dir=inkml_dir, img_dir=image_dir)\
                .stack_multiple_background(min_txt=1, max_txt=1, get_txt_rep=10, method="save")

print(total_images) 