import random
import re
from itertools import combinations


class RulePuzzle:
    def __init__(self, chunk_map, total_freq, epsilon=0.05, l_r="right", num_rules=3):
        # Chunk map is a map between ngrams and their frequencies
        # Each rule puzzle makes a few Rules (no more than max_rules) and constrains its guesses thereby.
        # Rules take a chunk and allow for . outside of it. ex: ite\Z which allows for smite, spite, etc.
        # It's impossible to guess the rule after one puzzle, but after several... ???
        # Also, chunk map can include regex encodings for ngrams of variable length?

        self.chunk_map = chunk_map
        self.total_freq = total_freq
        self.num_rules = num_rules
        self.l_r = l_r
        self.epsilon = epsilon
        self.chunks = self.chunk_selector()
        self.regexp = [re.compile(chunk) for chunk in self.chunks]

    def chunk_selector(self):
        # returns list of chunks
        val_score = lambda x: True if abs(self.total_freq - sum([y[self.chunk_map] for y in x])) <= self.epsilon else False
        posses = [v for v in combinations(self.chunk_map.keys(), self.num_rules) if val_score(v)]
        return random.choice(posses)