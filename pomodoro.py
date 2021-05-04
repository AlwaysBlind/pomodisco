from datetime import timedelta
from enum import Enum, unique
from time import sleep

from stopwatch import Stopwatch

STOPPED = "==STOPPED=="


@unique
class PomoStatus(Enum):
    BREAK = 3
    POMOTIME = 2
    LONGBREAK = 1


class UpdateStatus(Enum):
    Nothing = 0
    StatusChange = 1


class Pomodoro:
    status_states = dict()

    def __init__(self, break_length=timedelta(minutes=5), pomo_length=timedelta(minutes=25),long_break=timedelta(minutes=25),sets_in_a_session=4):
        self.status_states[PomoStatus.BREAK]= break_length
        self.status_states[PomoStatus.POMOTIME]= pomo_length
        self.status_states[PomoStatus.LONGBREAK]= long_break
        self.change_status(PomoStatus.POMOTIME)
        self.update()
        self.n_pomos_completed = 0
        self.n_sets_completed = 0
        self.active = False
        self.subscribers = set()
        self.sets_in_a_session = sets_in_a_session

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
        return self.session_length() - timedelta(seconds=round(self.stopwatch.duration))
    def session_length(self):
        return self.status_states[self.status]

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

    @classmethod
    def get_heavy_pomo(cls):
        return cls(short_length=timedelta(minutes=8), long_length=timedelta(minutes=20),pomo_length=timedelta(minutes=50), sets_in_a_session=3)
        


if __name__ == "__main__":
    p = Pomodoro()
    p.start()
    print(PomoStatus.BREAK is PomoStatus.LONGBREAK)
    print(p.session_length())
    sw = Stopwatch()
    sw.start()
    while sw.duration < 60:
        sleep(1)
        p.update()
        print(p.get_pomo_message())
        print(p.get_inactive_time())
