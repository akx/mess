try:
	import uwsgi
except ImportError:
	uwsgi = None

from time import sleep

def insert_timer_tick(signal=0):
	from mess.queue import insert_queue
	insert_queue()

insert_timer_started = False

def start_insert_timer(app):
	global insert_timer_started
	if insert_timer_started:
		return False
	insert_timer_started = True

	interval = app.config["INSERT_INTERVAL"]

	if uwsgi:
		uwsgi.register_signal(131, "workers", insert_timer_tick)
		uwsgi.add_rb_timer(131, interval)
		return True
	else:
		import threading
		def insert_timer_tick_loop():
			while 1:
				sleep(interval)
				insert_timer_tick()

		thread = threading.Thread(target=insert_timer_tick_loop, name="insert timer")
		thread.setDaemon(True)
		thread.start()
		return True

def configure_timer(app):
	if uwsgi:
		start_insert_timer(app)  # have to start this pre-fork on uwsgi
	else:
		app.before_first_request(lambda:start_insert_timer(app))