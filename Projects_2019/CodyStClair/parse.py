import re

BAD_CHARS = r'[^ A-Za-z0-9\']'

def parse_text(text):
    """Parses the input text into a list of words,
       after removing problematic characters.

    Arguments:
        text (str): The text to parse.

    Return (tuple):
        A tuplerepresenting the parsed words.
    """
    return tuple(re.sub(BAD_CHARS, '', text).split())

def parse_poem(poem_text):
    """Parses the text of the given poem into a list of parsed lines.

    Arguments:
        poem_text (str): A string representing the poem to parse.

    Return (tuple):
        A tuple containing the parsed lines of the poem.
    """
    return tuple(map(parse_text, filter(lambda x: x, poem_text.split('\n'))))

def parse_prose(prose_text):
    """Parses prose text, removing line breaks.

    Arguments:
        prose_text (str): A string representing the prose to parse.

    Return (tuple):
        A tuple containing the parsed words of the text.
    """
    return parse_text(re.sub(r'\n', ' ', prose_text))
