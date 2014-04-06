
from django.db import models
from django.core.cache import cache
from django.contrib import admin
import os.path
import random
from trie import Trie

import hanzi

class Pinyin(models.Model):
    initial = models.CharField(max_length=4, choices=hanzi.INITIALS)
    final = models.CharField(max_length=20, choices=hanzi.FINALS)
    tone = models.PositiveSmallIntegerField(default=0, choices=hanzi.TONES)
    pinyin_str = models.CharField(max_length=20, editable=False) # tone annotated pinyin str

    # def save(self, *args, **kwargs):
    #     '''
    #     extends default save() to create pinyin_str
    #     '''
    #     self.pinyin_str = '{initial}{final}{tone}'.format(initial=self.initial, final=self.final, tone=self.tone)
    #     super(Pinyin, self).save(*args, **kwargs)

    def __str__(self):
        return '{initial}{final}{tone}'.format(initial=self.initial, final=self.final, tone=self.tone)

    # @classmethod
    # def create(cls, initial, final, tone):
    #     pinyin = cls(initial, final, tone)

    #     pinyin.pinyin_str = 
    # #     return cls(name=name, email=email)

class Tag(models.Model):
    tag = models.CharField(max_length=200)

    def __str__(self):
        return str(self.tag)

class Vocabulary(models.Model):
    '''
    Hanzi vocabulary model
    '''
    vocabulary = models.CharField(max_length=10)
    numStrokes = models.PositiveSmallIntegerField(default=0)
    component = models.CharField(max_length=4, choices=hanzi.COMPONENTS)
    pinyins = models.ManyToManyField(Pinyin)  # handle multiple pronounciation
    tags = models.ManyToManyField(Tag)

    # @classmethod
    # def create(vocabulary):
    #     return cls(name=name, email=email)

class TaggedVocabulary(models.Model):
    tag = models.ForeignKey(Tag)
    vocabularies = models.ManyToManyField(Vocabulary)

admin.site.register(Pinyin)
admin.site.register(Tag)
admin.site.register(Vocabulary)
admin.site.register(TaggedVocabulary)


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

