from collections import Counter
from wordScores import WordScores
import json
import itertools
from os.path import exists
import re


class WordleSolver:
    def __init__(self, dictPath):

        # loading dictionary from provided path
        dictionary = json.load(open(f"{dictPath}.json"))

        # creates required scores json file
        WordScores(dictionary).toFile("scores")

        # loads in score json
        scores = json.load(open("scores.json"))

        # already orded in greatest probability to least
        self.words = scores.keys()

    # takes in an ordered dict representing a 5 letter word where each letter can be of values 0, 1, 2
    # letters with 0, are not in the word, letters with 1 are in the word but not in the right place and letters with 2 are in the word and in the right place
    def refine(self, wordle):

        # creates a re for above pattern where set letters are there and . are not set letters
        setLettersRe = re.compile(
            "".join([item[0] if int(item[1]) == 2 else "." for item in wordle])
        )
        self.words = list(filter(setLettersRe.match, self.words))

        # need to do the reverse of above to tell it what letters it doesn't have in what position, but since it is less specific needs to be done for each wrong letter in wrong place
        wrongLets = [item[0] if int(item[1]) != 2 else "." for item in wordle]
        self.words = list(
            filter(
                lambda word: True
                not in [wrongLets[i] == word[i] for i in range(len(word))],
                self.words,
            )
        )

        # now we can do non positional filtering based on the letters we would expect it to have given the wordle
        wordleLetList = [item[0] for item in wordle if int(item[1]) != 0]

        self.words = list(
            filter(
                lambda word: all(
                    [True if let in word else False for let in wordleLetList]
                ),
                self.words,
            )
        )

        # after that we can filter based on letters the wordle absolutley does not have
        wordleMissingList = [
            item[0]
            for item in wordle
            if int(item[1]) == 0 and item[0] not in wordleLetList
        ]

        # filtering, send above list to string and format it into re set, then filter false on it
        if wordleMissingList:
            self.words = list(
                itertools.filterfalse(
                    re.compile(
                        str(wordleMissingList).replace(",", "").replace("'", "")
                    ).search,
                    self.words,
                )
            )
