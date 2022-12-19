import sqlite3
from variables import *
import simpleaudio as sa
import pyttsx3
import time
import re

con = sqlite3.connect(CONNECTION_ADDRESS)

engine = pyttsx3.init()


def reading_text(text):
    engine.setProperty('rate', 140)
    engine.save_to_file(text, ADDRESS_RESPONSE_ASSISTANT)
    engine.runAndWait()
    wave_obj = sa.WaveObject.from_wave_file(ADDRESS_RESPONSE_ASSISTANT)
    play_obj = wave_obj.play()


def sqlite_query(query):
    cur = con.cursor()
    data = cur.execute(query)
    return data


def play_sound(path):
    wave_obj = sa.WaveObject.from_wave_file(path)
    play_obj = wave_obj.play()


def search_browser(text, key, continue_method):
    text = text.replace(key, '')
    url = "https://www.google.com/search?client=firefox-b-d&q=" + text
    import webbrowser as wb
    wb.open_new_tab(url)
    play_sound('sound\opening.wav')






