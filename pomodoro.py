from datetime import timedelta
from enum import Enum
from time import sleep

from stopwatch import Stopwatch


class PomoStatus(Enum):
    BREAK = 1
    POMOTIME = 2
    LONGBREAK = 3


class Pomodoro:
    sets_in_a_session = 4
    SESSION_LENGTHS = {
        PomoStatus.POMOTIME: timedelta(seconds=3),
        PomoStatus.BREAK: timedelta(seconds=3),
        PomoStatus.LONGBREAK: timedelta(seconds=5),
    }

    def __init__(self):
        self.change_status(PomoStatus.POMOTIME)
        self.active = True
        self.n_pomos_completed = 0
        self.n_sets_completed = 0

    def start(self):
        self.stopwatch.start()

    def stop(self):
        self.stopwatch.stop()

    def _time_left(self):
        return self.session_length - timedelta(seconds=round(self.stopwatch.duration))

    def update(self):
        tl = self._time_left()
        if tl < timedelta(0):
            self.handle_status()
            tl = self._time_left()
        self.time_left = tl

    def get_pomo_message(self):
        pomostring = f"""
        Pomo: {self.n_pomos_completed % self.sets_in_a_session + 1}/{self.sets_in_a_session}\n
        Sets completed: {self.n_sets_completed}\n
        Pomo mode: {self.status}\n
        Time left: {self._time_left()}"""
        return pomostring

    def handle_status(self):
        if self.status == PomoStatus.POMOTIME:
            self.n_pomos_completed += 1
            if self.n_pomos_completed % self.sets_in_a_session == 0:
                self.n_sets_completed += 1
                self.change_status(PomoStatus.LONGBREAK)
            else:
                self.change_status(PomoStatus.BREAK)
        else:
            self.change_status(PomoStatus.POMOTIME)

    def change_status(self, status):
        self.stopwatch = Stopwatch()
        self.status = status
        self.session_length = self.SESSION_LENGTHS[status]


if __name__ == "__main__":
    p = Pomodoro()
    p.start()
    sw = Stopwatch()
    sw.start()
    while sw.duration < 60:
        sleep(1)
        p.update()
        print(p.get_pomo_message())
