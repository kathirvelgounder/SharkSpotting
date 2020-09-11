import pafy
import cv2
import youtube_dl
import argparse
from Label import Label
from typing import List, Tuple, Dict
from Model import PyTorchModel
import webcolors

ydl_opts = {
    'nocheckcertificate:': True
}

class LiveStream:

    def __init__(self, url, model):
        self.url = url
        video = pafy.new(url, ydl_opts=ydl_opts)
        best = video.getbest(preftype="mp4")
        self.capture = cv2.VideoCapture()
        self.capture.open(best.url)
        self.model = model

    def display_frame(self, frame):
        cv2.imshow('frame', frame)

    def analyze_stream(self):
        success, frame = self.capture.read()
        count = 0
        while success:
            #run model predictions
            labels = self.model.predict(frame)

            #display bounding boxes with labels
            self.display_bounding_boxes(frame, labels)

            # #display lines between sharks and other sharks or sharks and people, with distances labeled
            # if frame_has_shark(labels):
            #     shark_distances = get_distances_from_sharks(labels)
            #     display_distances(frame, shark_distances)

            #display this frame
            frame = cv2.resize(frame, dsize=(1024, 540), interpolation=cv2.INTER_CUBIC)
            cv2.imshow(self.url,frame)

            #need this for the video stream to work continuously, basically says press 'q' to quit
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break

            success, frame = self.capture.read()
        
    def display_bounding_boxes(self, frame, labels):
        for label in labels:
            #if label.score > 0.8:
            label_name = label.group.lower()
            upperLeft = (label.x_min, label.y_min)
            lowerRight = (label.x_max, label.y_max)
            print(label_name + " at " + str(upperLeft) + " " + str(lowerRight))
            cv2.rectangle(frame, upperLeft, lowerRight, webcolors.name_to_rgb(label.color), thickness=3)

    def display_distances(self, frame, shark_distances):
        color_of_line = classes["shark"]["color"]
        for shark_label in shark_distances:
            shark_coords = shark_label.get_midpoint()
            for other in shark_distances[shark_label]:
                other_coords = other.get_midpoint()
                cv2.line(frame, shark_coords, other_coords, webcolors.name_to_rgb(color_of_line), 3)
                text_location = self.midpoint_of_line(shark_coords, other_coords)
                distance = self.distance_between_objects(shark_label, other) * GSD
                self.display_label(frame, text_location, str(int(distance)))
            


    def display_label(self, img, label_location, label_text):
        cv2.putText(img, label_text, label_location, cv2.FONT_HERSHEY_SIMPLEX, 1, webcolors.name_to_rgb(classes["shark"]["color"]), 2)


    #for now, just use distance between midpoint of bounding boxes
    def distance_between_objects(self, obj1, obj2) -> float:
        mid_x1, mid_y1 = obj1.get_midpoint()
        mid_x2, mid_y2 = obj2.get_midpoint()
        return math.sqrt(((mid_x2 - mid_x1)**2) + ((mid_y2 - mid_y1)**2))

    def frame_has_shark(self, labels: List[Label]) -> bool:
        for label in labels:
            if label.group.lower() == 'shark':
                return True
        return False

    #return the midpont of the line between two objects so we know where put the lines label
    def midpoint_of_line(self, p1: Tuple[int, int], p2: Tuple[int, int]) -> Tuple[int, int]:
        return (int)((p2[0]-p1[0])/2, (p2[1]-p1[1])/2)

    # if a shark is detected in the frame, get the distances from the shark to other sharks and
    # humans in the frame
    def get_distances_from_sharks(self, labels: List[Label]) -> Dict[Label, List[Label]]:
        shark_distances = dict()
        for label in labels:
            if label.group.lower() == 'shark':
                others: List[Label] = list()
                for other in labels:
                    if (not other.id == label.id) and (other.group.lower() == 'person' or other.group.lower() == 'shark'):
                        others.add(other)
                shark_distances[label] = others
        return shark_distances

    

    #using a bounding ellipse would be more accurate to find distance between objects (on average)
    #as opposed to a bounding box.
    def get_bounding_ellipse_from_box(self, x_min, x_max, y_min, y_max):
        pass

    #TODO: find a way to implement this
    def distance_between_ellipses(self):
        pass
    


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Live Stream from a URL and display video frames received.')
    parser.add_argument('stream', help="URL of video stream.")
    parser.add_argument('model', help="PyTorch or TensorFlow model file (local).")
    args = parser.parse_args()
    model = PyTorchModel(args.model)
    live_stream = LiveStream(args.stream, model) 
    live_stream.analyze_stream() #run model on live stream
    