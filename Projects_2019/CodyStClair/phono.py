import nltk
import re

vowels = r'(A[AEHOW(XR?)Y]|E[HRY]|I[HXY]|O[WY]|U[HWX])'
stress = r'1$'

pronunciations = nltk.corpus.cmudict.entries()

_is_vowel = lambda x: re.search(vowels, x)
_count_vowels = lambda x: len(list(filter(_is_vowel, x)))

syllable_counts = {item[0]: _count_vowels(item[1]) for item in pronunciations}

_is_stress = lambda x: re.search(stress, x) != None
_index_of_stress = lambda x: list(map(_is_stress, x)).index(True)

rhymes = {}

for item in pronunciations:
    try:
        rhymes[item[0]] = tuple(item[1][_index_of_stress(item[1]):])
    except ValueError:
        rhymes[item[0]] = None

def syllable_count(word):
    """Returns the number of syllables in a word.

    Arguments:
        word (str): The word to count the syllables of.

    Return (int):
        The number of syllables in word.

    Raises:
        KeyError: If the given word's pronunciation is not known.
    """
    if word.lower() in syllable_counts:
        return syllable_counts[word.lower()]
    raise KeyError("No pronunciation found for: " + word)

def word_to_rhyme(word):
    """Returns the part of a word's pronunciation that determines the rhyme.

    Arguments:
        word (str): The word to find the rhyme of.

    Returns (tuple):
        A tuple representing the pronunciation of the word's rhyme, or None
        if the word has no main stress (e.g. determiners)

    Raises:
        KeyError: If the given word's pronunciation is not known.
    """
    if word.lower() in rhymes:
        return rhymes[word.lower()]
    raise KeyError("No pronunciation found for: " + word)
