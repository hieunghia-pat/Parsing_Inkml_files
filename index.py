from add_background.AddBackground import AddBackground


image_dir = "images/non_grayscale_paragraphs"
inkml_dir = "InkData_paragraph"
background_dir = "ocr_background/old_paper_background"

total_images = AddBackground(bg_dir=background_dir, inkml_dir=inkml_dir, img_dir=image_dir, thickness=20).stack_backgrounds()
print(total_images)