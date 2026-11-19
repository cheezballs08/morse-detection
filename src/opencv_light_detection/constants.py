from typing import Final

import cv2

class Constants():

    CAMERA_ID: Final[int] = 21234
    VIDEO_CAPTURE_API: Final[int] = cv2.CAP_V4L2

    MINIMUM_BRIGHTNESS: Final[int] = 240
    MAXIMUM_BRIGHTNESS: Final[int] = 255

    BRIGHTNESS_TRESHOLD_TYPE: Final[int] = cv2.THRESH_BINARY
    MORPH_TYPE: Final[int] = cv2.MORPH_OPEN

    CONTOUR_MODE: Final[int] = cv2.RETR_EXTERNAL
    CONTOUR_METHOD: Final[int] = cv2.CHAIN_APPROX_SIMPLE

    CONTOUR_MIN_SIZE: Final[int] = 200

    MORPHOLOGY_KERNEL_SIZE: Final[int] = 5
    MORPHOLOGY_KERNEL_NONE: None = None

    GAUSSIAN_KERNEL_SIZE: Final[int] = 11
    GAUSSIAN_KERNEL_NONE: None = None
    GAUSSIAN_STD_DEVIATON: Final[int] = 0
    GAUSSIAN_STD_DEVIATION_AUTO_CALCULATE: Final[int] = 0

    EROSION_KERNEL_SIZE: Final[int] = 3
    EROSION_KERNEL_NONE: None = None
    EROSION_ITERATION_COUNT: Final[int] = 2

    DILATION_KERNEL_SIZE: Final[int] = 3
    DILATION_KERNEL_NONE: None = None
    DILATION_ITERATION_COUNT: Final[int] = 4

    CONTOUR_DISPLAY_THICKNESS: Final[int] = 2

    BOUNDING_BOX_THICKNESS: Final[int] = 2
    BOUNDING_BOX_TITLE: Final[str]= "LIGHT"

    BOUNDING_BOX_TITLE_X_OFFSET: Final[int] = 0
    BOUNDING_BOX_TITLE_Y_OFFSET: Final[int] = 10

    BOUNDING_BOX_TITLE_FONT: Final[int] = cv2.FONT_HERSHEY_SIMPLEX

    BOUNDING_BOX_TITLE_FONT_SCALE: Final[float] = 0.5
    BOUNDING_BOX_TITLE_FONT_THICKNESS: Final[int] = 2

    WINDOW_NAME: Final[str] = "Result"

    COLOR_RED: Final[tuple[int, int, int]] = (255, 0, 0)
    COLOR_GREEN: Final[tuple[int, int, int]] = (0, 255, 0)
    COLOR_BLUE: Final[tuple[int, int, int]] = (0, 0, 255)
    COLOR_WHITE: Final[tuple[int, int, int]] = (255, 255, 255)
    COLOR_BLACK: Final[tuple[int, int, int]] = (0, 0, 0)

    EXIT_KEY: Final[int] = ord("q")
    KEY_WAIT_PERIOD_MILISECONDS: Final[int] = 1