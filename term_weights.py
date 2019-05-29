import sys
import math
from file_utils import FileUtils
from word_count import WordCount

class TermWeights:
    def __init__(self):
        self.files = FileUtils().get_files_from_path(sys.argv[1])
        self.file_count = len(self.files)
        self.k1 = 1.2
        self.b = 0.75
        self.max_score = 0
        self.min_score = 100
        self.avg_doc_length = 0
        self.idf = {}
        self.word_count_calculator = WordCount()
        self.bm_25_scores = {}

    # Calculates the IDF value for a word
    def calculate_idf(self):
        for word, count in self.word_count_calculator.document_count.items():
            self.idf[word] = math.log10((self.file_count - count + 0.5) / (count + 0.5))
        self.avg_doc_length = sum(self.word_count_calculator.document_length.values()) / self.file_count

    # normalizes the BM25 scores to values between 0 and 1
    def normalize_score(self, score):
        if (self.max_score - self.min_score) == 0:
            return 0
        else:
            return((score - self.min_score) / (self.max_score - self.min_score))

    # Primary method that calculates the BM25 score using the word count
    # Also keeps track of the max and min BM25 scores to be used for normalization
    def calculate(self):
        self.word_count_calculator.calculate()
        self.calculate_idf()
        for file_name, word_count_dict in self.word_count_calculator.word_counts.items():
            bm_25 = {}
            for word, count in word_count_dict.items():
                try:
                    if self.word_count_calculator.global_count[word] != 1 and len(word) != 1:
                        count = int(count)
                        numerator = (count * ( self.k1 + 1) ) * float(self.idf[word])
                        denominator = (count + self.k1 * (1 - self.b + (self.b * (int(self.word_count_calculator.document_length[file_name])/self.avg_doc_length))))
                        bm_25_score = (numerator / denominator)
                        bm_25[word] = bm_25_score
                        if bm_25_score > self.max_score:
                            self.max_score = bm_25_score
                        if bm_25_score < self.min_score:
                            self.min_score = bm_25_score
                except KeyError:
                    continue
            self.bm_25_scores[file_name] = bm_25
        self.normalize()

    def normalize(self):
        for file_name, bm_25 in self.bm_25_scores.items():
            for word, score in bm_25.items():
                bm_25[word] = self.normalize_score(score)

if __name__ == "__main__":
    FileUtils().clean_dir(sys.argv[2])
    tw = TermWeights()
    tw.calculate()
