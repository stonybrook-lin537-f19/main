from collections import namedtuple
import phono

LineGroup = namedtuple("LineGroup", ["text", "syllables", "line_indices"])

def identify_meter(line):
    """Counts the number of syllables in the given line.

    Arguments:
        line (list): The line to operate on.

    Return (int):
        The number of syllables in the given line.

    Raises:
        KeyError: If a word is not found in the pronunciation dictionary.
    """
    return sum(map(phono.syllable_count, line))

def identify_dup_lines(poem):
    """Identifies duplicate lines in a poem.

    Arguments:
        poem (list): A list of the parsed lines in the poem.

    Return (list):
        A list of LineGroups denoting groups of lines with the same text.

    Raises:
        KeyError: If a word is not found in the pronunciation dictionary.
    """
    dup_lines = {}
    for i in range(len(poem)):
        if poem[i] not in dup_lines:
            dup_lines[poem[i]] = []
        dup_lines[poem[i]].append(i)
    return list([LineGroup(i, identify_meter(i), frozenset(dup_lines[i])) for i in dup_lines])

def identify_rhymes(line_groups):
    """Augments the lines of the given poem with rhyme scheme information.

    Arguments:
        line_groups (set): The set of line groups in the poem to operate on.

    Return (set):
        A set of sets of rhyming LineGroups.

    Raises:
        KeyError: If a LineGroup's rhyme cannot be found.
    """
    rhyme_groups = {}
    for group in line_groups:
        rhyme = phono.word_to_rhyme(group.text[-1])
        if rhyme not in rhyme_groups:
            rhyme_groups[rhyme] = []
        rhyme_groups[rhyme].append(group)
    return set([frozenset(rhyme_groups[i]) for i in rhyme_groups])

def analyze_poem(poem):
    """Counts the syllables of each line and identifies the poem's rhyme scheme.

    Arguments:
        poem (list): A list of the parsed lines in the poem.

    Return (set):
        A set partitioned into rhyme groups which contain LineGroups
        whose content is the syllable count of the lines they represent.

    Raises:
        KeyError: If a word is not found in the pronunciation dictionary.
    """
    return identify_rhymes(identify_dup_lines(poem))
