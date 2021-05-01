import os
import sys
import time
import keyboard
import threading
from math import floor

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
        self.control_lock = threading.Lock()
        self.counter_lock = threading.Lock()
        self.timer_th = threading.Thread(target=self.run_timer)
        self.key_listener_th = threading.Thread(target=self.handle_keys)
        self.mapped_keys = {
            'p': self.pause,
            'r': self.reset,
            'esc': self.end
        }

    def run(self):
        try:
            self.timer_th.start()
            self.key_listener_th.start()
            self.timer_th.join()
            self.key_listener_th.join()
        except KeyboardInterrupt:
            self.should_run = False
        if self.remaining_seconds != 0:
            sys.exit(1)

    def run_timer(self):
        while self.should_run and self.remaining_seconds > 0:
            self.update_screen()
            time.sleep(1)
            if not self.paused:
                with self.counter_lock:
                    self.remaining_seconds -= 1
        with self.control_lock:
            self.should_run = False
        print("Ending??")
        print(self.should_run)

    def update_screen(self):
        os.system(CLEAR_SCREEN_CMD)
        print(human_readable(self.remaining_seconds))

    def handle_keys(self):
        while self.should_run:
            event = keyboard.read_event()
            event_type = event.event_type
            pressed_key = event.name
            del event
            if event_type == "down":
                try:
                    handle_func = self.mapped_keys[pressed_key]
                    handle_func()
                except KeyError:
                    pass

    def pause(self):
        with self.control_lock:
            self.paused = not self.paused

    def reset(self):
        with self.control_lock:
            self.paused = False
        with self.counter_lock:
            self.remaining_seconds = self.initial_seconds

    def end(self):
        with self.control_lock:
            self.should_run = False


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


def main():
    if len(sys.argv) > 1:
        time_input = parse_time(sys.argv[1])
    else:
        time_input = parse_time(DEFAULT_SESSION)
    total_seconds = 0
    for key in ARGUMENT_KEYS:
        total_seconds += time_input[key[0]] * key[2]
    timer = Timer(total_seconds)
    timer.run()


if __name__ == "__main__":
    main()
