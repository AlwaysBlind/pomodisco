import unittest
from time import sleep
from datetime import timedelta
from pomodoro import PomoStatus, Pomodoro

class TestPomodoroMethods(unittest.TestCase):
    def test_time_left_pomotime(self):
        self.assert_status(PomoStatus.POMOTIME)

    def test_time_left_longbreak(self):
        self.assert_status(PomoStatus.LONGBREAK)

    def test_time_left_break(self):
        self.assert_status(PomoStatus.BREAK)

    def assert_status(self, status):
        p = Pomodoro()
        p.change_status(status)
        self.assertEqual(p.get_time_left(), status.SESSION_LENGTH)

    def test_inactive_time(self):
        p = Pomodoro()
        sleep(0.5)
        self.assertTrue(p.get_inactive_time() >= timedelta(seconds=0.5))
        sleep(0.5)
        self.assertTrue(p.get_inactive_time() >= timedelta(seconds=1))

    def test_inactive_time_resets(self):
        p = Pomodoro()
        sleep(1)
        p.start()
        self.assertTrue(p.get_inactive_time() <= timedelta(seconds=0.1))


    
if __name__ == "__main__":
    unittest.main()
