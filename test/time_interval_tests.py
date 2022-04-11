from datetime import datetime
import string
from unittest import TestCase

from hydroplantly.time_interval import TimeInterval


class TestTimeInterval(TestCase):

    def testToString(self):
        t = TimeInterval(10, 00, 17, 30)
        self.assertEqual(str(t), '10:00 - 17:30')
        t = TimeInterval(7, 1, 23, 10)
        self.assertEqual(str(t), '07:01 - 23:10')
        t = TimeInterval(0, 0, 8, 3)
        self.assertEqual(str(t), '00:00 - 08:03')

    def testEqual(self):
        a = TimeInterval(0, 0, 8, 3)
        b = TimeInterval(0, 0, 8, 3)
        self.assertEqual(a, b)

    def testParseFromTime(self):
        t = TimeInterval.from_time("00:00", "08:05")
        self.assertEqual(TimeInterval(0, 0, 8, 5), t)
        t = TimeInterval.from_time(start="00:01", end="09:05")
        self.assertEqual(TimeInterval(0, 1, 9, 5), t)

    def testIsInDatetime(self):
        t = TimeInterval.from_time("10:00", "17:00")

        dt = datetime.fromisoformat('2022-10-30 12:00')
        self.assertTrue(t.isInDatetime(dt))

        dt = datetime.fromisoformat('2022-10-30 10:00')
        self.assertTrue(t.isInDatetime(dt))
        dt = datetime.fromisoformat('2022-10-30 16:59:59')
        self.assertTrue(t.isInDatetime(dt))

        dt = datetime.fromisoformat('2022-10-30 08:00')
        self.assertFalse(t.isInDatetime(dt))

        t = TimeInterval.from_time("17:00", "02:00")
        dt = datetime.fromisoformat('2022-10-31 23:00')
        self.assertTrue(t.isInDatetime(dt))
        dt = datetime.fromisoformat('2022-10-31 01:00')
        self.assertTrue(t.isInDatetime(dt))

        dt = datetime.fromisoformat('2022-10-31 02:00')
        self.assertFalse(t.isInDatetime(dt))

        dt = datetime.fromisoformat('2022-10-31 16:59')
        self.assertFalse(t.isInDatetime(dt))
