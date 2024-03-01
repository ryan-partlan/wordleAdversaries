import random
from puzzle import *


class WordleBot:

    def __init__(self, w_len, dict_dir="words.txt", freq_dir="word_freqs.txt"):
        self.w_len = w_len
        self.all_words = self.read_dict(dict_dir)
        self.w_list = self.all_words.copy()
        self.freqs = self.read_freqs(freq_dir)
        self.word_info = list("-" * w_len)
        self.lett_info = defaultdict(set)
        self.bad_letts = set()
        self.max_repeat = {}

    def new_game(self):
        self.word_info = list("-" * self.w_len)
        self.lett_info = defaultdict(set)
        self.bad_letts = set()
        self.max_repeat = {}
        self.w_list = self.all_words.copy()

    def read_dict(self, dict_dir):
        alph = set(list("abcdefghijklmnopqrstuvwxyz"))
        with open(dict_dir, "r") as f:
            unf_words = [list(word.rstrip("\n").lower()) for word in f.readlines() if len(word) - 1 == self.w_len]
            filt_func = lambda word: True if all([char in alph for char in word]) else False
            f_words = [word for word in unf_words if filt_func(word)]
            return f_words

    def read_freqs(self, freq_dir):
        with open(freq_dir, "r") as f:
            return {line.split(" ")[0].lower(): float(line.split(" ")[1]) for line in f.readlines()}

    def make_puzzle(self, n_guesses=6):
        i = random.randint(0, len(self.all_words))
        # IDEA: Have some distribution that it uses to choose the words
        word = self.all_words[i]
        return Puzzle(word, n_guesses)

    def thin_words(self):
        def check_poss(word):
            l_count = Counter(word)
            for i, letter in enumerate(self.word_info):
                if letter != "-" and letter != word[i]:
                    return False
                if i in self.lett_info[word[i]]:
                    return False
                if word[i] in self.bad_letts:
                    return False
                if l_count[letter] > self.max_repeat.get(letter, 1000):
                    return False
            return True
        w_list = [word for word in self.w_list if check_poss(word)]
        return w_list

    def make_guess(self, puzz):
        def get_score(word):
            l_count = Counter(word)
            max_rep = max(l_count.values())
            score = sum([self.freqs[letter] for letter in word])
            if max_rep > 1:
                score /= (max_rep * puzz.n_guesses)
            return score
        guess = max(self.w_list, key=get_score)
        word_inf, lett_info, bad, max_rep = puzz.eval_guess(guess)
        for key in lett_info.keys():
            self.lett_info[key] = self.lett_info[key].union(lett_info[key])
        for key in max_rep.keys():
            self.max_repeat[key] = max_rep[key]
        for i, lett in enumerate(word_inf):
            if self.word_info[i] == "-":
                self.word_info[i] = word_inf[i]
        if guess == puzz.word:
            return guess, True
        self.bad_letts = self.bad_letts.union(bad)
        return guess, False

    def play(self, n_guesses):
        p = self.make_puzzle(n_guesses=n_guesses)
        win = False
        for _ in range(n_guesses):
            win = self.play_turn(p)
            if win:
                break
        return win

    def play_turn(self, p):
        guess, res = self.make_guess(p)
        # print(guess)
        # print(self.word_info)
        self.w_list = self.thin_words()
        return res

if __name__=="__main__":
    tests = 100
    corrs = 0
    w = WordleBot(5)
    for _ in range(tests):
        if w.play(6) == True:
            corrs += 1
        w.new_game()
    print(f"Accuracy is {corrs/tests}")