from bs4 import BeautifulSoup
import re
import operator
import codecs
import sys
from file_utils import FileUtils

class WordCount:
    def __init__(self):
        self.global_count = {}
        self.document_length = {}
        self.document_count = {}
        self.word_counts = {}
        self.files = FileUtils().get_files_from_path(sys.argv[1])
        self.stop_words = map(lambda x: unicode(x), codecs.open('stop_words.txt','r', 'utf-8').read().split())

    # strips word of special characters
    def strip(self, text):
        text = re.sub(ur'[\W_0-9]+', u'', text, flags=re.UNICODE)
        return unicode(text)

    # removes all the stop words from the list of words
    def remove_stop_words(self, words):
        return [w for w in words if not w in self.stop_words]

    # method to calculate word count for a words
    # also maintains a global count of occurrences of a word
    def fill_dictionaries(self, word_count, word):
        word = self.strip(unicode(word).lower())
        if not word:
            return
        if word_count.has_key(word):
            word_count[word] += 1
        else:
            word_count[word] = 1
        if self.global_count.has_key(word):
            self.global_count[word] += 1
        else:
            self.global_count[word] = 1
        return word_count

    # maintains a hashmap to keep the number of documents in which
    # a word occurs
    def fill_document_count(self, words):
        words = set(map(lambda x: unicode(x), words))
        for word in words:
            if self.document_count.has_key(word):
                self.document_count[word] += 1
            else:
                self.document_count[word] = 1

    # Opens the html files, parses it into text by removing the markup
    # Converts it into tokens
    # generates the word count and document word_counts
    # also maintains the document length hashmap
    def calculate(self):
        for file in self.files:
            html_file = codecs.open('{}/{}'.format(sys.argv[1], file), 'r')
            file_name = file.split('.')[0]
            word_count = {}
            soup = BeautifulSoup(html_file.read(), 'html.parser')
            html_file.close()
            words = soup.get_text(strip=True).split()
            words = self.remove_stop_words(words)
            map(lambda word: self.fill_dictionaries(word_count, word), words)
            sorted_x = sorted(word_count.items(), key=operator.itemgetter(1), reverse=True)
            self.document_length[file.split(".")[0]] = len(words)
            self.fill_document_count(word_count.keys())
            self.word_counts[file_name] = word_count

if __name__ == "__main__":
    FileUtils().clean_dir(sys.argv[2])
    wc = WordCount()
    wc.calculate()
