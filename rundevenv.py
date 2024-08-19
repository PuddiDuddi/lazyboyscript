import subprocess
import webbrowser
import psutil
from pyvda import VirtualDesktop
from time import sleep
import pyautogui
import re


class Command:

    @classmethod
    def run(cls, command):
        if cls.is_process_running(command):
            print(f"{command} already running passing...")
            return  # process already running, do nothing
        if command == Command.pycharm:
            subprocess.Popen(command)
            sleep(5)
        else:
            subprocess.run(command)
            sleep(5)

    @classmethod
    def is_process_running(cls, command):
        wslexes = ['wslservice.exe', 'wslrelay.exe', 'wslhost.exe']
        splitcommand = re.split(r'[\\ "]', command)
        for proc in psutil.process_iter(['pid', 'name']):
            # some system processes will not have a name
            if any(part in proc.info['name'] for part in splitcommand) and len(proc.info['name']) > 1\
                    and proc.info['name'] not in wslexes:
                print(proc.info['name'])
                return True
        return False


    wsl = "wt.exe wsl -d Ubuntu"
    pycharm = r"C:\Program Files\JetBrains\PyCharm Community Edition 2022.3.3\bin\pycharm64.exe"


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
        print('Switching Vdesktop')
        VirtualDesktop(2).go()
        sleep(1)
        print('Launching Pycharm')
        Command.run(Command.pycharm)
        print('Launching wsl')
        Command.run(Command.wsl)
        print('Launching jupyter and portainer')
        Browser.open("https://portainer.local:9443","http://127.0.0.1:666/lab")
except Exception as e:
    print(e)