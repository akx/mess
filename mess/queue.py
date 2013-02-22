from time import time as T
from mess.db import insert_measurements

_queue = []
_put = _queue.append

def enqueue(metric, value, system="-", instance=None, time=0):
	if not time:
		time = T()
	_put((time, metric, system, instance, value))

def insert_queue():
	process = _queue[:]
	del _queue[:]
	insert_measurements(process)