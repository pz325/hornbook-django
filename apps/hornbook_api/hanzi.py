# -*- coding: utf-8 -*-

TONES = (
    ('0', '轻声'),
    ('1', '一声'),
    ('2', '二声'),
    ('3', '三声'),
    ('4', '四声')
)

INITIAL = (
    ('b', 'b'),
    ('p', 'p'),
    ('m', 'm'),
    ('f', 'f'),
    ('d', 'd'),
    ('t', 't'),
    ('n', 'n'),
    ('l', 'l'),
    ('g', 'g'),
    ('k', 'k'),
    ('h', 'h'),
    ('j', 'j'),
    ('q', 'q'),
    ('x', 'x'),
    ('zh', 'zh'),
    ('ch', 'ch'),
    ('sh', 'sh'),
    ('r', 'r'),
    ('z', 'z'),
    ('c', 'c'),
    ('s', 's'),
    ('y', 'y'),
    ('w', 'w'),
)

FINAL = (
    ('a', 'a'),
    ('o', 'o'),
    ('e', 'e'),
    ('i', 'i'),
    ('u', 'u'),
    ('ü', 'ü'),
    ('ia', 'ia'),
    ('ua', 'ua'),
    ('uo', 'uo'),
    ('ie', 'ie'),
    ('üe', 'üe'),
    ('ai', 'ai'),
    ('uai', 'uai'),
    ('ei', 'ei'),
    ('ui', 'ui'),
    ('ao', 'ao'),
    ('iao', 'iao'),
    ('ou', 'ou'),
    ('iu', 'iu'),
    ('an', 'an'),
    ('ian', 'ian'),
    ('uan', 'uan'),
    ('üan', 'üan'),
    ('en', 'en'),
    ('in', 'in'),
    ('un', 'un'),
    ('ün', 'ün'),
    ('anɡ', 'anɡ'),
    ('ianɡ', 'ianɡ'),
    ('uanɡ', 'uanɡ'),
    ('enɡ', 'enɡ'),
    ('ing', 'ing'),
    ('onɡ', 'onɡ')
)

ATONE = 'ā á ǎ à'.split(' ')
OTONE = 'ō ó ǒ ò'.split(' ')
ETONE = 'ē é ě è'.split(' ')
ITONE = 'ī í ǐ ì'.split(' ')
UTONE = 'ū ú ǔ ù'.split(' ')
YUTONE = 'ǖ ǘ ǚ ǜ'.split(' ')

TONE_ANNOTATION_REPLACE = dict(
    a=ATONE,
    o=OTONE,
    e=ETONE,
    i=ITONE,
    u=UTONE,
    yu=YUTONE)

TONE_ANNOTATION = (
    ('a', 'a'),
    ('o', 'o'),
    ('e', 'e'),
    ('i', 'i'),
    ('u', 'u'),
    ('ü', 'ü'), # yu
    ('ia', 'a'),
    ('ua', 'a'),
    ('uo', 'o'),
    ('ie', 'e'),
    ('üe', 'e'),
    ('ai', 'a'),
    ('uai', 'a'),
    ('ei', 'e'),
    ('ui', 'i'),
    ('ao', 'a'),
    ('iao', 'a'),
    ('ou', 'o'),
    ('iu', 'u'),
    ('an', 'a'),
    ('ian', 'a'),
    ('uan', 'a'),
    ('üan', 'a'),
    ('en', 'e'),
    ('in', 'i'),
    ('un', 'u'),
    ('ün', 'ü'), # yu
    ('anɡ', 'a'),
    ('ianɡ', 'a'),
    ('uanɡ', 'a'),
    ('enɡ', 'e'),
    ('ing', 'i'),
    ('onɡ', 'o')
)

# TODO: to accomplish this
COMPONENTS = (
    ('艹', '草字头'),
    ('木', '木字旁'),
    ('', '独体字'),
    ('冫', '两点水儿'),
    ('冖', '秃宝盖儿'),
    ('讠', '言字旁儿'),
    ('厂', '偏厂儿'),
)

final = '''a o e i u ü ia ua uo ie üe ai uai ei ui ao iao ou iu an ian uan üan en in un ün anɡ ianɡ uanɡ enɡ ing onɡ'''
finals = ',\n'.join(["('{f}', '{f}')".format(f=f) for f in final.split(' ')])
x = 'ā ɑ a'

