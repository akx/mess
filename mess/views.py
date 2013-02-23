import time

from flask import request
from mess.app import app
from mess.queue import enqueue


@app.route("/p",  methods=("GET", "POST"))
def post_metric():
	a = request.args
	metric = a.get("m")
	system = a.get("s")
	instance = a.get("i")
	try:
		value = float(a.get("v"))
	except ValueError:
		return "FAIL VALUE"

	if metric:
		n = enqueue(metric, value, system, instance)
		return "OK %d" % n
	else:
		return "FAIL METRIC"
