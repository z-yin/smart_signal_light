import datetime as dt
import time
import numpy as np

b = dt.datetime.fromtimestamp(500000)
c = dt.datetime.fromtimestamp(1493852400)
d = time.mktime(dt.datetime(2017, 5, 17, 8, 0, 0).timetuple())

k = {4: 5}
if 5 - 1 in k:
    print('y')
