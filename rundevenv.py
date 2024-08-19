import subprocess
import webbrowser
import psutil
from pyvda import VirtualDesktop
from time import sleep
import pyautogui


class Command:

    @classmethod
    def run(cls, command):
        if cls.is_process_running(command):
            print(f"{command} already running passing...")
            pass  # process already running, do nothing
        else:
            subprocess.run(command, shell=True)
            sleep(10)

    @classmethod
    def is_process_running(cls, command):
        for proc in psutil.process_iter(['pid', 'name']):
            if str(proc.info['name']) in str(command):
                return True
        return False

    wsl = "wt.exe wsl -d Ubuntu"
    pycharm = r'"C:\Program Files\JetBrains\PyCharm Community Edition 2022.3.3\bin\pycharm64.exe"'


class Browser:

    @classmethod
    def open(cls, url1, url2):
        if len(pyautogui.getWindowsWithTitle("brave")) == 1:
            subprocess.run(r'"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"' + ' ' + url1 +
                           ' --new-window', shell=True)
            webbrowser.open(url2)
        else:
            print('Multiple brave.exe processes found passing...')
        sleep(2)


try:
    if VirtualDesktop.current().number == 1:
        VirtualDesktop(2).go()
        sleep(1)
        Command.run(Command.pycharm)
        Command.run(Command.wsl)
        Browser.open("https://portainer.local:9443","http://127.0.0.1:666/lab")
except Exception as e:
    print(e)

