import threading
from time import sleep, ctime
loops = [4,2,5,8,3,10,1,7]

def loop(nloop, nsec):
    print("start loop %d at: %s" % (nloop, ctime()))
    sleep(nsec)
    print("loop %d done at: %s" % (nloop, ctime()))

def main():
    print("starting at: %s" % ctime())
    threads = []
    nloops = range(len(loops))

    for i in nloops:
        t = threading.Thread(target=loop,
            args=(i, loops[i]))
        threads.append(t)
    
    for i in nloops:
        threads[i].start()

    for i in nloops:
        threads[i].join()
    
    print("all Done at: %s" % ctime())

if __name__ == "__main__":
    main()