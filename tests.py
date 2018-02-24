import unittest
from playground import parse_time


class TestDateParser(unittest.TestCase):
    def test_simple_tomorrow_event(self):
        self.assertEqual(parse_time("#Напомнить завтра в 6 пойти на учебу"), {
            "upcoming": "завтра",
            "hour": 6
        })

    def test_simple_next_week_event(self):
        self.assertEqual(parse_time("#Напомнить на следующий недели в 9:00 пойти на учебу"), {
            "adj": "следующий",
            "upcoming": "неделя",
            "hour": 9,
            "minutes": 0
        })

    def test_simple_next_month_event(self):
        self.assertEqual(parse_time("#Напомнить на следующем месяце в 9:00 пойти на учебу"), {
            "adj": "следующий",
            "upcoming": "месяц",
            "hour": 9,
            "minutes": 0
        })

    def test_simple_weekday(self):
        self.assertEqual(parse_time("#Напомнить в понедельник в 16:45 сделать что нибудь достойное"), {
            "weekDay": "понедельник",
            "hour": 16,
            "minutes": 45
        })

    def test_simple_weekday_with_mod(self):
        self.assertEqual(parse_time("#Напомнить в следующий понедельник в 16:45 сделать что нибудь достойное"), {
            "adj": "следующий",
            "weekDay": "понедельник",
            "hour": 16,
            "minutes": 45
        })


    def test_simple_exact_time(self):
        self.assertEqual(parse_time("#Напомнить 9 октября  в 16:45 сделать что нибудь достойное"), {
            "month": "октябрь",
            "day": 9,
            "hour": 16,
            "minutes": 45
        })


if __name__ == "__main__":
    unittest.main()
