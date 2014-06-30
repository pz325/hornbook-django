
from django.db import models
from django.db import IntegrityError
from django.core.cache import cache
from django.contrib import admin
import os.path
import random
from trie import Trie

import hanzi_base

class Pinyin(models.Model):
    initial = models.CharField(max_length=3, choices=hanzi_base.INITIALS)
    final = models.CharField(max_length=5, choices=hanzi_base.FINALS)
    tone = models.PositiveSmallIntegerField(default=0, choices=hanzi_base.TONES)
    pinyin_str = models.CharField(max_length=20, blank=True, editable=False) # tone annotated pinyin str
    signature = models.SlugField(max_length=20, editable=False, unique=True) # pinyin signature
    
    def save(self, *args, **kwargs):
        '''
        extends default save() to create pinyin_str
        '''
        signature = self.initial+self.final+str(self.tone)
        try:
            self.signature = signature;
            self.pinyin_str = hanzi_base.getPinyinStr(self.initial, self.final, self.tone)
            super(Pinyin, self).save(*args, **kwargs)
        except IntegrityError:
            pass

    def __str__(self):
        return self.pinyin_str

class Tag(models.Model):
    tag = models.SlugField(max_length=200, unique=True)

    def __str__(self):
        return str(self.tag)

class Hanzi(models.Model):
    '''
    Hanzi characer model
    '''
    hanzi = models.CharField(max_length=3, db_index=True, unique=True, blank=False, null=False)
    numStrokes = models.PositiveSmallIntegerField(default=0)
    strokes = models.CharField(max_length=100)
    radix = models.CharField(max_length=3, choices=hanzi_base.RADIX)
    pinyins = models.ManyToManyField(Pinyin)  # handle multiple pronounciation
    tags = models.ManyToManyField(Tag)

admin.site.register(Pinyin)
admin.site.register(Tag)
admin.site.register(Hanzi)

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

import codecs
def importHanzi():
    f = codecs.open('apps/hornbook_api/strokeorder.freq.txt', 'rb', 'utf-8')
    for l in f.readlines():
        tokens = l.split(' ')
        numStrokes = int(tokens[1])
        hanzi = tokens[3]
        strokes = tokens[0]
        h = Hanzi(hanzi=hanzi, numStrokes=numStrokes, strokes=strokes)
        h.save()