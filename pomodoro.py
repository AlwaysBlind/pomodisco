from datetime import timedelta
from enum import Enum, unique
from time import sleep

from stopwatch import Stopwatch


@unique
class PomoStatus(Enum):
    BREAK = (timedelta(seconds=3), 1)
    POMOTIME = (timedelta(seconds=3), 2)
    LONGBREAK = (timedelta(seconds=3), 3)

    def __init__(self, session_length, _):
        self.SESSION_LENGTH = session_length


class Pomodoro:
    sets_in_a_session = 4

    def __init__(self):
        self.change_status(PomoStatus.POMOTIME)
        self.active = True
        self.n_pomos_completed = 0
        self.n_sets_completed = 0

    def start(self):
        self.stopwatch.start()

    def stop(self):
        self.stopwatch.stop()

    def get_time_left(self):
        return self.session_length - timedelta(seconds=round(self.stopwatch.duration))

    def update(self):
        time_left = self.get_time_left()
        if time_left < timedelta(0):
            self.handle_status()
            time_left = self.get_time_left()
        self.time_left = time_left

    def get_pomo_message(self):
        pomostring = f"""
        Pomo: {self.n_pomos_completed % self.sets_in_a_session + 1}/{self.sets_in_a_session}\n
        Sets completed: {self.n_sets_completed}\n
        Pomo mode: {self.status}\n
        Time left: {self.time_left}"""
        return pomostring

    def handle_status(self):
        if self.status is PomoStatus.POMOTIME:
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
        self.session_length = status.SESSION_LENGTH


if __name__ == "__main__":
    p = Pomodoro()
    # p.start()
    print(PomoStatus.BREAK is PomoStatus.LONGBREAK)
    print(PomoStatus.BREAK.SESSION_LENGTH)
    sw = Stopwatch()
    sw.start()
    while sw.duration < 60:
        sleep(1)
        p.update()
        print(p.get_pomo_message())
