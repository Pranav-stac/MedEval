import os
import cv2
import matplotlib.pyplot as plt

def plot_show_image_with_boxes(image_path, boxes_list):
    """
    Plot and display an image with bounding boxes and object names.
    Args:
    image_path : str : path to the image
    boxes_list : List[str] : List of strings with each string containing bounding box coordinates in the format 'xmin,ymin,xmax,ymax,classid'
    Returns:
    None
    Outputs:
    Image is displayed with bounding boxes and object names drawn on it
    """
    # Convert image path extension from .xml to .jpg
    image_path_jpg = os.path.splitext(image_path)[0] + '.jpg'

    # Read image
    image = cv2.imread(image_path_jpg)

    if image is not None:  # Check if the image is loaded successfully
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Plot boxes and object names
        for box_str in boxes_list:
            xmin, ymin, xmax, ymax, classid = map(float, box_str.split(','))
            xmin, ymin, xmax, ymax = int(xmin), int(ymin), int(xmax), int(ymax)  # Convert to integers
            cv2.rectangle(image, (xmin, ymin), (xmax, ymax), (255, 0, 0), 5)
            cv2.putText(image, str(labels[int(classid)]), (xmin, ymin - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

        plt.imshow(image)
        plt.show()
    else:
        print("Error: Unable to load the image.")
# Take image name as input
image_name = input("Enter the image name: ")
IMAGE_PATH = f'D:/Downloads/IndoorObjectDetectionDataset/data/sequence_1/{image_name}.jpg'
ANNOTATIONS_PATH = 'D:/Downloads/IndoorObjectDetectionDataset/data/annotations.txt'

# Split the image path and replace the extension with '.xml'
image_path_parts = IMAGE_PATH.split('.')
image_path_xml = image_path_parts[0].split('/')[-1] + '.xml'  # Extract only the filename without the path
print(image_path_xml)

# Initialize a list to store all bounding boxes
all_boxes = []
labels = [
    'hallway_assist_bar', 'chair', 'hospital_bed', 'handle', 'counter', 'bedside_monitor',
    'iv_pole', 'push_latch', 'light_switch', 'table', 'door_handle', 'cabinet', 'staff',
    'dispenser', 'computer', 'countertop', 'faucet', 'person', 'TV', 'telephone', 'keyboard',
    'mouse', 'drawer', 'toilet', 'restroom_assist_bar', 'sink', 'curtain', 'waste_bin', 'sofa',
    'infusion_pump', 'overbed_table', 'foot_board', 'press_to_open', 'surgical_light', 'operating_bed',
    'medical_drawer', 'utility_cart', 'exam_table', 'elevator_panel', 'bedrail', 'wheel_chair',
    'bedside_table', 'medical_waste_container', 'xray_bed', 'xray_machine', 'syringe_pump',
    'visitor', 'patient', 'breathing_tube', 'ventilator', 'electrosurgical_unit', 'toilet_handle',
    'incubator', 'panda_baby_warmer', 'sequential_compression', 'surgical_instrument', 'hs', 'tv'
]
# Read all annotations from the file
with open(ANNOTATIONS_PATH) as f:
    lines = f.readlines()

# Iterate over each annotation in the file
for line in lines:
    line = line.strip().split(' ')
    
    # Extract the image filename from the annotation
    image_filename = line[0]
    
    # Check if the annotation is for the current image
    if image_filename == image_path_xml:
        # Extract bounding box information and accumulate them
        boxes_list = line[1:]
        all_boxes.extend(boxes_list)

# Plot all accumulated bounding boxes on the image
plot_show_image_with_boxes(IMAGE_PATH, boxes_list=all_boxes)