import sqlalchemy
import sqlalchemy.orm

from roadbuds import config

engine = sqlalchemy.create_engine(config.Settings().database_url, pool_pre_ping=True)
SessionLocal = sqlalchemy.orm.sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = sqlalchemy.orm.declarative_base()


# NOTE: To register all models with Base.metadata for schema creation (Base.metadata.create_all()),
# import all feature modules that contain models:
#   from roadbuds import users, assistance  # noqa: F401
# This ensures SQLAlchemy knows about all tables when creating the database schema.


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
