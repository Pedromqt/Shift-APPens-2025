from queue import Queue

navigationQueue = Queue()
alertsQueue = Queue()

def addQueue(queue,item):
    queue.put(item)

def getFirstQueue(queue):
    if not queue.empty():
        return queue.get()
    return None