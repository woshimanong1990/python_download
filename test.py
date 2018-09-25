import sys
import multiprocessing
import time

def consumer(queue):
    print("consumer start")
    while True:
        if queue.empty():
            continue
        print("consumer item")
        item= queue.get()
        print("consumer", item)
        time.sleep(0.1)
def publishe(queue):
    print("publishe start")
    while True:
        queue.put(time.time())
        time.sleep(0.3)
        print("publishe put")


if __name__ == "__main__":
    p = multiprocessing.Pool(processes=2)
    manager = multiprocessing.Manager()
    queue = manager.Queue(10)
    p1 = multiprocessing.Process(target=consumer, args=(queue, ))
    
    for i in range(2):
        result = p.apply_async(publishe, args=(queue,))
    
    p1.start()
    p.close()
    p.join()
    p1.join()

