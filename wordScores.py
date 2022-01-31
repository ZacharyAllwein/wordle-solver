import math
import json


class WordScores:

    # length of words defaults to 5 as this is meant for wordle solving
    def __init__(self, dictionary, lengthOfWords=5):

        # create a formated dictionary where all words are lowercase, and match the length paramater
        self.dictionary = list(
            filter(
                lambda word: len(word) == lengthOfWords,
                map(lambda word: word.lower(), dictionary),
            )
        )

        # Creates a list of columns of each of the words. ex. [word, what] -> [w, w], [o, h], [r, a], [d, t]
        columns = [[word[i] for word in self.dictionary] for i in range(lengthOfWords)]

        # uses the columns created above to figure out scores of each of the words.
        # scores are calculated based on frequency of individual letter in columns, for my purpose this is good enough.
        # once scores have been calculated it then sorts them in descending order
        self.scores = {
            item[1]: item[0]
            for item in sorted(
                [
                    (item[1], item[0])
                    for item in {
                        word: math.prod(
                            [
                                columns[i].count(word[i]) / len(columns[i])
                                for i in range(len(word))
                            ]
                        )
                        for word in self.dictionary
                    }.items()
                ],
                reverse=True,
            )
        }

    # writes self.scores attribute to file for easy viewing
    def toFile(self, name):

        with open(f"{name}.json", "w") as file:
            json.dump(self.scores, file)
