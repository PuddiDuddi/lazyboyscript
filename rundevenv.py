"""lazyboy pydev launching script"""

import re
from time import sleep
import subprocess  # nosec B404
import webbrowser
import psutil
from pyvda import VirtualDesktop
import pyautogui


class Command:
    """running commands"""

    @classmethod
    def run(cls: type, command: str) -> None:
        """Takes in a class command to run it"""
        if cls.is_process_running(command):
            print(f"{command} already running passing...")
            return  # process already running, do nothing
        if command == Command.pycharm:
            subprocess.Popen(command)  # nosec B603
            sleep(5)
        else:
            subprocess.run(command, check=False)  # nosec B603
            sleep(5)

    @classmethod
    def is_process_running(cls: type, command: str) -> bool:
        """checks if the process is already running"""
        wslexes = ["wslservice.exe", "wslrelay.exe", "wslhost.exe"]
        splitcommand = re.split(r'[\\ "]', command)
        for proc in psutil.process_iter(["pid", "name"]):
            # some system processes will not have a name
            if (
                    any(part in proc.info["name"] for part in splitcommand)
                    and len(proc.info["name"]) > 1
                    and proc.info["name"] not in wslexes
            ):
                print(proc.info["name"])
                return True
        return False

    wsl = "wt.exe wsl -d Ubuntu"
    pycharm = r"C:\Program Files\JetBrains\PyCharm Community Edition 2022.3.3\bin\pycharm64.exe"


class Browser:
    """Class for browser opening as chromium browser behave differently to other windows binaries"""

    @classmethod
    def open(cls: type, url1: str, url2: str) -> None:
        """opens url in default browser, takes in 2 urls"""
        if len(pyautogui.getWindowsWithTitle("brave")) < 1:  # pyright: ignore [reportAttributeAccessIssue]
            subprocess.run(  # nosec B603
                r'"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"'
                + " "
                + url1
                + " --new-window",
                check=False,
            )
            webbrowser.open(url2)
        else:
            print("Multiple brave.exe processes found passing...")
        sleep(2)


try:
    if VirtualDesktop.current().number == 1:
        print("Switching Vdesktop")
        VirtualDesktop(2).go()
        sleep(1)
        print("Launching Pycharm")
        Command.run(Command.pycharm)
        print("Launching wsl")
        Command.run(Command.wsl)
        print("Launching jupyter and portainer")
        Browser.open("https://portainer.local:9443", "http://127.0.0.1:666/lab")
except Exception as e:
    print(e)
    