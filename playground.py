from pymystem3 import Mystem
import arrow

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

MONTH_MAP = {
    "январь": 0,
    "февраль": 1,

    "март": 2,
    "апрель": 3,
    "май": 4,

    "июнь": 5,
    "июль": 6,
    "август": 7,

    "сентябрь": 8,
    "октябрь": 9,
    "ноябрь": 10,

    "декабрь": 11,
}

WEEKDAYS_MAP = {
    "понедельник": 0,
    "вторник": 1,
    "среда": 2,
    "четверг": 3,
    "пятница": 4,
    "суббота": 5,
    "воскресенье": 6,
}

UPCOMING_MAP = {
    "след": 1,
    "следующий": 1,
    "пред": -1,
    "предыдущий": -1,
}

DAY_MAP = {
    "сегодня": 0,
    "завтра": 1,
    "послезавтра": 2,
    "неделя": 7,
    "месяц": 31,
}

TIME_SEPARATOR_CHARS = [' ', ':']

DATE_KEY_WORDS = ["сегодня", "послезавтра", "завтра", "неделя", "месяц", WEEK_DAYS, MONTH]

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


def get_date(input, text_struct, date_index):
    prev = date_index - 1
    while prev >= 0:
        if len(input[prev]) > 0 and input[prev] != ' ':
            try:
                return int(input[prev])
            except ValueError:
                break
        prev = prev - 1
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

        if grammar is not None and (grammar[0:2] == "PR" or input[next] == "в"):
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


def parse_place(input, text_struct):
    def get_next(index):
        while index >= 0:
            if not 'analysis' in text_struct[index]:
                index = index + 1
            else:
                break
        return index


    next = get_next(0)
    place_preps = ["в", "на", "с"]

    while next < len(input):
        grammar = get_grammar(text_struct, next)

        if grammar is not None and (grammar[0:2] == "PR" or input[next] in place_preps):
            place = []
            next = next + 1

            if input[next] != " (":
                continue

            next = next + 1
            while next < len(input) and input[next] != ") " and input[next] != ")\n":
                place.append(text_struct[next]['text'])
                next = next + 1

            return ' '.join(place)
        else:
            next = get_next(next + 1)

    return None


def parse(sentence, test_mode=False):
    lInput = system.lemmatize(sentence)
    d = system.analyze(sentence)

    date_index, kWindex, value = find_key_date_noun(lInput)
    time = get_time(lInput, d, date_index)

    time_obj = {}
    date = arrow.utcnow()

    if time != None and len(time) > 0:
        time_obj["hour"] = time[0]
        date = date.replace(hour=time[0])
        if len(time) > 1:
            time_obj["minutes"] = time[1]
            date = date.replace(minute=time[1])

    adj = get_upcoming_addition(lInput, d, date_index)
    if adj is not None:
        time_obj["adj"] = adj

    if kWindex == 5:
        time_obj["weekDay"] = value
        date = date.shift(weekday=abs(WEEKDAYS_MAP[value] - date.weekday()))
    elif kWindex == 6:
        time_obj["month"] = value
        time_obj["day"] = day = get_date(lInput, d, date_index)
        date = date.replace(month=MONTH_MAP[value], day=day)
    else:
        time_obj["upcoming"] = value
        date = date.shift(days=DAY_MAP[value])

    return date.timestamp, time_obj, parse_place(lInput, d)
