from pymystem3 import Mystem
from json import dumps

MONTH = [
    "январь",
    "февраль",

    "март",
    "апрель",
    "май",

    "июнь",
    "июль",
    "август",

    "сентябрь",
    "октябрь",
    "ноябрь",

    "декабрь",
]

WEEK_DAYS = [
    "понедельник",
    "вторник",
    "среда",
    "четверг",
    "пятница",
    "суббота",
    "воскресенье",
]

UPCOMING_ADJS_SHORTS = [
    "след",
    "пред",
]

keyWords = ["послезавтра", "завтра", "неделя", "месяц", MONTH, WEEK_DAYS]


def find_key_date_noun(input):
    """
    Searches for one of key words in input

    :param input: Lemmatized Input
    :return: Index of first found date word
    """
    for i, word in enumerate(input):
        for r in keyWords:
            if isinstance(r, str) and word == r:
                return i
            elif isinstance(r, list) and word in r:
                return i
    return -1

def get_upcoming_addition(input, text_struct, date_index):
    prev = date_index - 1
    if prev >= 0 and prev < len(text_struct) \
            and 'analysis' in text_struct[prev]:
        analysis = text_struct[prev]['analysis']
        if len(analysis) > 0 and 'gr' in analysis[0]:
            origin_form_word = input[prev]
            d = analysis[0]['gr'][0:2]
            if analysis[0]['gr'].find('A') == 0:
                return origin_form_word
            elif origin_form_word in UPCOMING_ADJS_SHORTS:
                return origin_form_word
    return None


system = Mystem()
sentence = "на след, на пред, на Cледующей недели 9 января в 18:00, 9 мая"
lInput = system.lemmatize(sentence)
d = system.analyze(sentence)
print("Lemanize: %s" % lInput)
print("Data: %s" % d)

date_index = find_key_date_noun(lInput)
print("Found at: %s %s" % (get_upcoming_addition(lInput, d, date_index), lInput[date_index]))
