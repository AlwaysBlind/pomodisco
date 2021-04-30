from datetime import timedelta
from enum import Enum, unique
from time import sleep

from stopwatch import Stopwatch

STOPPED = "==STOPPED=="


@unique
class PomoStatus(Enum):
    BREAK = (timedelta(minutes=5), 1)
    POMOTIME = (timedelta(minutes=25), 2)
    LONGBREAK = (timedelta(minutes=25), 3)

    def __init__(self, session_length, _):
        self.SESSION_LENGTH = session_length


class UpdateStatus(Enum):
    Nothing = 0
    StatusChange = 1


class Pomodoro:
    sets_in_a_session = 4

    def __init__(self):
        self.change_status(PomoStatus.POMOTIME)
        self.update()
        self.n_pomos_completed = 0
        self.n_sets_completed = 0
        self.active = False
        self.subscribers = set()

    def start(self):
        self.stopwatch.start()
        self.inactive_stopwatch = Stopwatch()
        self.inactive_stopwatch.stop()
        self.active = True

    def get_inactive_time(self):
        return timedelta(seconds=self.inactive_stopwatch.duration)

    def stop(self):
        self.stopwatch.stop()
        self.inactive_stopwatch = Stopwatch()
        self.active = False

    def get_time_left(self):
        return self.session_length - timedelta(seconds=round(self.stopwatch.duration))

    def update(self):
        status = UpdateStatus.Nothing
        time_left = self.get_time_left()
        if time_left < timedelta(0):
            self.handle_status()
            status = UpdateStatus.StatusChange
            time_left = self.get_time_left()
        self.time_left = time_left
        return status

    def get_pomo_message(self):
        invisible_string = "                       \u2062"
        pomostring = f""">>> ```\n
Pomo: {self.n_pomos_completed % self.sets_in_a_session + 1}/{self.sets_in_a_session}{invisible_string}\n
Sets completed: {self.n_sets_completed}\n
Pomo mode: {self.status}\n
Time left: {self.time_left} {"" if self.active else STOPPED }```"""
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
        self.stop()
        self.status = status
        self.session_length = status.SESSION_LENGTH


if __name__ == "__main__":
    p = Pomodoro()
    p.start()
    print(PomoStatus.BREAK is PomoStatus.LONGBREAK)
    print(PomoStatus.BREAK.SESSION_LENGTH)
    sw = Stopwatch()
    sw.start()
    while sw.duration < 60:
        sleep(1)
        p.update()
        print(p.get_pomo_message())
        print(p.get_inactive_time())
