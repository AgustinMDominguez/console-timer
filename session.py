import os
import sys
import tty
import time
import stopit
import ctypes
import termios
import threading
import multiprocessing
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
        # self.key_listener_th = multiprocessing.Process(target=self.handle_keys)
        self.key_listener_th = threading.Thread(target=self.handle_keys)
        self.mapped_keys = {
            'p': self.pause,
            'r': self.reset,
            'e': self.end
        }

    def run(self):
        try:
            self.timer_th.start()
            self.key_listener_th.start()
            self.timer_th.join()
            print("Killing?")
            kill_thread(self.key_listener_th)
            self.key_listener_th.join()
            print("Killed :D")
        except KeyboardInterrupt:
            self.should_run = False
        os.system(CLEAR_SCREEN_CMD)
        print()
        if self.remaining_seconds != 0:
            sys.exit(1)

    def run_timer(self):
        while self.should_run and self.remaining_seconds > 0:
            self.update_screen()
            time.sleep(1)
            if not self.paused:
                with self.counter_lock:
                    self.remaining_seconds -= 1
        self.should_run = False

    def update_screen(self):
        os.system(CLEAR_SCREEN_CMD)
        timer_str = human_readable(self.remaining_seconds)
        print(f" > {timer_str} <")

    def handle_keys(self):
        while self.should_run:
            try:
                pressed_key = self.get_key()
                handle_func = self.mapped_keys[pressed_key]
                handle_func()
                pass
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

    @staticmethod
    def get_key():
        with stopit.ThreadingTimeout(1) as to_ctx_mgr:
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(fd)
                ch = sys.stdin.read(1)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        if to_ctx_mgr.state == to_ctx_mgr.EXECUTED:
            return ch
        else:
            return '0'


def kill_thread(thread):
    thread_id = thread.ident
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, ctypes.py_object(SystemExit))
    if res > 1:
        ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
        print('Exception raise failure')


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


def timer():
    pass

if __name__ == "__main__":
    total_seconds = get_total_seconds(sys.argv)
    timer = Timer(total_seconds)
    timer.run()
