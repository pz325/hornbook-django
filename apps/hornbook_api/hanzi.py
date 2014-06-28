# -*- coding: utf-8 -*-

TONES = (
    (0, u'轻声'),
    (1, u'一声'),
    (2, u'二声'),
    (3, u'三声'),
    (4, u'四声')
)

INITIALS = (
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

FINALS = (
    ('a', 'a'),
    ('o', 'o'),
    ('e', 'e'),
    ('i', 'i'),
    ('u', 'u'),
    ('v', u'ü'),
    ('ia', 'ia'),
    ('ua', 'ua'),
    ('uo', 'uo'),
    ('ie', 'ie'),
    ('ve', u'üe'),
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
    ('van', u'üan'),
    ('en', 'en'),
    ('in', 'in'),
    ('un', 'un'),
    ('vn', u'ün'),
    ('anɡ', 'anɡ'),
    ('ianɡ', 'ianɡ'),
    ('uanɡ', 'uanɡ'),
    ('enɡ', 'enɡ'),
    ('ing', 'ing'),
    ('onɡ', 'onɡ')
)

FINALSTR = {
    'a': 'a',
    'o': 'o',
    'e': 'e',
    'i': 'i',
    'u': 'u',
    'v': u'ü',
    'ia': 'ia',
    'ua': 'ua',
    'uo': 'uo',
    'ie': 'ie',
    've': u'üe',
    'ai': 'ai',
    'uai': 'uai',
    'ei': 'ei',
    'ui': 'ui',
    'ao': 'ao',
    'iao': 'iao',
    'ou': 'ou',
    'iu': 'iu',
    'an': 'an',
    'ian': 'ian',
    'uan': 'uan',
    'van': u'üan',
    'en': 'en',
    'in': 'in',
    'un': 'un',
    'vn': u'ün',
    'anɡ': 'anɡ',
    'ianɡ': 'ianɡ',
    'uanɡ': 'uanɡ',
    'enɡ': 'enɡ',
    'ing': 'ing',
    'onɡ': 'onɡ'
}

ATONES = u'ā á ǎ à'.split(' ')
OTONES = u'ō ó ǒ ò'.split(' ')
ETONES = u'ē é ě è'.split(' ')
ITONES = u'ī í ǐ ì'.split(' ')
UTONES = u'ū ú ǔ ù'.split(' ')
YUTONES = u'ǖ ǘ ǚ ǜ'.split(' ')

TONE_ANNOTATION_REPLACEMENTS = {
    'a': 'ATONES',
    'o': 'OTONES',
    'e': 'ETONES',
    'i': 'ITONES',
    'u': 'UTONES',
    'v': 'YUTONES'
}

TONE_ANNOTATIONS = {
     'a': 'a',
     'o': 'o',
     'e': 'e',
     'i': 'i',
     'u': 'u',
     'v': 'v', # ü
     'ia': 'a',
     'ua': 'a',
     'uo': 'o',
     'ie': 'e',
     've': 'e', # üe
     'ai': 'a',
     'uai': 'a',
     'ei': 'e',
     'ui': 'i',
     'ao': 'a',
     'iao': 'a',
     'ou': 'o',
     'iu': 'u',
     'an': 'a',
     'ian': 'a',
     'uan': 'a',
     'van': 'a', # üan
     'en': 'e',
     'in': 'i', # in
     'un': 'u', 
     'ang': 'a',
     'iang': 'a',
     'uang': 'a',
     'eng': 'e',
     'ing': 'i',
     'ong': 'o',
}

def getPinyinStr(initial, final, tone):
    '''
    Generate tonated pinyin string
    e.g. initial = b, final = a, tone = 3, pinyinStr = bǎ
    @param initial
    @param final ü input as 'v'
    @tone
    @return tonated pinyin string
    '''
    finalStr = FINALSTR[final]
    if tone == 0:
        return initial+finalStr
    
    replace = TONE_ANNOTATIONS[final]
    tonatedFinal = []
    for c in final:
        if c == replace:
            tonatedFinal.append(TONE_ANNOTATION_REPLACEMENTS[replace][tone-1])
        else:
            tonatedFinal.append(c)
    f = ''.join(tonatedFinal)
    return initial+f

# TODO: to accomplish this
COMPONENTS = (
    (u'艹', u'草字头'),
    (u'木', u'木字旁'),
    (u'', u'独体字'),
    (u'冫', u'两点水儿'),
    (u'冖', u'秃宝盖儿'),
    (u'讠', u'言字旁儿'),
    (u'厂', u'偏厂儿'),
)

# final = '''a o e i u ü ia ua uo ie üe ai uai ei ui ao iao ou iu an ian uan üan en in un ün ang iang uang eng ing ong'''
# finals = ',\n'.join(["('{f}', '{f}')".format(f=f) for f in final.split(' ')])
# x = 'ā ɑ a'
