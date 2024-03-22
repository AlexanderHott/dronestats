import os

import easyocr
import cv2
import keyboard
import numpy as np
from PIL import ImageGrab

from dronestats.vision import draw_annotations, find_white_rectangle, extract_lap_time_annotations, parse_lap_times, \
    resize_image
from dronestats.writer import write_to_csv


ACTIVATOR_KEY = "space"
CSV_FILE = os.environ["APPDATA"] + "\\race_times.csv"


def extract_race_times(image: np.ndarray) -> list[float] | None:
    # image_path = "../images/race_1.png"
    # image = cv2.imread(image_path)

    image = resize_image(image, 0.75)

    # draw_annotations(image, annotations)
    bounding_box = find_white_rectangle(image)
    if bounding_box is None:
        print("No white rectangle found")
        return None
    x, y, w, h = bounding_box

    # crop the image to x,y,w,h
    cropped_image = image[y:y + h, x:x + w]

    reader = easyocr.Reader(["en"])
    annotations = reader.readtext(cropped_image)
    # print(annotations)
    # draw_annotations(cropped_image, annotations)
    annotations = extract_lap_time_annotations(annotations)
    # draw_annotations(cropped_image, annotations)
    return parse_lap_times(annotations)


if __name__ == '__main__':
    while True:
        keyboard.wait(ACTIVATOR_KEY)

        # take screenshot
        screen = ImageGrab.grab()
        np_screen = np.array(screen)

        # analyze screenshot to get race times
        race_times = extract_race_times(np_screen)
        if race_times is None:
            print("No lap times found")
            continue
        else:
            print("lap times", race_times)

        # append race times to record
        write_to_csv(race_times, CSV_FILE)