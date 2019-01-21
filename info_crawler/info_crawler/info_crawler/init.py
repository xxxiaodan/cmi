import time

import start

while 1:
    print 1
    flag= start.start()
    print flag
    if flag:
        time.sleep(10)
