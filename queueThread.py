from threading import Thread
import Queue
import time

def produce(queue, host, numID):
    print "[+]", numID, "Scraping information on host:", host
    time.sleep(1)
    print "[+]", numID, "Putting it in the queue..."
    queue.put(host)

def consume(queue):
    while True:
        item = queue.get()
        print "[+] Processing item:", str(item)
        q.task_done()

if __name__ == "__main__":
    # start consumer thread. Grabs crap off of the queue, and does work
    q = Queue.Queue()
    
    t = Thread(target=consume, args=(q,))
    t.daemon= True
    t.start()
    print "[+] Started the daemon thread"
    
    # Start the producers
    hosts = ["lol", "abc", "nowai", "ERMERGERD"]

    for x in range(len(hosts)):
        t = Thread(target=produce, args=(q, hosts[x], x))
        t.start()
        time.sleep(1)

    q.join()
    
    
    




    
