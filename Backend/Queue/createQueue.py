from queue import Queue

def createQueues():
    queue_alerts = Queue()
    queue_navigation = Queue()
    return queue_alerts, queue_navigation

def addQueue(queue,item):
    queue.put(item)

def getFirstQueue(queue):
    if not queue.empty():
        return queue.get()
    return None

if __name__ == "__main__":
    createQueues()