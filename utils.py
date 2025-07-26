import subprocess
import time
import os
from datetime import datetime
from pync import Notifier


def swipe_to_right():
    print('Swipe to Right')
    subprocess.run([
        'osascript', '-e',
        'tell application "System Events" to key code 124 using control down'
    ])
    time.sleep(0.3)


def swipe_to_left():
    print('Swipe to Left')
    subprocess.run([
        'osascript', '-e',
        'tell application "System Events" to key code 123 using control down'
    ])
    time.sleep(0.3)


def open_app(app, extra_script=''):
    print(f'Opening {app}')
    subprocess.run([
        'osascript', '-e',
        f'tell app "{app}" to activate {extra_script}'
    ])
    time.sleep(0.3)


def get_frontmost_app_name():
    return subprocess.run([
        'osascript', '-e',
        'tell application "System Events" to get name of first process whose frontmost is true'
    ], capture_output=True, text=True).stdout.strip()


def copy():
    print('Copying')
    subprocess.run([
        'osascript', '-e',
        'tell application "System Events" to keystroke "c" using command down'
    ])


def paste():
    print('Pasting')
    subprocess.run([
        'osascript', '-e',
        'tell application "System Events" to keystroke "v" using command down'
    ])


def screenshot():
    print('Taking Screenshot')
    subprocess.run([
        'osascript', '-e',
        f'do shell script "screencapture -i ~/Desktop/screenshot_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.png"'
    ])


def send_notif(title: str, text: str) -> None:
    Notifier.notify(text, title=title)
    time.sleep(0.3)
    play_sound()


def play_sound(sound_name='Funk.aiff'):
    os.system(f'afplay /System/Library/Sounds/{sound_name}')
