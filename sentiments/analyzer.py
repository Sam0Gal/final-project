import nltk

class Analyzer():
    """Implements sentiment analysis."""

    def __init__(self, positives, negatives):
        """Initialize Analyzer."""

        # TODO
        score = 0
        self.positives = []
        self.negatives = []
        with open("positive-words.txt", "r") as lines:
            for line in lines:
                if line.strip().startswith(";") is True or line.strip() == "":
                    continue
                self.positives.append(line.strip())
        with open("negative-words.txt", "r") as lines:
            for line in lines:
                if line.startswith(";") is True or line == "":
                    continue
                self.negatives.append(line.strip())

    def analyze(self, text):
        """Analyze text for sentiment, returning its score."""

        # TODO
        text = text.lower()
        score = 0
        tokenizer = nltk.tokenize.TweetTokenizer()
        tokens = tokenizer.tokenize(text)
        for token in tokens:
            if token in self.positives:
                score += 1
            elif token in self.negatives:
                score -= 1
        return score
