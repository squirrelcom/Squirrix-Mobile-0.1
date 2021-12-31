#!/usr/bin/python3

# Shell prototype
from lib.core import *
import pyttsx3

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def talk(text):
    engine.say(text)
    engine.runAndWait()


# The code segment below is for
# setting up the path in android

# Generally it should be in this path
P = 'sdcard/com.hipipal.qpyplus/projects3/shell'
try:
    os.chdir(P)
except OSError:
    pass


def main():
    s = shell()
    s.start()


if __name__ == '__main__':
    main()
