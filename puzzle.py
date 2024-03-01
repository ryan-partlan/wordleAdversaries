from collections import defaultdict, Counter


class Puzzle:
    def __init__(self, word, n_guesses):
        self.word = word
        self.word_l_count = Counter(self.word)
        self.letts = set(word)
        self.n_guesses = n_guesses

    def eval_guess(self, guess):
        good_lett_set = set([lett for lett in guess if lett in self.letts])
        bad_letts = set([lett for lett in guess if lett not in self.letts])
        guess_l_count = Counter(guess)
        word_info = []
        lett_info = defaultdict(set)
        max_repeats = {}
        i = 0
        for g, corr in zip(guess, self.word):
            if guess_l_count[g] > self.word_l_count[g]:
                max_repeats[g] = self.word_l_count[g]
            if g in good_lett_set and g != corr:
                lett_info[g].add(i)
            i += 1
            if g == corr:
                word_info += g
            else:
                word_info += "-"
        self.n_guesses -= 1
        return word_info, lett_info, bad_letts, max_repeats






