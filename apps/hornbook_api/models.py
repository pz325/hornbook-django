from django.db import models
from django.core.cache import cache
import os.path
import random
from trie import Trie

FILE_MOST_COMMON_CHARACTERS = '/../../data/most_common_chinese_characters.txt'
FILE_MOST_COMMON_WORDS = '/../../data/most_common_chinese_words.txt'

# Create your models here.
class MostCommonCharacter():
    '''
    500 most common Chinese characters
    '''
    @staticmethod
    def load():
        chars = cache.get('most_common_characters')
        if chars is None:
            f = open(os.path.dirname(__file__) + FILE_MOST_COMMON_CHARACTERS)
            chars = []
            for line in f.readlines():
                char, freq = line.split(' ')
                u_char = unicode(char, 'utf-8')
                freq = int(freq)
                chars.append((u_char, freq))
            cache.set('most_common_characters', chars)
        return chars
   
    @staticmethod
    def get_all():
        return MostCommonCharacter.load()

    @staticmethod
    def get_one():
        chars = MostCommonCharacter.load()
        index = random.randint(0, len(chars)-1)
        u_char = chars[index][0]
        return u_char


class MostCommonWord():
    '''
    Words contains only MostCommonCharacter
    '''

    trie = None

    @staticmethod
    def generate_trie():
        if MostCommonWord.trie is None:
            MostCommonWord.trie = Trie()
            f = open(os.path.dirname(__file__) + FILE_MOST_COMMON_WORDS)
            for line in f.readlines():
                word, frequency, _ = line.split(' ')
                u_word = unicode(word, 'utf-8')
                MostCommonWord.trie.insert(u_word)

    @staticmethod
    def get_words(ref_character):
        if MostCommonWord.trie is None:
            MostCommonWord.generate_trie()
        return MostCommonWord.trie.enumerate(ref_character)
