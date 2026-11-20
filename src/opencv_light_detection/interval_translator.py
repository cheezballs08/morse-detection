from enum import Enum

from opencv_light_detection.constants import Constants

MORSE_TO_LETTER_DICTIONARY = {
    ".-": "A",
    "-...": "B",
    "-.-.": "C",
    "-..": "D",
    ".": "E",
    "..-.": "F",
    "--.": "G",
    "....": "H",
    "..": "I",
    ".---": "J",
    "-.-": "K",
    ".-..": "L",
    "--": "M",
    "-.": "N",
    "---": "O",
    ".--.": "P",
    "--.-": "Q",
    ".-.": "R",
    "...": "S",
    "-": "T",
    "..-": "U",
    "...-": "V",
    ".--": "W",
    "-..-": "X",
    "-.--": "Y",
    "--..": "Z",
}

class MorseTokens(Enum):
    DOT = 0
    LINE = 1
    SYMBOL_BREAK = 2
    LETTER_BREAK = 3
    WORD_BREAK = 4
    TIMEOUT = 5

    def __str__(self) -> str:

        match self:
            case MorseTokens.DOT:
                return "."
            case MorseTokens.LINE:
                return "-"
            case MorseTokens.SYMBOL_BREAK:
                return ""
            case MorseTokens.LETTER_BREAK:
                return "/"
            case MorseTokens.WORD_BREAK:
                return "//"
            case MorseTokens.TIMEOUT:
                return "<<<TIMEOUT>>>"


def interval_list_to_morse_token_list(intervals: list[tuple[bool,float]]) -> list[MorseTokens]:

    token_list: list[MorseTokens] = list()

    for interval in intervals:

        if interval[0] == False:

            if  Constants.MORSE_SYMBOL_BREAK_RANGE_MIN <= interval[1] <= Constants.MORSE_SYMBOL_BREAK_RANGE_MAX:
                token_list.append(MorseTokens.SYMBOL_BREAK)

            if  Constants.MORSE_LETTER_BREAK_RANGE_MIN <= interval[1] <= Constants.MORSE_LETTER_BREAK_RANGE_MAX:
                token_list.append(MorseTokens.LETTER_BREAK)

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

def morse_token_list_to_character_list(tokens: list[MorseTokens]) -> list[str]:
    result: list[str] = []
    current_letter: str = ""

    for token in tokens:
        if token == MorseTokens.DOT:
            current_letter += "."

        elif token == MorseTokens.LINE:
            current_letter += "-"

        elif token == MorseTokens.LETTER_BREAK:
            if current_letter:
                result.append(
                    MORSE_TO_LETTER_DICTIONARY.get(current_letter, "?")
                )
                current_letter = ""

        elif token == MorseTokens.WORD_BREAK:
            if current_letter:
                result.append(
                    MORSE_TO_LETTER_DICTIONARY.get(current_letter, "?")
                )
                current_letter = ""

            result.append(" ")

        elif token == MorseTokens.TIMEOUT:
            break

    if current_letter:
        result.append(MORSE_TO_LETTER_DICTIONARY.get(current_letter, "?"))

    return result