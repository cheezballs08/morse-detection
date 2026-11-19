from opencv_light_detection.return_codes import ReturnCode
from opencv_light_detection.frame_processing import FrameProcessor
from opencv_light_detection.constants import Constants

def main() -> int:

    frame_processor = FrameProcessor(Constants.CAMERA_ID, Constants.VIDEO_CAPTURE_API)

    if not frame_processor.check_opened() == True:

        return ReturnCode.EXIT_FAIL_COULD_NOT_OPEN_VIDEO_CAPTURE.value

    while True:

        is_success: bool = frame_processor.capture_frame()

        if not is_success:
            frame_processor.exit()

            return ReturnCode.EXIT_FAIL_COULD_NOT_CAPTURE_FRAME.value

        frame_processor.find_contours_hsv()

        frame_processor.draw_contour_bounding_boxes()

        frame_processor.update_lightsource_state()

        frame_processor.draw_lightsource_state()

        frame_processor.show_gui()

        if frame_processor.check_interrupt_state() == True:
            frame_processor.record_light_activation_intervals(True)

            for interval in frame_processor.light_dark_intervals:
                print(interval)

            frame_processor.exit()

            return ReturnCode.EXIT_SUCCESS.value

        frame_processor.record_light_activation_intervals(False)

if __name__ == "__main__":
    main()