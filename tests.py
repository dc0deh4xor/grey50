import unittest
from playground import parse


class TestPlaceParser(unittest.TestCase):
    def test_simple_place(self):
        _,_,place = parse("#напомнить сегодня в 6 на (ойбеке)")
        self.assertEqual(place, "ойбеке")

    def test_simple_place_add(self):
        _, _, place = parse("#напомнить сегодня в 6 на (ойбеке) метро")
        self.assertEqual(place, "ойбеке")

class TestDateParser(unittest.TestCase):

    def test_simple_tomorrow_event(self):
        self.assertEqual(parse("#Напомнить завтра в 6 пойти на учебу", test_mode=True), {
            "upcoming": "завтра",
            "hour": 6
        })

    def test_simple_next_week_event(self):
        self.assertEqual(parse("#Напомнить на следующий недели в 9:00 пойти на учебу", test_mode=True), {
            "adj": "следующий",
            "upcoming": "неделя",
            "hour": 9,
            "minutes": 0
        })

    def test_simple_next_month_event(self):
        self.assertEqual(parse("#Напомнить на следующем месяце в 9:00 пойти на учебу", test_mode=True), {
            "adj": "следующий",
            "upcoming": "месяц",
            "hour": 9,
            "minutes": 0
        })

    def test_simple_weekday(self):
        self.assertEqual(parse("#Напомнить в понедельник в 16:45 сделать что нибудь достойное", test_mode=True), {
            "weekDay": "понедельник",
            "hour": 16,
            "minutes": 45
        })

    def test_simple_weekday_with_mod(self):
        self.assertEqual(
            parse("#Напомнить в следующий понедельник в 16:45 сделать что нибудь достойное", test_mode=True), {
                "adj": "следующий",
                "weekDay": "понедельник",
                "hour": 16,
                "minutes": 45
            })

    def test_simple_exact_time(self):
        self.assertEqual(parse("#Напомнить 9 октября  в 16:45 сделать что нибудь достойное", test_mode=True), {
            "month": "октябрь",
            "day": 9,
            "hour": 16,
            "minutes": 45
        })


if __name__ == "__main__":
    unittest.main()
