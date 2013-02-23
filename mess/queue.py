from time import time as T
import mess.db as db

_queue = []
_put = _queue.append

def enqueue(metric, value, system="-", instance=None, time=0):
	if not time:
		time = T()
	_put((time, metric, system, instance, value))
	return len(_queue)

def insert_queue():
	if not _queue:
		return
	process = _queue[:]
	del _queue[:]
	db.insert_measurements(process)
