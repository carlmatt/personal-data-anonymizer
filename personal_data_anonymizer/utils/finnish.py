""" Module for the conjugation of Finnish names
"""
import re


vowels = '[aeiouyåäö]'
consonants = '[bcdfghjklmnpqrstvwxz]'
diphthongs = [
    'ai', 'ei', 'oi', 'ui', 'yi', 'äi', 'öi',
    'au', 'eu', 'iu', 'ou',
    'äy', 'öy', 'ey', 'iy',
    'ie', 'uo', 'yö'
]
cases = [
    # ['nominatiivi', ''],
    ['genetiivi', 'n'],
    ['akkusatiivi', 'n'],
    ['partitiivi', 'a'],
    ['essiivi', 'na'],
    ['translatiivi', 'ksi'],
    ['inessiivi', 'ssa'],
    ['elatiivi', 'sta'],
    ['illatiivi', 'on'],
    ['adessiivi', 'lla'],
    ['ablatiivi', 'lta'],
    ['allatiivi', 'lle'],
    ['abessiivi', 'tta'],
    ['komitatiivi', 'nsa'],
    # ['instruktiivi', '---'],
    ['komparatiivi', 'sti'],
    ['monikko', 't']
]

cases_dict = {case: ending for (case, ending) in cases}

substitutions = [
    [r'nen$', r'se'],
    [r'tis$', r'ttii'],
    [r'ton$', r'ttoma'],
    [r'tön$', r'ttömä'],
    [r'pan$', r'ppama'],
    [r'nyt$', r'nee'],
    [r'nut$', r'nee'],
    [r'eer$', r'eeri'],
    [r'ies$', r'iehe'],
    [r'mus$', r'mukse'],
    [r'hus$', r'hukse'],
    [r'tus$', r'tukse'],
    [r'nto$', r'nno'],
    [r'(%s)\1([iaueäo])$'%('[kpt]'), r'\1\2'],
    [r'(%s%s%s)$'%(consonants, consonants, vowels), r'\1'],
    [r'k(%s)s$'%vowels, r'kk\1\1'],
    [r'p(%s)s$'%vowels, r'pp\1\1'],
    [r'(%s)s$'%vowels, r'\1\1'],
    [r't(%s)$'%vowels, r'd\1'],
    [r'(%s)$'%vowels, r'\1']
]


def ending(word):
    if not re.search(r'[aou]', word[:-1]):
        return re.sub(r'a$', 'ä', word)
    else:
        return word


def conjugate(noun, case):
    suffix = cases_dict[case]
    conjugation = noun
    for t in substitutions:
        if re.search(t[0], noun):
            conjugation = re.sub(t[0], t[1] + suffix, noun)
            break
    return ending(conjugation)
