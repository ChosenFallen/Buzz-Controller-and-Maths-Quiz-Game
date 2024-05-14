from threading import Thread
import time

def printing():
    for i in range(10):
        print(i)
        time.sleep(1)

thread = Thread(target=printing)
thread.start()
print("TEST 1")
time.sleep(2)
print("TEST 2")
thread.join()
print("DONE")