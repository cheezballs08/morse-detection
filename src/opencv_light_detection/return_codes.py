from enum import Enum

class ReturnCode(Enum):
    EXIT_SUCCESS = 0
    EXIT_FAIL_COULD_NOT_OPEN_VIDEO_CAPTURE = 1
    EXIT_FAIL_COULD_NOT_CAPTURE_FRAME = 2