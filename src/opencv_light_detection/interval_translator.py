from enum import Enum

from opencv_light_detection.constants import Constants


class MorseTokens(Enum):
    DOT = 0
    LINE = 1
    SYMBOL_BREAK = 2
    WORD_BREAK = 3
    TIMEOUT = 4

    def __str__(self) -> str:

        match self:
            case MorseTokens.DOT:
                return "."
            case MorseTokens.LINE:
                return "-"
            case MorseTokens.SYMBOL_BREAK:
                return ""
            case MorseTokens.WORD_BREAK:
                return " "
            case MorseTokens.TIMEOUT:
                return "<<<TIMEOUT>>>"


def interval_list_to_morse_token_list(intervals: list[tuple[bool,float]]) -> list[MorseTokens]:

    token_list: list[MorseTokens] = list()

    for interval in intervals:

        if interval[0] == False:

            if  Constants.MORSE_SYMBOL_BREAK_RANGE_MIN <= interval[1] <= Constants.MORSE_SYMBOL_BREAK_RANGE_MAX:
                token_list.append(MorseTokens.SYMBOL_BREAK)

            elif Constants.MORSE_WORD_BREAK_RANGE_MIN <= interval[1] <= Constants.MORSE_WORD_BREAK_RANGE_MAX:
                token_list.append(MorseTokens.WORD_BREAK)

            elif Constants.MORSE_TIMEOUT_RANGE_MIN <= interval[1] <= Constants.MORSE_TIMEOUT_RANGE_MAX:
                token_list.append(MorseTokens.TIMEOUT)
                return token_list

        else:

            if  Constants.MORSE_DOT_RANGE_MIN <= interval[1] <= Constants.MORSE_DOT_RANGE_MAX:
                token_list.append(MorseTokens.DOT)

            elif Constants.MORSE_LINE_RANGE_MIN <= interval[1] <= Constants.MORSE_LINE_RANGE_MAX:
                token_list.append(MorseTokens.LINE)

    return token_list