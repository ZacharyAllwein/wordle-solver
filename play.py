from decimal import Rounded
from wordleSolver import WordleSolver
import math

if __name__ == "__main__":
    wordleSolver = WordleSolver("dictionary")

    print("wordle format: w0o1r1d2 ")

    while len(wordleSolver.words) > 1:

        print(wordleSolver.words)

        print("wordle format: w0o1r1d2 ")

        wordle = input("your wordle: ")

        wordle = [(wordle[i], wordle[i + 1]) for i in [0, 2, 4, 6, 8]]
        print(wordle)

        wordleSolver.refine(wordle)
