import os
import subprocess
import sys
from pathlib import Path
from time import sleep



def start():
    p = subprocess.Popen([sys.executable, 'run.py'],
                         stdout=open('output.log', 'a'),
                         stderr=open('error.log', 'a'))

if __name__ == "__main__":
    if os.path.exists('.pid'):
        Path('.need_shutdown').touch()
    while os.path.exists('.pid'):
        sleep(2)
    start()
