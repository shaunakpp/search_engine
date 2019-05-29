import re
import operator
import codecs
import sys
import linecache
from itertools import islice
from finder import Finder

# Main class for retrieving documents based on queries
class Retriever:
    def __init__(self, query):
        self.stop_words = map(lambda x: unicode(x), codecs.open('stop_words.txt','r', 'utf-8').read().split())
        self.finder = Finder()
        self.query = query
        self.tokens =  self.parse()

    # removes spaces, punctuation from query
    def strip(self, text):
        text = re.sub(ur'[\W_0-9]+', u'', text, flags=re.UNICODE)
        return unicode(text.lower())

    # removes all the stop words from the list of words
    def remove_stop_words(self, words):
        return [w for w in words if not w in self.stop_words]

    # cleans query by stripping punctuations and stop words
    def parse_query(self, query):
        text = map(lambda x: self.strip(x), query)
        return(self.remove_stop_words(text))

    # parses input query, checks if weights are given in input
    # weights are assumed if -w option is provided
    # if not, then all terms in query are given 1 weight
    def parse(self):
        temp = {}
        if self.query[0] == '-w':
            l = self.query[1:]
            for tup in [(l[i],l[i+1]) for i in range(0,len(l),2)]:
                temp[tup[0]] = float(tup[1])
        else:
            for token in self.query:
                temp[token] = 1
        tokens = self.parse_query(temp.keys())
        for key in temp.keys():
            if key not in tokens:
                temp.pop(key, None)
        return temp

    # driver function calculates scores and prints the results
    def run(self):
        print(self.query)
        self.parse()
        results = {}
        for tup in self.tokens.items():
            token, weight = tup
            number_of_entries, postings_index = self.finder.find(unicode(token))
            for i in range(number_of_entries):
                line = linecache.getline('postings.txt', postings_index)
                doc_id, score = line.split(",")
                if doc_id in results.keys():
                    results[doc_id] += float(score) * weight
                else:
                    results[doc_id] = float(score) * weight
                postings_index += 1
        sorted_results = sorted(results.items(), key=operator.itemgetter(1), reverse=True)

        for tup in islice(filter(lambda t: t[1] > 0.0, sorted_results), 10):
            print('{}.html {}'.format(tup[0], round(tup[1], 3)))

if __name__ == "__main__":
    Retriever(sys.argv[1:]).run()
