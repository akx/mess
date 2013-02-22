from sqlalchemy import create_engine, select
from mess.app import app
from mess.schema import db_measures, db_metrics, db_sources
engine = create_engine(app.config["DBURL"])

try:
	from MySQLdb.cursors import BaseCursor
	BaseCursor._defer_warnings = True
except:
	pass

metric_cache = {}
source_cache = {}

def get_metric_id(conn, name):
	name = unicode(name).lower().strip()
	metric_id = metric_cache.get(name)
	if metric_id:
		return metric_id

	metric_id = conn.execute(select([db_metrics.c.metric_id], db_metrics.c.name == name)).scalar()
	if not metric_id:
		metric_id = conn.execute(db_metrics.insert({db_metrics.c.name: name})).inserted_primary_key[0]

	metric_cache[name] = metric_id

	return metric_id

def get_source_id(conn, system, instance):
	system = unicode(system).lower().strip()
	instance = unicode(instance).lower().strip()
	if not instance:
		instance = None
	cache_key = (system, instance)
	source_id = source_cache.get(cache_key)
	if source_id:
		return source_id

	source_id = conn.execute(select(
		[db_sources.c.source_id],
		(db_sources.c.system == system) & (db_sources.c.instance == instance))
	).scalar()

	if not source_id:
		source_id = conn.execute(db_sources.insert({db_sources.c.system: system, db_sources.c.instance: instance})).inserted_primary_key[0]

	source_cache[cache_key] = source_id

	return source_id

def insert_measurements(mlist):
	with engine.connect() as conn:

		inserts = []
		for (time, metric, system, instance, value) in mlist:
			metric_id = get_metric_id(conn, metric)
			source_id = get_source_id(conn, system, instance)
			inserts.append({'timestamp': time, 'metric_id': metric_id, 'source_id': source_id, 'value': value})
		with conn.begin():
			db_measures.insert(bind=conn).values(inserts).execute()