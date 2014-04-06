# -*- coding: utf-8 -*-

TONES = (
    (0, '轻声'),
    (1, '一声'),
    (2, '二声'),
    (3, '三声'),
    (4, '四声')
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

ATONES = 'ā á ǎ à'.split(' ')
OTONES = 'ō ó ǒ ò'.split(' ')
ETONES = 'ē é ě è'.split(' ')
ITONES = 'ī í ǐ ì'.split(' ')
UTONES = 'ū ú ǔ ù'.split(' ')
YUTONES = 'ǖ ǘ ǚ ǜ'.split(' ')

TONE_ANNOTATION_REPLACEMENTS = dict(
    a=ATONES,
    o=OTONES,
    e=ETONES,
    i=ITONES,
    u=UTONES,
    yu=YUTONES)

TONE_ANNOTATIONS = dict(
     a='a',
     o='o',
     e='e',
     i='i',
     u='u',
     yu='yu', # ü
     ia='a',
     ua='a',
     uo='o',
     ie='e',
     yue='e', # üe
     ai='a',
     uai='a',
     ei='e',
     ui='i',
     ao='a',
     iao='a',
     ou='o',
     iu='u',
     an='a',
     ian='a',
     uan='a',
     yuan='a', # üan
     en='e',
     yin='i', # in
     un='u', 
     ang='a',
     iang='a',
     uang='a',
     eng='e',
     ing='i',
     ong='o',
)

def getPinyinStr(initial, final, tone):
    '''
    Generate tonated pinyin string
    e.g. initial = b, final = a, tone = 3, pinyinStr = bǎ
    @param initial
    @param final ü input as it is
    @tone
    @return tonated pinyin string
    '''
    if tone == 0:
        return '{i}{f}'.format(i=initial, f=final)

    if final == 'ü': 
        key = 'yu'
    elif final == 'üe': 
        key = 'yue'
    elif final == 'üan': 
        key = 'yuan'
    elif final == 'in': 
        key = 'yin'
    else: 
        key = final
    replace = TONE_ANNOTATIONS[key]
    tonatedFinal = []
    for c in final:
        if c == replace:
            tonatedFinal.append(TONE_ANNOTATION_REPLACEMENTS[replace][tone-1])
        else:
            tonatedFinal.append(c)
    f = ''.join(tonatedFinal)
    return '{i}{f}'.format(i=initial, f=f)

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

# final = '''a o e i u ü ia ua uo ie üe ai uai ei ui ao iao ou iu an ian uan üan en in un ün ang iang uang eng ing ong'''
# finals = ',\n'.join(["('{f}', '{f}')".format(f=f) for f in final.split(' ')])
# x = 'ā ɑ a'
