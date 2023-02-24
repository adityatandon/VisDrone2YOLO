# Download the original VisDrone dataset and follow 
# this directory structure to use this code as-is
# 
# └── working directory 
#      └── visDrone2YOLO.py
#      └── viewConvertedLabels.py
#      └── filterVisDroneLabels.py
#      └── VisDrone2019-DET-train
#               └── annotations
#               └── images
#               └── labels (will be created)
#      └── VisDrone2019-DET-val
#               └── annotations
#               └── images
#               └── labels (will be created)
#      └── VisDrone2019-DET-test-dev
#               └── annotations
#               └── images
#               └── labels (will be created)
#      └── VisDrone2019-DET-test-challenge
#               └── images

from PIL import Image
import os
from os import listdir
from os.path import isfile, join

# Image directories - change for train, val and test-dev
image_dir = "VisDrone2019-DET-val/images/"
annot_dir = "VisDrone2019-DET-val/annotations/"
output_dir = "VisDrone2019-DET-val/labels/"
remove_ignored = True

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

def convert_annotation(img_size, bbox):
    # Convert VisDrone bounding box to YOLO bounding box in xywh pattern
    width_div = 1.0 / img_size[0]
    height_div = 1.0 / img_size[1]
    return [(bbox[0] + bbox[2] / 2) * width_div, (bbox[1] + bbox[3] / 2) * height_div, bbox[2] * width_div, bbox[3] * height_div]

# Read all filenames in the original annotations directory and add the names to a list
fileNames = [file_name for file_name in listdir(annot_dir) if isfile(join(annot_dir, file_name))]

for file in fileNames:

    basename = os.path.basename(file)
    filename = os.path.splitext(basename)[0] 

    with open(annot_dir + file, 'r', encoding='utf8') as f:
        img = Image.open(image_dir + filename + '.jpg')

        for line in f:
            # Separate individual elements in the annotations separated by ','
            data = line.strip().split(',')
            class_label = int(data[5]) - 1   # Assume YOLO classes in the range 0-9 with 0-pedestrian and 9-motor

            if(remove_ignored==True):
                considered = data[4] # If ignored annotations should be removed, check whether current annotation is considered
            elif(remove_ignored==False):
                considered = 1  # If ignored annotations are not to be removed, consider all annotations
            
            if((considered!=str(0)) and (class_label>=0) and (class_label<=9)): # Check for valid classes
                bounding_box_visdrone = [float(x) for x in data[:4]]
                yolo_bounding_box = convert_annotation(img.size, bounding_box_visdrone)
                bounding_box_string = " ".join([str(x) for x in yolo_bounding_box]) # Create the annotation string to be written

                with open(output_dir + file, 'a+', encoding="utf-8") as output_file:
                    output_file.write(f"{class_label} {bounding_box_string}\n") # Write the converted annotation with class in YOLO format