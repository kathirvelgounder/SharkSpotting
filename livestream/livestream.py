import pafy
import cv2
import youtube_dl
import argparse

class LiveStream:

    def __init__(self, url):
        self.url = url
        video = pafy.new(url)
        best = video.getbest(preftype="mp4")
        self.capture = cv2.VideoCapture()
        self.capture.open(best.url)

    #returns both whether reading the frame succeeded and the frame itself
    def get_frame(self):
        success, frame = self.capture.read()
        return success, frame

    def display_frame(self, frame):
        cv2.imshow('frame', frame)
    


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Live Stream from a URL and display video frames received.')
    parser.add_argument('stream', help="URL of video stream.")
    args = parser.parse_args()
    live_stream = LiveStream(args.stream)
    success, frame = live_stream.get_frame()
    while success:
        success, frame = live_stream.get_frame()
        live_stream.display_frame(frame)
        if cv2.waitKey(10) == 27: #exit if Escape is hit
            break

