from time import sleep
import curses


def start_curses():
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)
    return stdscr


def stop_curses(stdscr):
    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()

try:
    stdscr = start_curses()
    stdscr.addstr("Pretty text")
    stdscr.refresh()
    # sleep(10)
    presed_key = stdscr.getkey()
    stop_curses(stdscr)
except Exception as e:
    stop_curses(stdscr)
    raise e

print(presed_key)