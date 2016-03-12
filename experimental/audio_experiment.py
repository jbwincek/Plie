import speech_recognition as sr

with open('wit_key', 'r') as key_file:
    KEY = key_file.read().strip()


def handle_audio():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio_data = recognizer.listen(source)
    print('listening...')
    response = recognizer.recognize_wit(audio_data, KEY, show_all=True)
    print('got: {}'.format(response))

handle_audio()

