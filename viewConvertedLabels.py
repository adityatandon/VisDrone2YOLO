# Code to read annotations in the YOLO format and draw
# and display bounding boxes on the associated image file
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
#      └── VisDrone2019-DET-val
#               └── images
#               └── labels
#      └── VisDrone2019-DET-test-dev
#               └── images
#               └── labels

from PIL import Image, ImageDraw

file_name = "0000126_00054_d_0000124"
image_filepath = "VisDrone2019-DET-train/images/" + file_name + ".jpg"
label_filepath = "VisDrone2019-DET-train/labels/" + file_name + ".txt"

# To convert annotations from YOLO format to absolute corner points of a rectangle
def yolo_to_bounding_box(image_class, b_box, w, h):
    # x_center, y_center, width heigth
    half_width = (b_box[2] * w) / 2
    half_height = (b_box[3] * h) / 2
    x_min = int((b_box[0] * w) - half_width)
    y_min = int((b_box[1] * h) - half_height)
    x_max = int((b_box[0] * w) + half_width)
    y_max = int((b_box[1] * h) + half_height)
    return [image_class, x_min, y_min, x_max, y_max]

# To draw bounding boxes on the image
def draw_boxes(img, b_boxes):
    draw = ImageDraw.Draw(img)

    # To assign color based on class label
    color_list = ["red", "green", "blue", "yellow", "purple", "orange", "pink", "teal", "magenta", "turquoise"]

    for b_box in b_boxes:
        draw.rectangle(b_box[1:], outline=color_list[int(b_box[0])], width=1)
    img.show()

# Program start
img = Image.open(image_filepath)
bounding_boxes= []

with open(label_filepath, 'r', encoding='utf8') as file:
    for line in file:
        data = line.strip().split(' ')
        image_class = data[0]
        bounding_box = [float(val) for val in data[1:]]
        bounding_boxes.append(yolo_to_bounding_box(image_class,bounding_box, img.size[0], img.size[1]))

draw_boxes(img, bounding_boxes)