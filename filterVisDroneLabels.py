# Code to read annotations in the YOLO format and remove
# annotations from classes that are filtered out
#
# Follow this directory structure to use this code as-is
#
# └── working directory 
#      └── visDrone2YOLO.py
#      └── viewConvertedLabels.py
#      └── filterVisDroneLabels.py
#      └── VisDrone2019-DET-train
#               └── images
#               └── labels 
#               └── labels-filtered (will be created)
#      └── VisDrone2019-DET-val
#               └── images
#               └── labels
#               └── labels-filtered (will be created)
#      └── VisDrone2019-DET-test-dev
#               └── images
#               └── labels
#               └── labels-filtered (will be created)

import os
from os import listdir
from os.path import isfile, join

label_dir = "VisDrone2019-DET-val/labels/"
output_dir = "VisDrone2019-DET-val/labels-filtered/"

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Read all filenames in the labels directory and add the names to a list
fileNames = [file_name for file_name in listdir(label_dir) if isfile(join(label_dir, file_name))]

# Add the class labels that will be retained after filtering, eg: 0, 1, 2 
# Range: 0-9. All labels not added will be filtered out.
retain_labels = [7, 2, 5]

for file in fileNames:

    basename = os.path.basename(file)
    filename = os.path.splitext(basename)[0]  

    with open(os.path.join(label_dir, f"{filename}.txt"), 'r', encoding='utf8') as f:
        for line in f:
            label = int(line[0])    # Label is the first character on the line
            
            if(label in retain_labels):
                with open(os.path.join(output_dir, f"{filename}.txt"), "a+", encoding="utf-8") as file:
                    file.write(line)