import unittest
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

    
if __name__ == "__main__":
    unittest.main()