from parsing_inkml.ParsingInkml import ParsingInkml

images_file = "images/grayscale_lines"
inkml_files = "InkData_line"

total_files = ParsingInkml(inkml_files, images_file, thickness=20)()
print(total_files)