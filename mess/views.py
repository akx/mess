import time

from flask import request

from mess.app import app
from mess.queue import enqueue


@app.route("/p")
def post_metric():
	a = request.args
	metric = a.get("m")
	system = a.get("s")
	instance = a.get("i")
	value = a.get("v")
	if metric and value:
		enqueue(metric, system, instance, value)
		return "OK"
	else:
		return "FAIL"
