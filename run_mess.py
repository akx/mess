import argparse
import logging

if __name__ == "__main__":
	ap = argparse.ArgumentParser("mess", "it's a mess, I tell you")
	ap.add_argument("--debug", "-d", default=False, action="store_true")
	ap.add_argument("--port", "-p", default=5000, type=int)
	ap.add_argument("--recreate-db", default=False, action="store_true")
	ap.add_argument("--dburl")
	ap.add_argument("--insert-interval", default=5, type=float)
	ap.add_argument("-v", "--verbose", default=False, action="store_true")
	ap.add_argument("--squelch-werkzeug", default=False, action="store_true")
	ap.add_argument("--run-test", default=False, action="store_true")
	args = ap.parse_args()
	from mess.app import app

	if args.dburl:
		app.config["DBURL"] = args.dburl

	if args.insert_interval:
		app.config["INSERT_INTERVAL"] = args.insert_interval

	if args.recreate_db:
		from mess.db import get_engine
		from mess.schema import metadata
		engine = get_engine()
		metadata.drop_all(engine, checkfirst=True)
		metadata.create_all(engine)

	if args.verbose:
		logging.basicConfig(level=logging.DEBUG)

	if args.squelch_werkzeug:
		import werkzeug._internal as wi
		wi._log = lambda *a, **k: 0


	if args.run_test:
		from mess.testing import run_test
		run_test()
	else:
		app.run(debug=args.debug, port=args.port)