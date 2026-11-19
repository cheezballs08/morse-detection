from opencv_light_detection.constants import Constants

from typing import Sequence
from cv2.typing import MatLike

import time
import cv2
import numpy as np

class FrameProcessor():

    video_capture: cv2.VideoCapture

    captured_frame: MatLike

    result_gui_frame: MatLike

    contours: Sequence[MatLike]

    contour_midpoints: list[tuple[int, int]] = list()

    previous_light_state: bool = False

    current_light_state: bool

    light_dark_intervals: list[tuple[bool, float]] = list()

    is_first_light_state_check: bool = True

    interval_start_time = time.time()

    def __init__(self, camera_id: int, api_preference: int) -> None:
        self.video_capture = cv2.VideoCapture(camera_id, api_preference)

    def check_opened(self) -> bool:
        return self.video_capture.isOpened()

    def exit(self) -> None:
        self.video_capture.release()
        cv2.destroyAllWindows()

    def check_interrupt_state(self) -> bool:
        if cv2.waitKey(Constants.KEY_WAIT_PERIOD_MILISECONDS) & 0xFF == Constants.EXIT_KEY:
            return True

        return False

    def capture_frame(self) -> bool:

        read_state, frame = self.video_capture.read()

        self.captured_frame = frame

        self.result_gui_frame = frame

        self.contour_midpoints = list()

        return read_state

    def find_contours_hsv(self) -> None:

        frame_hsv: MatLike = cv2.cvtColor(self.captured_frame, cv2.COLOR_BGR2HSV)

        _, _, frame_v = cv2.split(frame_hsv)

        _, edited_frame = cv2.threshold(
            frame_v,
            Constants.MINIMUM_BRIGHTNESS,
            Constants.MAXIMUM_BRIGHTNESS,
            Constants.BRIGHTNESS_TRESHOLD_TYPE
        )

        morphology_kernel = np.ones((Constants.MORPHOLOGY_KERNEL_SIZE, Constants.MORPHOLOGY_KERNEL_SIZE))

        edited_frame = cv2.morphologyEx(edited_frame, Constants.MORPH_TYPE, morphology_kernel)

        edited_frame = cv2.GaussianBlur(
            edited_frame,
            (Constants.GAUSSIAN_KERNEL_SIZE, Constants.GAUSSIAN_KERNEL_SIZE),
            Constants.GAUSSIAN_STD_DEVIATION_AUTO_CALCULATE
        )

        erosion_kernel = np.ones((Constants.EROSION_KERNEL_SIZE, Constants.EROSION_KERNEL_SIZE))

        edited_frame = cv2.erode(edited_frame, erosion_kernel, iterations=Constants.EROSION_ITERATION_COUNT)

        dilation_kernel = np.ones((Constants.DILATION_KERNEL_SIZE, Constants.DILATION_KERNEL_SIZE))

        edited_frame = cv2.dilate(edited_frame, dilation_kernel, iterations=Constants.DILATION_ITERATION_COUNT)

        self.contours, _ = cv2.findContours(edited_frame, Constants.CONTOUR_MODE, Constants.CONTOUR_METHOD)

        self.contours = [contour for contour in self.contours if cv2.contourArea(contour) > Constants.CONTOUR_MIN_SIZE]

    def draw_contours(self) -> None:
        cv2.drawContours(
            self.result_gui_frame,
            self.contours,
            -1,
            Constants.COLOR_GREEN,
            Constants.CONTOUR_DISPLAY_THICKNESS
        )

    def draw_contour_bounding_boxes(self) -> None:

        for contour in self.contours:

            rectangle_x_pos, rectangle_y_pos, rectangle_width, rectangle_height = cv2.boundingRect(contour)

            cv2.rectangle(
                self.result_gui_frame,
                (rectangle_x_pos, rectangle_y_pos),
                (rectangle_x_pos + rectangle_width, rectangle_y_pos + rectangle_height),
                Constants.COLOR_GREEN,
                Constants.BOUNDING_BOX_THICKNESS
            )

            cv2.putText(
                self.result_gui_frame,
                Constants.BOUNDING_BOX_TITLE,
                (rectangle_x_pos - Constants.BOUNDING_BOX_TITLE_X_OFFSET, rectangle_y_pos - Constants.BOUNDING_BOX_TITLE_Y_OFFSET),
                Constants.BOUNDING_BOX_TITLE_FONT,
                Constants.BOUNDING_BOX_TITLE_FONT_SCALE,
                Constants.COLOR_GREEN,
                Constants.BOUNDING_BOX_TITLE_FONT_THICKNESS
            )

    def find_contour_midpoints(self) -> None:
        for contour in self.contours:
            moments = cv2.moments(contour)

            if moments["m00"] != 0:
                midpoint_x_pos = int(moments["m10"] / moments["m00"])
                midpoint_y_pos = int(moments["m01"] / moments["m00"])

                self.contour_midpoints.append((midpoint_x_pos, midpoint_y_pos))

    def draw_contour_midpoints(self) -> None:
        for coordinate in self.contour_midpoints:
            cv2.circle(
                self.result_gui_frame,
                coordinate,
                Constants.DOT_RADIUS,
                Constants.COLOR_GREEN,
                Constants.DOT_THICKNESS
            )

    def update_lightsource_state(self) -> None:
        if not self.is_first_light_state_check:
            self.previous_light_state = self.current_light_state
            self.current_light_state = len(self.contours) != 0

        else:
            self.current_light_state = len(self.contours) != 0
            self.is_first_light_state_check = False


    def draw_lightsource_state(self) -> None:
        if self.current_light_state:
            cv2.putText(
                self.result_gui_frame,
                Constants.HAS_LIGHT_STRING,
                (Constants.DATA_TITLE_X_POSITION, Constants.DATA_TITLE_Y_POSITION),
                Constants.DATA_TITLE_FONT,
                Constants.DATA_TITLE_FONT_SCALE,
                Constants.COLOR_GREEN,
                Constants.DATA_TITLE_FONT_THICKNESS
            )
        else:
            cv2.putText(
                self.result_gui_frame,
                Constants.DOSENT_HAVE_LIGHT_STRING,
                (Constants.DATA_TITLE_X_POSITION, Constants.DATA_TITLE_Y_POSITION),
                Constants.DATA_TITLE_FONT,
                Constants.DATA_TITLE_FONT_SCALE,
                Constants.COLOR_RED,
                Constants.DATA_TITLE_FONT_THICKNESS
            )

    def record_light_activation_intervals(self, trigger_interval_end: bool) -> None:

        if self.previous_light_state != self.current_light_state and not trigger_interval_end:
            duration = time.time() - self.interval_start_time

            self.light_dark_intervals.append((self.previous_light_state, duration))

            self.interval_start_time = time.time()

        elif trigger_interval_end:
            duration = time.time() - self.interval_start_time

            self.light_dark_intervals.append((self.previous_light_state, duration))


    def show_gui(self) -> None:
        cv2.imshow(Constants.WINDOW_NAME, self.result_gui_frame)