import json
from function import *
from vosk import Model, KaldiRecognizer
import pyaudio
import time
import pyttsx3
import simpleaudio as sa
from ecapture import ecapture as ec



RESPONSE_ASSISTANT = False
CONTINUE = False
METHOD_CONTINUE = ""

model = Model("my_model_big")
rec = KaldiRecognizer(model, 18000)
cap = pyaudio.PyAudio()
stream = cap.open(format=pyaudio.paInt16, channels=1, rate=18000, input=True, frames_per_buffer=8000)


def read_text_in_voice():
    stream.start_stream()
    data = stream.read(20)
    if rec.AcceptWaveform(data):
        result = json.loads(rec.Result())["text"]
        if result != "":
            return result


def nothing_method():
    wave_obj = sa.WaveObject.from_wave_file("sound/nothing.wav")
    play_obj = wave_obj.play()
    time.sleep(4.2)
    reset_rec_stream()


def sayed_assistant():
    wave_obj = sa.WaveObject.from_wave_file(SOUND_BEEP_ADDRESS)
    wave_obj.play()
    time.sleep(2.1)
    reset_rec_stream()


def reset_rec_stream():
    rec.Reset()
    stream.stop_stream()
    stream.start_stream()
def thanks(text, key, continue_method):
    wave_obj = sa.WaveObject.from_wave_file("sound/thanks.wav")
    wave_obj.play()
    time.sleep(2.1)
    reset_rec_stream()

def start_assistant(text):
    data = sqlite_query('SELECT * FROM start_name;')
    for row in data:
        if row[1] in text:
            sayed_assistant()
            global RESPONSE_ASSISTANT
            RESPONSE_ASSISTANT = True
            break
def who_are_you(text, key, continue_method):
    wave_obj = sa.WaveObject.from_wave_file("sound/presentation.wav")
    wave_obj.play()
    time.sleep(2.1)
    reset_rec_stream()

def math_assistant(text, key, continue_method):
    global CONTINUE, METHOD_CONTINUE
    wave_obj = sa.WaveObject.from_wave_file('sound/solve_math.wav')
    wave_obj.play()
    CONTINUE = True
    METHOD_CONTINUE = continue_method
    time.sleep(4.1)
    reset_rec_stream()

def take_picture(text, key, continue_method):
    wave_obj = sa.WaveObject.from_wave_file("sound/take_picture.wav")
    wave_obj.play()
    time.sleep(5)
    ec.capture(0, "test", "img.jpg")
    reset_rec_stream()

def solve_math(text):
    global CONTINUE, METHOD_CONTINUE
    str = text
    data_math = sqlite_query('SELECT * FROM math order by id DESC ;')
    for row in data_math:
        str = str.replace(row[1], row[2])

    data_alphabet = sqlite_query('SELECT * FROM alphabet;')
    str = str.replace(" ", "")
    for row in data_alphabet:
        str = str.replace(row[1], "")
    try:
        print(str)
        print(eval_math(str))
    except:
        nothing_method()
    CONTINUE = False
    METHOD_CONTINUE = ""


def response_assistant(text):
    global RESPONSE_ASSISTANT
    data = sqlite_query('SELECT * FROM response_assistant;')
    data1 = sqlite_query('SELECT * FROM response_assistant;')
    count = len(data1.fetchall()) - 1
    for i, row in enumerate(data):
        if row[1] in text:
            func = globals()[row[2]]
            func(text, row[1], row[3])
            break
        else:
            if count == i:
                nothing_method()

    RESPONSE_ASSISTANT = False
def eval_math(text_math):
    new_data = re.split(", |-|/|\+", text_math)
    for i, row in enumerate(new_data):
        if '&&&' in row:
            text=row
            text=text.replace('&&&','')
            reshe=text.split('&&')[1]
            text=text.replace(reshe,'')
            text=text.replace('&&','**(1/'+reshe+')')
            text_math=text_math.replace(row,text)
    return eval(text_math)

print('بگویید هی سینا یا سینا یا ...')
while True:
    try:
        text = read_text_in_voice()
    except:
        model = Model("my_model")
        rec = KaldiRecognizer(model, 18000)
        cap = pyaudio.PyAudio()
        stream = cap.open(format=pyaudio.paInt16, channels=1, rate=18000, input=True, frames_per_buffer=4000)

    if text != None:
        print(text)
        if RESPONSE_ASSISTANT == True:
            response_assistant(text)
        else:
            if CONTINUE == False:
                start_assistant(text)
            else:
                method = globals()[METHOD_CONTINUE]
                method(text)

