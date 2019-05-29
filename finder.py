import mmap
import os
import codecs

# used for searching a term in dictionary and getting the postings entry
class Finder:
    def __init__(self):
        self.position_map = {}
        self.file = codecs.open('dictionary.txt', 'r+', 'utf-8')
        self.seeker = 0
        self.locator = 0
        self.generate_map()
    # uses memory map for parsing large dictionary file and generates a position map
    # position map is used for searching a term
    def generate_map(self):
        mm = mmap.mmap(self.file.fileno(), 0)
        while self.seeker < mm.size():
            mm.seek(self.seeker)
            word = mm.readline()
            letter = word[0]
            if letter not in self.position_map.keys():
                self.position_map[letter] = self.seeker
            self.seeker += len(word) + len(mm.readline()) + len(mm.readline())
        mm.close()

    # uses position map for searching a term and returns number of entries of the word
    # and first entry in postings file
    # find is file io based using a range search
    # ranges are based on starting letter of the term
    # this works as dictionary is lexicographically sorted
    def find(self, query):
        letter = query[0]
        self.locator = self.position_map[letter]
        number_of_entries = 0
        postings_index = 0
        mm = mmap.mmap(self.file.fileno(), 0)
        while True:
            mm.seek(self.locator)
            word = mm.readline()
            if word[0] != query[0]:
                print('word not found: {}'.format(query))
                break
            if word.strip() == str(query):
                number_of_entries = int(mm.readline().strip())
                postings_index = int(mm.readline().strip())
                break

            self.locator += len(word) + len(mm.readline()) + len(mm.readline())
        mm.close()
        return(number_of_entries, postings_index)
