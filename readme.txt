AddBackGround(bg_dir, inkml_dir, img_dir)

This class is designed to stack multiple text images on top per background.

Parameters:
    + bg_dir: direction to the folder containing the background images
    + inkml_dir: direction to the folder containing the text images 
    + img_dir: direction to the folder containing the stacked-background images (the result images)

Method: 
    stack_multiple_background(min_txt=1, max_txt=5, get_txt_rep=1, method="show") -> int

    Designed to stack multiple text images on top per background 

    Parameters:
        + min_txt: minimum number of text images to stack on top of a background 
        + max_txt: maximum number of text images to stack on top of a background 
        + get_txt_rep: times to get random(min_txt, max_txt) text images to stack on top of a background
        + method: has "show" or "save" received values indicating whether this method is used to save to just show the results. (If using "show" methos, stacked-background images are shown per 1s)

    Returns: the number of successful stacked-background images 