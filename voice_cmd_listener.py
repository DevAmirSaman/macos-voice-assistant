import speech_recognition as sr

from utils import send_notif, get_frontmost_app_name
from cmd_list import CMD_MAP, APPS


def listen_for_cmd():
    recognizer = sr.Recognizer()
    search_on_firefox = False
    activity_lvl = 10

    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        send_notif(title='دستیار صوتی', text='🎙در حال شنیدن دستورات...')

        while activity_lvl > 0:
            try:
                if search_on_firefox and get_frontmost_app_name() == 'firefox':
                    recognizer.pause_threshold = 2.0
                    recognizer.phrase_threshold = 1.5
                else:
                    recognizer.pause_threshold = 0.8
                    recognizer.phrase_threshold = 0.3

                audio = recognizer.listen(source, timeout=8)
                phrase = recognizer.recognize_google(audio, language='fa-IR')

                if phrase == 'خاموش':
                    break

                elif phrase in APPS:
                    activity_lvl += 1
                    if APPS[phrase] == 'firefox':
                        search_on_firefox = True
                    CMD_MAP['app'](app=APPS[phrase])

                elif phrase in CMD_MAP:
                    activity_lvl += 1
                    CMD_MAP[phrase]()

                elif search_on_firefox:
                    activity_lvl += 1
                    CMD_MAP['app'](
                        app='firefox',
                        extra_script=f'open location "https://www.google.com/search?q={phrase}"'
                    )
                    search_on_firefox = False

                else:
                    activity_lvl -= 1
                print(f'Detected phrase: {phrase}')

            except sr.WaitTimeoutError:
                activity_lvl -= 2
                print('Timeout! No speech detected')

            except sr.UnknownValueError:
                activity_lvl -= 1
                print('Google Speech Recognition could not understand audio')

            except sr.RequestError as e:
                activity_lvl = 0
                print(f'An error occurred when requesting audio: {e}')

            except Exception as e:
                activity_lvl -= 1
                print(f'An error occurred when processing audio: {e}')

    send_notif(title='Voice Assistant', text='BYE BYE!!!')
