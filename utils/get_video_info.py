import cv2
from tkinter import filedialog
import sys
import os
import time

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.insert(0, parent_dir)

from lib.fprint import fprint


def main():
    fprint("I", "Choose a video")

    try:
        video_path = filedialog.askopenfilename(title="Choose a video")
        capture = cv2.VideoCapture(video_path)
        width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = int(capture.get(cv2.CAP_PROP_FPS))
    except:
        fprint("E", "There was an error!")

    fprint("S", "The video dimensions are:")
    print(f" - WIDTH: {width}")
    print(f" - HEIGHT: {height}")
    print(f" - FPS: {fps}\n")

    fprint("W", "The program will exit in 5s")
    time.sleep(5)
    exit(0)
    
if __name__ == "__main__":
    main()