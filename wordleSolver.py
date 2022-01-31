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

        # attempting to filter [("s", 2), ("o", 1), ("r", 1), ("e", 1), ("s", 1)]
        # creates a re for above pattern where set letters are there and . are not set letters
        setLettersRe = re.compile(
            "".join([item[0] if int(item[1]) == 2 else "." for item in wordle])
        )
        self.words = list(filter(setLettersRe.match, self.words))

        # need to do the reverse of above to tell it what letters it doesn't have in what position, but since it is less specific needs to be done for each wrong letter in wrong place
        wrongLets = [item[0] if int(item[1]) != 2 else "." for item in wordle]

        self.words = [
            word
            for word in self.words
            if True not in [wrongLets[i] == word[i] for i in range(len(word))]
        ]

        # for i in range(len(wrongLets)):

        #     pattern = "".join(
        #         [wrongLets[j] if j == i else "." for j in range(len(wrongLets))]
        #     )

        #     # because it is positional and wronglets have . in them, occasionally a pattern like ..... emerges if so just continue and ignore it
        #     if pattern == ".....":
        #         continue

        #     self.words = list(
        #         itertools.filterfalse(re.compile(pattern).match, self.words)
        #     )

        # now we can do non positional filtering based on the letters we would expect it to have given the wordle
        wordleLetList = [item[0] for item in wordle if int(item[1]) != 0]

        # takes all of the words and makes sure that they all have above letters in them
        self.words = [
            word
            for word in self.words
            if not any(
                [wordleLetList.count(let) - word.count(let) for let in wordleLetList]
            )
        ]

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
