import random
import time
from mess.queue import enqueue, insert_queue

__author__ = 'Aarni'

def test_inserts(system, instance, n):
	t0 = int(time.time())
	t = int(time.time())
	for x in xrange(n):
		enqueue("kittens.huffed", random.random() * 2500, system=system, instance=instance, time=t - x * 5)
	insert_queue()
	t1 = time.time()
	mps = n / (t1 - t0)
	return mps

def run_test():
	mpses = []
	for x in xrange(40):
		n = 100 + x * 100
		mps = test_inserts("sys%02d" % (x%3), "inst%02d" % x, n)
		print n, mps
		mpses.append(mps)
	print "MPS:", sum(mpses) / float(len(mpses))