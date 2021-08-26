#!/usr/bin/python3

import tools
from tools import time, sr
import tkinter as tk

root = tk.Tk()
root.title('Speech Recognizer')

r, m = tools.setup()

nwbw = 12 #Num Words Before Wrap

info_frame = tk.Frame(root)
info_threshold = tk.Label(info_frame, text='THRESHOLD')
info_text = tk.Label(info_frame, text='SPEECH TO TEXT')

info_threshold.grid(row=0, column=0)
info_text.grid(row=1, column=0)
info_frame.pack(side='top')

def adjust():
    global r, m, info_text
    info_text.config(text='==== Adjusting for noise, please do not speak ====')
    root.update()
    (r, m, energy_threshold) = tools.noise_adjust(5, r, m)
    info_text.config(text='SPEECH TO TEXT')
    info_threshold.config(text=str(round(energy_threshold, 4)))
    root.update()

outputwin = tk.Toplevel(root)
outputwin.title('Speech to Text')
outputtext = tk.Label(outputwin)
outputtext.pack(expand=1, fill='both')
def record():
    global r, m, info_text, outputtext
    with m as source: audio = r.listen(source)
    try:
        stime = time.time()
        value = r.recognize_google(audio)
        etime = time.time()
        time_to_recognize = round(etime-stime, 2)
        newvalue = ''
        if len(value.split()) > nwbw:
            tmp = 0
            tmp2 = ''
            for word in value.split():
                tmp2 += ' '+word
                tmp += 1
                if tmp == nwbw:
                    newvalue += tmp2.strip()+'\n'
                    tmp = 0
                    tmp2 = ''
            newvalue += tmp2
            newvalue = newvalue.strip()
        else:
            newvalue = value
        outputtext.config(text=newvalue)
        info_text.config(text='Worked ('+str(time_to_recognize)+')')
    except sr.UnknownValueError:
        info_text.config(text='(Not clear or no speech)')
    except sr.RequestError:
        info_text.config(text='==== Google Speech Recognition unreachable ====')
    root.update()
    outputwin.update()
    root.after(0, record)

button_frame = tk.Frame(root)
button_mic = tk.Button(button_frame, text='Start', command=record)
button_adjust = tk.Button(button_frame, text='Adjust for noise', command=adjust)

button_frame.pack(side='bottom')
button_mic.grid(row=0, column=0)
button_adjust.grid(row=0, column=1)

root.mainloop()