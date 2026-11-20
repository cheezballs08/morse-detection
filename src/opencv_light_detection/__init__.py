from opencv_light_detection.return_codes import ReturnCode
from opencv_light_detection.frame_processing import FrameProcessor
from opencv_light_detection.constants import Constants
import opencv_light_detection.interval_translator as interval_translator

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

        # frame_processor.draw_contour_bounding_boxes()

        frame_processor.update_lightsource_state()

        frame_processor.draw_lightsource_state()

        frame_processor.show_gui()

        if frame_processor.check_interrupt_state() == True:
            frame_processor.record_light_activation_intervals(True)

            intervals = frame_processor.light_dark_intervals

            frame_processor.exit()

            for interval in intervals:
                print(interval)

            # assuming first interval is always dark

            intervals.pop(0)

            morse_tokens = interval_translator.interval_list_to_morse_token_list(intervals)

            print("<------->")

            print(morse_tokens)

            print("<------->")

            for token in morse_tokens:
                print(token, end=" ")

            print()

            print("<------->")

            character_sequence = interval_translator.morse_token_list_to_character_list(morse_tokens)

            print(character_sequence)

            print("<------->")

            for character in character_sequence:
                print(character, end="")

            return ReturnCode.EXIT_SUCCESS.value

        frame_processor.record_light_activation_intervals(False)

if __name__ == "__main__":
    main()