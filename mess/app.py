from time import sleep
from flask import Flask
import logging

log = logging.getLogger(__name__)
app = Flask(__name__)
app.config["INSERT_INTERVAL"] = 5
app.config["DBURL"] = "dummy://"
app.config.from_envvar('MESS_SETTINGS', silent=True)
import mess.views

def insert_timer_tick():
	from mess.queue import insert_queue
	insert_queue()


@app.before_first_request
def start_insert_timer():
	interval = app.config["INSERT_INTERVAL"]

	try:
		import uwsgi
		uwsgi.register_signal(131, "", insert_timer_tick)

		uwsgi.add_rb_timer(131, interval)
		return True
	except ImportError:
		pass # Assume uwsgi isn't our flavor

	import threading
	def insert_timer_tick_loop():
		while 1:
			sleep(interval)
			insert_timer_tick()

	thread = threading.Thread(target=insert_timer_tick_loop, name="insert timer")
	thread.setDaemon(True)
	thread.start()
	return True

