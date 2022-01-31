from decimal import Rounded
from wordleSolver import WordleSolver
import math

if __name__ == "__main__":

    # new instance of wordleSolver dictionary that creates a new set of scores based on a dictionary
    wordleSolver = WordleSolver("dictionary")

    while len(wordleSolver.words) > 1:

        # give all usable words
        print(wordleSolver.words)

        # example formating
        print("wordle format: w0o1r1d2 ")

        wordle = input("your wordle: ")

        # makes the wordle usable
        wordle = [(wordle[i], wordle[i + 1]) for i in [0, 2, 4, 6, 8]]

        # refines the list
        wordleSolver.refine(wordle)

    print(wordleSolver.words)
