import cv2
import numpy as np

Annotations = list[list[list[int]], str, float]


def draw_annotations(image: np.ndarray, annotations: Annotations) -> None:
    """Draw annotations on an image."""
    # Iterate through annotations
    for annotation in annotations:
        # Extract coordinates, text, and confidence score
        points, text, confidence = annotation

        # Convert points to numpy array of integers
        points = np.array(points, dtype=np.int32)

        # Draw bounding box
        cv2.polylines(image, [points], isClosed=True, color=(0, 255, 0), thickness=2)

        # Add text
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.5
        font_thickness = 1
        text_size = cv2.getTextSize(text, font, font_scale, font_thickness)[0]
        text_origin = (points[0][0], points[0][1] - 5)
        cv2.putText(image, text, text_origin, font, font_scale, (0, 255, 0), font_thickness)

    # Display the image
    cv2.imshow('Annotated Image', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def find_white_rectangle(image: np.ndarray) -> tuple[int, int, int, int] | None:
    """Find the white rectangle in an image."""
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Threshold the image to create a binary image
    _, binary = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY)
    # Find contours in the binary image
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # Filter contours based on area to find the white rectangle
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 1000:  # Adjust this threshold as needed
            # Draw a bounding rectangle around the white rectangle
            x, y, w, h = cv2.boundingRect(contour)
            return x, y, w, h
    # Display the image with the bounding rectangle

    return None


def extract_lap_time_annotations(annotations: Annotations) -> Annotations:
    """Extract lap times from annotations."""
    # find vertical line of the "Best Lap" text
    best_laps = list(filter(lambda x: x[1].lower() == "best lap", annotations))
    if len(best_laps) == 0:
        return []
    best_lap = best_laps[0]
    y1, y2 = best_lap[0][0][0], best_lap[0][1][0]
    center = (y1 + y2) // 2

    # 1st is BEST LAP, 2nd is the fastest time
    skip = 2
    lap_times = list(filter(lambda x: x[0][0][0] <= center <= x[0][1][0], annotations))[skip:]

    return lap_times


def parse_lap_times(lap_times: Annotations) -> list[float]:
    """Parse lap times from annotations"""
    return [float(annot[1]) for annot in lap_times]


def resize_image(image: np.ndarray, scale_factor: float) -> np.ndarray:
    """Resize an image by a scale factor."""
    height, width = image.shape[:2]
    new_height, new_width = int(height * scale_factor), int(width * scale_factor)
    return cv2.resize(image, (new_width, new_height))

