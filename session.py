import os
import sys
from math import floor

from inputimeout import inputimeout, TimeoutOccurred

DEFAULT_SESSION = "1h"
CLEAR_SCREEN_CMD = "cls" if os.name == "nt" else "clear"
ARGUMENT_KEYS = [
    ("hours", "h", 60*60),
    ("minutes", "m", 60),
    ("seconds", "s", 1)
]


class Timer():
    def __init__(self, total_seconds):
        self.initial_seconds = total_seconds
        self.remaining_seconds = total_seconds
        self.paused = False
        self.should_run = True
        self.mapped_keys = {
            'p': self.pause,
            'r': self.restart,
            'e': self.end,
            '0': self.passf
        }

    def run(self):
        while self.should_run and self.remaining_seconds > 0:
            self.update_screen()
            key = self.get_key()
            if not self.paused:
                self.remaining_seconds -= 1
            try:
                handle_func = self.mapped_keys[key]
                handle_func()
            except KeyError:
                pass

    def pause(self)-> None:
        self.paused = not self.paused

    def restart(self)-> None:
        self.remaining_seconds = self.initial_seconds

    def end(self)-> None:
        self.should_run = False

    def passf(self)-> None:
        pass

    def update_screen(self):
        os.system(CLEAR_SCREEN_CMD)
        timer_str = human_readable(self.remaining_seconds)
        print(f" > {timer_str} <")

    @staticmethod
    def get_key()-> str:
        try:
            key = inputimeout(prompt="command >  ", timeout=1)
        except TimeoutOccurred:
            key = '0'
        return key


def parse_time(st):
    time_dic = {}
    for key in ARGUMENT_KEYS:
        time_dic[key[0]] = 0
        spl = st.split(key[1])
        if len(spl) == 2:
            time_dic[key[0]] = int(spl[0])
            st = spl[1]
    return time_dic


def human_readable(total_seconds):
    hours = floor(total_seconds/(60*60))
    st = ''
    if hours > 0:
        total_seconds = total_seconds % (60*60)
        st += str(hours).zfill(2) + ":"
    minutes = floor(total_seconds/60)
    if minutes > 0:
        total_seconds = total_seconds % (60)
    if hours > 0 or minutes > 0:
        st += str(minutes).zfill(2) + ":"
    st += str(total_seconds).zfill(2)
    return st


def get_total_seconds(argv):
    time_input = argv[1] if (len(argv) > 1) else DEFAULT_SESSION
    parsed_time = parse_time(time_input)
    total_seconds = 0
    for key in ARGUMENT_KEYS:
        total_seconds += parsed_time[key[0]] * key[2]
    return total_seconds


if __name__ == "__main__":
    total_seconds = get_total_seconds(sys.argv)
    timer = Timer(total_seconds)
    timer.run()
