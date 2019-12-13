import random
import phono

class PoemGenerator:
    def _get_rhyme_partition(self):
        """Partitions the words available by rhyme.

        Return (set):
            A set of sets of rhyming words.
        """
        rhymes = {}
        for word in self.words:
            try:
                rhyme = phono.word_to_rhyme(word)
            except KeyError:
                continue
            if rhyme is None:
                continue
            if rhyme not in rhymes:
                rhymes[rhyme] = []
            rhymes[rhyme].append(word)
        return set(frozenset(rhymes[i]) for i in rhymes)
    def __init__(self, text):
        """Creates a poem generator object.

        Arguments:
            text (list): A list of strings to build bigrams from.
        """
        rev_text = list(reversed(text))
        self.bigrams = set(zip(rev_text, rev_text[1:]))
        self.words = set(text)
        self.rhymes = self._get_rhyme_partition()
    def _gen_sequence(self, syllables, prev_word):
        """Generates a sequence of words meeting the syllable constraint.

        Arguments:
            syllables (int): The number of syllables the line ought to have.
            prev_word (str): The previous word in the sequence (not counted in syllables).

        Return (list):
            A sequence meeting the syllable count requirement, or None if no such
            sequence was found.
        """
        if syllables == 0:
            return []
        if syllables < 0:
            return None
        possible_cont = [i[1] for i in self.bigrams if i[0] == prev_word]
        random.shuffle(possible_cont)
        for cont in possible_cont:
            try:
                available_syllables = syllables - phono.syllable_count(cont)
            except KeyError:
                continue
            remnant = self._gen_sequence(available_syllables, cont)
            if remnant != None:
                remnant.append(cont)
                return remnant
        return None
    def gen_line(self, syllables, seed=None):
        """Generates a line of a poem with the specified constraints.

        Arguments:
            syllables (int): The number of syllables the line ought to have.
            seed (str): The word to end the line with.

        Return (list):
            The newly-generated line, or None if no valid line was found.
        """
        if not seed:
            seed = random.choice(self.words)
        available_syllables = syllables - phono.syllable_count(seed)
        if available_syllables < 0:
            return None
        if available_syllables == 0:
            return [seed]
        cont = self._gen_sequence(available_syllables, seed)
        if cont == None:
            return None
        cont.append(seed)
        return cont
    def _try_rhyme_set(self, syllables, rhyme_group):
        """Tries to generate a rhyming set of lines with the meter specified by
        syllables using the words in rhyme_group.

        Arguments:
            syllables (list): A list of syllable counts for each line to be
            generated.
            rhyme_group (list): A list of rhyming words in the generator's text.

        Return (list):
            A list of the new rhyming lines, or None if no such set could be
            constructed.
        """
        solution = []
        for spec in syllables:
            possible_lines = [self.gen_line(spec, rhyme) for rhyme in rhyme_group]
            possible_lines = list(filter(lambda x: x, possible_lines))
            if not possible_lines:
                return None
            solution.append(random.choice(possible_lines))
        return solution
    def gen_rhyme_group(self, syllables):
        """Generates a set of rhyming lines with the specified syllable counts.

        Arguments:
            syllables (list): A list of syllable counts for each line to be
            generated.

        Return (list):
            A list of the new rhyming lines (which are lists themselves).
        """
        potential_rhyme_sets = [i for i in self.rhymes if len(i) >= len(syllables)]

        while potential_rhyme_sets:
            current_attempt = random.choice(potential_rhyme_sets)
            attempt_list = list(current_attempt)
            random.shuffle(attempt_list)
            solution = self._try_rhyme_set(syllables, attempt_list)
            if solution is not None:
                break
            potential_rhyme_sets.remove(current_attempt)
        return solution
    def gen_poem(self, lines):
        """Generates a poem meeting the given line specifications.

        Arguments:
            lines (list): A list of rhyme groups, which contain line groups,
            which specify syllable counts and line indices.

        Return (list):
            The newly-generated poem as a list of lines, which are lists of words,
            or None if no solution can be found.
        """
        highest_index = 0
        for rhyme_group in lines:
            for line_group in rhyme_group:
                for index in line_group.line_indices:
                    if index > highest_index:
                        highest_index = index
        poem = [None for i in range(highest_index+1)]
        for rhyme_group in lines:
            rhyme_list = list(rhyme_group)
            solution = self.gen_rhyme_group([i.syllables for i in rhyme_list])
            if solution is None:
                return None
            for i in range(len(rhyme_list)):
                for line_index in rhyme_list[i].line_indices:
                    poem[line_index] = solution[i]
        return poem
