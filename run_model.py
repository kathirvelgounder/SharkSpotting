import argparse
import cv2
import time
from Model import PyTorchModel
from Model import TFModel

def run_model(mp4_file, model):
    vidcap = cv2.VideoCapture(mp4_file)
    success, frame = vidcap.read()
    count = 0
    while success:

        #run model predictions
        labels = model.predict(frame)
        #display image with any bounding boxes on it
        cv2.imshow(mp4_file,frame)

        #display labels
        for label in labels:
            cv2.rectangle(frame, (label.x_min, label.y_min), (label.x_max, label.y_max), thickness=15)
        #need this for the video stream to work continuously
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

        success, frame = vidcap.read()
        



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run PyTorch or TensorFlow model on an mp4 video.')
    parser.add_argument('mp4', help="Path to the video.")
    args = parser.parse_args()

    model = PyTorchModel("actual model goes here") #replace the string with the actual PyTorch or TensorFlow Model
    run_model(args.mp4, model)