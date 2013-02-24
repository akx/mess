import os
from flask import Flask
import logging

log = logging.getLogger(__name__)

def configure(app):
	app.config["INSERT_INTERVAL"] = int(os.environ.get("MESS_INSERT_INTERVAL", 5))
	app.config["DBURL"] = os.environ.get("MESS_DBURL", "dummy://")
	if os.environ.get("MESS_DEBUG"):
		logging.basicConfig(level=logging.DEBUG)
	app.config.from_envvar('MESS_SETTINGS', silent=True)
	from mess.timer import configure_timer
	configure_timer(app)


app = Flask(__name__)
configure(app)
import mess.views  # Pull in views
