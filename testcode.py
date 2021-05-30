from os import getpid
from multiprocessing import Process
import psutil
from time import sleep


def kill_tree(pid):
    parent = psutil.Process(pid)
    for child in parent.children(recursive=True):
        child.kill()


def remaining_time(current_time, delay):
    sleep(delay)
    print(current_time, "secs remain")


def battle():
    print("In 10 seconds, this program will explode lol")
    x = 10
    while x > 0:
        remaining_time(x, 2)
        x = x-2
    print("Program has exploded!")


def stop_battle():
    while True:
        print("Welcome to the anti program explody program. Type 1 to stop the explosion.")
        usrinput = input("usr: ")
        if usrinput == "1":
            print("Killing process...")
            pid = getpid()
            kill_tree(pid)
            print("Process killed!")
            print("Waiting to see if anything happens...")
            sleep(5)
            print("Nope I think we're good!")
            break
        else:
            print("Invalid command!")


def main():
    p1 = Process(target=battle(),)
    p2 = Process(target=stop_battle(),)
    p1.start()
    p2.start()


if __name__ == "__main__":
    print("Starting main")
    main()
    print("Stopping main")
