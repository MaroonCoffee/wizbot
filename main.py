from os import getpid
from multiprocessing import Process
import psutil
import empower_collection


def kill_tree(pid):
    parent = psutil.Process(pid)
    for child in parent.children(recursive=True):
        child.kill()


def battle_loop():
    battle_process = Process(target=empower_collection.battle())
