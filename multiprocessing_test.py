from os import getppid
from multiprocessing import Process
import psutil
from time import sleep


def kill_tree(ppid):
    parent = psutil.Process(ppid)
    for child in parent.children(recursive=True):
        child.kill()


def battle():
    print("The second message in this function won't be able to run, as it will have ended before then")
    sleep(5)
    print("This text will not be displayed, as the function will have already terminated")


def stop_battle():
    sleep(1)
    print("This text is from a separate function that will end itself and the previous function")
    print("Killing processes...")
    ppid = getppid()
    kill_tree(ppid)
    print("This text will not be displayed, as the function will have already terminated")


if __name__ == "__main__":
    p1 = Process(target=battle)
    p2 = Process(target=stop_battle)
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    print("Both processes completed!")
