from datetime import timedelta
from stopwatch import Stopwatch
from time import sleep
import math
class Pomodoro:
    def __init__(self):
        self.pomo_length = timedelta(minutes=25)
        self.stopwatch = Stopwatch()
        self.active = True

    def start(self):
        self.stopwatch.start()

    def stop(self):
        self.stopwatch.stop()

    def time_left(self):
        return self.pomo_length - timedelta(seconds=round(self.stopwatch.duration))

    
        

if __name__ == "__main__":
    p = Pomodoro()
    p.start()
    sleep(2)
    print(p.time_left())
    p.stop()
    sleep(2)
    print(p.time_left())
