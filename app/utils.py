import cv2
import numpy as np


def apply_colormap_to_frame(frame: np.ndarray, colormap=cv2.COLORMAP_JET) -> np.ndarray:
    normalized_frame = cv2.normalize(frame, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    colored_frame = cv2.applyColorMap(normalized_frame, colormap)

    return colored_frame
