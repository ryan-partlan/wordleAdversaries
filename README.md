This is a project that I worked on due to my curiosity with the game Wordle.

This program is a little AI that takes from the Cambridge dictionary and generates random wordles to challenge itself with. There is a naive approach to guessing based on the overall frequency of the letters in the word, balanced by a disincentive for picking words with repeat letters.

The parameters can be adjusted for different Wordle lengths, number of guesses, etc. For a standard game of Wordle (5 letters, 6 guesses), the algorithm solves it about 86% of the time.

My eventual goals for this project are to investigate the relationship between an agent generating puzzles according to a set of simple regular expressions/CFGs, and a guessing AI agent trying to determine those rules. I am interested in how the signals given by the solving of a Wordle can be used to detect inherent patterns.