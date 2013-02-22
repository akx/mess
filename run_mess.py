import argparse

if __name__ == "__main__":
	ap = argparse.ArgumentParser("mess", "it's a mess, I tell you")
	ap.add_argument("--debug", "-d", default=False, action="store_true")
	ap.add_argument("--port", "-p", default=5000, type=int)
	ap.add_argument("--recreate-db", default=False, action="store_true")
	ap.add_argument("--dburl")
	ap.add_argument("--run-test", default=False, action="store_true")
	args = ap.parse_args()
	from mess.app import app
	if args.dburl:
		app.config["DBURL"] = args.dburl

	if args.recreate_db:
		from mess.db import engine
		from mess.schema import metadata
		metadata.drop_all(engine, checkfirst=True)
		metadata.create_all(engine)

	if args.run_test:
		from mess.testing import run_test
		run_test()

	else:
		app.run(debug=args.debug, port=args.port)