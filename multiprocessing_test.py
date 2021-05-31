from multiprocessing import Process, Queue
from time import sleep


def battle():
    print("The second message in this function won't be able to run, as it will have ended before then")
    sleep(10)
    print("This text will not be displayed, as the function will have already terminated")


def stop_battle(error_channel):
    sleep(1)
    print("This text is from a separate function that will end itself and the previous function")
    sleep(5)
    print("Killing processes...")
    error_channel.put(100)
    sleep(1)
    print("This text will not be displayed, as the function will have already terminated")


def error_handler(error_code):
    if error_code == 100:
        print("Error 100: Battle stopped by the stop_battle function")
        print("Hopefully this text will be displayed!")
    else:
        print("Invalid Error Code!")


def battle_loop():
    error_channel = Queue()
    p1 = Process(target=battle)
    p2 = Process(target=stop_battle, args=(error_channel,))
    p1.start()
    p2.start()
    while True:
        error_code = error_channel.get()
        if error_code != "":
            break
    p1.terminate()
    p2.terminate()
    error_handler(error_code)


def main():
    battle_loop()


if __name__ == "__main__":
    main()
