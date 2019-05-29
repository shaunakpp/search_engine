import codecs
import sys
import os
import shutil
import operator
from file_utils import FileUtils
from term_weights import TermWeights

class Index:
    def __init__(self):
        self.dictionary_entry = []
        self.term_weight_calculator = TermWeights()
        self.postings = {}

    # Generate postings hashmap using the the normalized BM25 scores from
    # the term weight calculator
    def generate_postings(self):
        self.term_weight_calculator.calculate()
        for file_name, bm_25 in self.term_weight_calculator.bm_25_scores.items():
            for word, score in bm_25.items():
                if not float(score) == 0.0:
                    self.postings[unicode("{}_{}").format(word, file_name)] = score

    # decorator method for getting the document count hashmap which stores
    # the number of documents a word occurs in
    def document_count(self):
        return self.term_weight_calculator.word_count_calculator.document_count

    # Primary function to generate postings.txt and dictionary.txt files
    # Both postings and dictionary files are in alphabetically sorted order
    def generate(self):
        self.generate_postings()
        postings_file = codecs.open('{}/postings.txt'.format(sys.argv[2]), 'w', 'utf-8')
        dictionary_file = codecs.open('{}/dictionary.txt'.format(sys.argv[2]), 'w', 'utf-8')
        position = 1
        for tup in sorted(self.postings.items(), key=operator.itemgetter(0)):
            word, doc_id = unicode(tup[0]).split("_")
            score = tup[1]
            postings_file.write(unicode("{},{}\n").format(doc_id, score))
            if not word in self.dictionary_entry:
                self.dictionary_entry.append(word)
                dictionary_file.write(unicode("{}\n{}\n{}\n").format(word, self.document_count()[word], position))
            position += 1
        postings_file.close()
        dictionary_file.close()

if __name__ == "__main__":
    FileUtils().clean_dir(sys.argv[2])
    Index().generate()
