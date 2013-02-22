from sqlalchemy import *

metadata = MetaData()



db_metrics = Table('metrics', metadata,
    Column('metric_id', Integer, primary_key=True, autoincrement=True),
    Column('name', String(64), nullable=False, index=True),
    Column('display_name', String(64), nullable=True),
    sqlite_autoincrement=True
 )

db_sources = Table('sources', metadata,
    Column('source_id', Integer, primary_key=True, autoincrement=True),
    Column('system', String(64), nullable=False, index=True),
    Column('instance', String(64), index=True),
    UniqueConstraint("system", "instance"),
    sqlite_autoincrement=True
)

db_measures = Table('measures', metadata,
	Column('measure_id', Integer, primary_key=True, autoincrement=True),
	Column('metric_id', Integer, index=True),
	Column('source_id', Integer, nullable=True, index=True),
	Column('timestamp', Integer, index=True),
	Column('value', Numeric(15, 3)),
	sqlite_autoincrement=True
)