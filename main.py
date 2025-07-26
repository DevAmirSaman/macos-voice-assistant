import os
import time
import threading
import pvporcupine
from pynput import keyboard
from dotenv import load_dotenv
from pvrecorder import PvRecorder

import voice_cmd_listener


load_dotenv()

ACCESS_KEY = os.getenv('ACCESS_KEY')
KEYWORD_FILE = os.getenv('KEYWORD_FILE')
IS_ASSISTANT_ACTIVE = False


def wake_word_listener():
    porcupine = pvporcupine.create(access_key=ACCESS_KEY, keyword_paths=[KEYWORD_FILE])
    recorder = PvRecorder(device_index=-1, frame_length=porcupine.frame_length)
    try:
        recorder.start()
        global IS_ASSISTANT_ACTIVE
        while True:
            if not IS_ASSISTANT_ACTIVE and porcupine.process(recorder.read()) >= 0:
                print('[Wake Word Listener] Assistant Activated')
                IS_ASSISTANT_ACTIVE = True
                voice_cmd_listener.listen_for_cmd()
                IS_ASSISTANT_ACTIVE = False
                print('[Wake Word Listener] Assistant Deactivated')

    finally:
        recorder.delete()
        porcupine.delete()


def key_listener():
    start_time = 0.0

    def on_press(key):
        nonlocal start_time
        if key == keyboard.Key.shift and not start_time:
            start_time = time.time()

    def on_release(key):
        nonlocal start_time
        if key == keyboard.Key.shift:
            global IS_ASSISTANT_ACTIVE
            if not IS_ASSISTANT_ACTIVE and time.time() - start_time >= 1.0:
                print('[Key Listener] Assistant Activated')
                IS_ASSISTANT_ACTIVE = True
                voice_cmd_listener.listen_for_cmd()
                IS_ASSISTANT_ACTIVE = False
                print('[Key Listener] Assistant Deactivated')
            start_time = 0.0

    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()


try:
    threading.Thread(target=wake_word_listener, daemon=True).start()
    key_listener()
except KeyboardInterrupt:
    pass
