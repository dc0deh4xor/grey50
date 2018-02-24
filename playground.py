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

TIME_SEPARATOR_CHARS = [' ', ':']

DATE_KEY_WORDS = ["послезавтра", "завтра", "неделя", "месяц", WEEK_DAYS, MONTH]

system = Mystem()


def find_key_date_noun(input):
    """
    Searches for one of key words in input

    :param input: Lemmatized Input
    :return: Index of first found date word
    """
    for i, word in enumerate(input):
        for kI, r in enumerate(DATE_KEY_WORDS):
            if isinstance(r, str) and word == r:
                return i, kI, word
            elif isinstance(r, list) and word in r:
                return i, kI, word
    return -1


def get_grammar(text_struct, index):
    if 0 <= index < len(text_struct) and "analysis" in text_struct[index]:
        analysis = text_struct[index]['analysis']
        if len(analysis) > 0 and 'gr' in analysis[0]:
            return analysis[0]['gr']

    return None


def get_time(input, text_struct, date_index):
    def get_next(index):
        while index >= 0:
            if not 'analysis' in text_struct[index]:
                index = index + 1
            else:
                break
        return index

    next = get_next(date_index + 1)

    while next < len(input):
        grammar = get_grammar(text_struct, next)

        if grammar is not None and grammar[0:2] == "PR":
            next = next + 1
            _time = []
            while next < len(input):
                if not input[next] in TIME_SEPARATOR_CHARS:
                    try:
                        _time.append(int(input[next]))
                    except ValueError:
                        break
                next = next + 1
            return _time
        else:
            next = get_next(next + 1)

    return None


def get_upcoming_addition(input, text_struct, date_index):
    """
    Searches for adjective modifers of date

    :param input: Lemmatized Input
    :param text_struct: Analyzed Input
    :param date_index: Index of date keyword
    :return:
    """
    prev = date_index - 1

    while prev >= 0:
        if not 'analysis' in text_struct[prev]:
            prev = prev - 1
        else:
            break

    grammar = get_grammar(text_struct, prev)
    if grammar is not None:
        grammar = grammar[0:2]
        origin_form_word = input[prev]
        if grammar == 'A,' or grammar == "A=":
            return origin_form_word
        elif origin_form_word in UPCOMING_ADJS_SHORTS:
            return origin_form_word

    return None


def parse_time(sentence):
    lInput = system.lemmatize(sentence)
    d = system.analyze(sentence)

    date_index, kWindex, value = find_key_date_noun(lInput)
    time = get_time(lInput, d, date_index)

    time_obj = {}

    if time != None and len(time) > 0:
        time_obj["hour"] = time[0]
        if len(time) > 1:
            time_obj["minutes"] = time[1]

    if kWindex == 4:
        time_obj["weekDay"] = value
    elif kWindex == 5:
        time_obj["month"] = value
    else:
        time_obj["upcoming"] = value

    time_obj["adj"] = get_upcoming_addition(lInput, d, date_index)

    return time_obj


sentence = "на след, на пред, на Cледующей недели 9 января в 18:00, 9 мая"
print("Found at: %s" % dumps(parse_time(sentence), indent=2, ensure_ascii=False))
