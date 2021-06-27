from os import getpid
from multiprocessing import Process
import psutil
import empower_collection
import ahk


ahk = ahk.AHK()


def kill_tree(pid):
    parent = psutil.Process(pid)
    for child in parent.children(recursive=True):
        child.kill()


def battle_loop():
    battle_process = Process(target=empower_collection.battle())


def main():
    empower_collection.card_handler()


if __name__ == "__main__":
    main()
