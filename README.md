
# Console - Timer
> A python-implemented linux console timer that can be paused, restarted, or exited.

- [Console - Timer](#console---timer)
- [Launch Arguments](#launch-arguments)
- [Interactive Commands](#interactive-commands)
- [Installation](#installation)
  - [Direct script run](#direct-script-run)
  - [Associate command with script](#associate-command-with-script)
  - [Add Completion sound to timer](#add-completion-sound-to-timer)
  - [Add multiple sounds](#add-multiple-sounds)

# Launch Arguments
Calling the script without arguments runs a DEFAULT session,
set on the script originally as 1 hour.  
If passed, the argument must be in the form  
* `[Xh][Ym][Zs]`   

all optional. They refer to hours, minutes, and seconds respectively.  
So for example all these are valid arguments:  
```
1h3s
1m85s
65m
10s
1h1m1s
```
If present, they must be in the correct order.  
If present, they must not be separated by spaces

# Interactive Commands
The commands are single letter key input that **must** be entered and immediatly (within the second) sent with the return (enter) key.  

The current commands are:  
* `e`: exits the timer
* `r`: restarts the timer with the initial times
* `p`: pauses and unpauses the timers

# Installation
Currently theres only one dependency: [inputimeout](https://pypi.org/project/inputimeout/)  

## Direct script run
1. Clone the repository.  
2. Install dependencies
   - **Option 1:** Install dependency directly  
    `pip install inputimeout`
   - **Option 2:** Intall through requierements    
    `pip install -r requirements.txt`
3. Run script:  
   `python3 session.py <args>`  

## Associate command with script  
On top of the previous installation, you can associate this script
with a command so you can run it from anywhere on your system.
On Linux this can be done by:  

1. Move `session.py` to a permanent known place.  
    `mv session.py /home/path/to/place/`
2. Create a runner script on bin search folder (usually `/usr/bin/`).
Name it the name of the command, for example `timer`  
`touch /usr/bin/timer`
3. Open the file and copy the launch command into runner script
```
#!/bin/bash
python3 /home/path/to/place/session.py $@
```
Now typing `timer <args>` will run the script with the same arguments.

## Add Completion sound to timer
Additionaly, if the previous steps were followed, you can add a sound to a successful run (exited by completing the timer without `Ctrl+C` or `e` command), you can add one of the following:  
```
paplay /usr/share/sounds/freedesktop/stereo/message-new-instant.oga
paplay /usr/share/sounds/freedesktop/stereo/complete.oga
spd-say "timer completed"
paplay /usr/share/sounds/freedesktop/stereo/dialog-error.oga
```
like so:  
```
#!/bin/bash
python3 /home/path/to/place/session.py $@ && paplay /usr/share/sounds/freedesktop/stereo/complete.oga
```

## Add multiple sounds
With the same trick to associate a command to the script, you can add multiple commands, like making `play_completion_sounds` to run all the paplay commands, then making the timer script be:

```
#!/bin/bash
python3 /home/path/to/place/session.py $@ && play_completion_sounds
```
