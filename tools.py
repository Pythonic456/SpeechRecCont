#!/usr/bin/python3

import speech_recognition as sr
import time

def setup():
    print('===== IGNORE FOLLOWING WARNINGS =====')
    time.sleep(2)
    r = sr.Recognizer()
    m = sr.Microphone()
    print('===== WARNINGS FINISHED =====')
    return r, m

def noise_adjust(noise_adjust_time, r, m):
    print("Adjusting to noise, do not speak please...")
    for i in range(noise_adjust_time):
        with m as source: r.adjust_for_ambient_noise(source)
    return r, m, r.energy_threshold
