from flask import Flask, request, render_template
import os
import cv2
import matplotlib.pyplot as plt

app = Flask(__name__)

def extract_image_name(image_file):
    return os.path.splitext(image_file.filename)[0]

def plot_show_image_with_boxes(image_path, boxes_list, labels, output_filename):
    # Convert image path extension from .xml to .jpg
    image_path_jpg = os.path.splitext(image_path)[0] + '.jpg'

    # Read image
    image = cv2.imread(image_path_jpg)

    if image is not None:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        for box_str in boxes_list:
            xmin, ymin, xmax, ymax, classid = map(float, box_str.split(','))
            xmin, ymin, xmax, ymax = int(xmin), int(ymin), int(xmax), int(ymax)
            cv2.rectangle(image, (xmin, ymin), (xmax, ymax), (255, 0, 0), 5)
            cv2.putText(image, str(labels[int(classid)]), (xmin, ymin - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

        plt.imshow(image)
        plt.axis('off')  # Turn off axis
        plt.savefig(f'static/{output_filename}')  # Save the image with boxes using a unique filename
        plt.close()

def lab(image_path, boxes_list, labels):
    # Convert image path extension from .xml to .jpg
    image_path_jpg = os.path.splitext(image_path)[0] + '.jpg'

    # Read image
    image = cv2.imread(image_path_jpg)

    if image is not None:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        label_counts = {}
        for box_str in boxes_list:
            xmin, ymin, xmax, ymax, classid = map(float, box_str.split(','))
            class_name = labels[int(classid)]
            if class_name in label_counts:
                label_counts[class_name] += 1
            else:
                label_counts[class_name] = 1

        return label_counts

@app.route('/audit', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        image_files = request.files.getlist('image_files')
        
        if not image_files:
            return "No selected files"
        
        results = []
        for image_file in image_files:
            if image_file.filename == '':
                continue  # Skip empty files
            
            image_name = extract_image_name(image_file)
            image_path = os.path.join('uploads', image_file.filename)
            image_file.save(image_path)
            IMAGE_PATH = f'D:/Downloads/IndoorObjectDetectionDataset/data/sequence_1/{image_name}.jpg'
            ANNOTATIONS_PATH = 'D:/Downloads/IndoorObjectDetectionDataset/data/annotations.txt'

            image_path_parts = IMAGE_PATH.split('.')
            image_path_xml = image_path_parts[0].split('/')[-1] + '.xml'

            all_boxes = []
            labels = ['hallway_assist_bar', 'chair', 'hospital_bed', 'handle', 'counter', 'bedside_monitor','iv_pole', 'push_latch', 'light_switch', 'table', 'door_handle', 'cabinet', 'staff','dispenser', 'computer', 'countertop', 'faucet', 'person', 'TV', 'telephone', 'keyboard','mouse', 'drawer', 'toilet', 'restroom_assist_bar', 'sink', 'curtain', 'waste_bin', 'sofa','infusion_pump', 'overbed_table', 'foot_board', 'press_to_open', 'surgical_light', 'operating_bed','medical_drawer', 'utility_cart', 'exam_table', 'elevator_panel', 'bedrail', 'wheel_chair','bedside_table', 'medical_waste_container', 'xray_bed', 'xray_machine', 'syringe_pump','visitor', 'patient', 'breathing_tube', 'ventilator', 'electrosurgical_unit', 'toilet_handle','incubator', 'panda_baby_warmer', 'sequential_compression', 'surgical_instrument', 'hs', 'tv']
            with open(ANNOTATIONS_PATH) as f:
                lines = f.readlines()

            for line in lines:
                line = line.strip().split(' ')
                image_filename = line[0]

                if image_filename == image_path_xml:
                    boxes_list = line[1:]
                    all_boxes.extend(boxes_list)

            output_filename = f"{image_name}_result.jpg"
            plot_show_image_with_boxes(IMAGE_PATH, boxes_list=all_boxes, labels=labels, output_filename=output_filename)
            label_counts = lab(IMAGE_PATH, boxes_list=all_boxes, labels=labels)
            results.append((image_name, label_counts, output_filename))

        return render_template('home.html', results=results)
    
    return render_template('home.html')
    
    return render_template('home.html')

@app.route('/', )
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)