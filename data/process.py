#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import defaultdict

f_chars = open('most_common_chinese_characters.txt')
most_common_chars = []
for line in f_chars.readlines():
    char, freq = line.split(' ')
    u_char = unicode(char, 'utf-8')
    freq = int(freq)
    most_common_chars.append((u_char, freq))
print(most_common_chars[0: 10])
d = [dict(u_char=ch, frequency=f) for (ch, f) in most_common_chars]
print d[0:10]

# f_words = open('most_common_chinese_words.txt')

# most_common_chars = defaultdict()
# most_common_words = defaultdict()

# for line in f_words.readlines():
#     word, freq, _ = line.split(' ')
#     u_word = unicode(word, 'utf-8')
#     most_common_words[u_word] = freq

# for line in f_chars.readlines():
#     u_char = unicode(line, 'utf-8').strip()
#     if u_char in most_common_words:
#         most_common_chars[u_char] = most_common_words[u_char]

# most_common_chars_tuple = []
# for key, value in most_common_chars.iteritems():
#     most_common_chars_tuple.append((key, value))

# print(most_common_chars_tuple[0:10])
# s = sorted(most_common_chars_tuple, key=lambda u_char: int(u_char[1]), reverse=True)
# print(s[0:10])

# f = open('most_common_chinese_characters_freq.txt', 'w')
# for u_char in s:
#     f.write('{0} {1}\n'.format(u_char[0].encode('utf-8'), u_char[1]))
