import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session
import sqlalchemy.ext.declarative as dec


SqlAlchemyBase = dec.declarative_base()
__factory = None


def global_init(database_file):
    global __factory

    if __factory:
        return

    if not database_file or not database_file.strip():
        raise Exception('Укажите имя файла БД')

    connection_str = f"sqlite:///{database_file.strip()}?check_same_thread=False"
    engine = sa.create_engine(connection_str)
    __factory = orm.sessionmaker(bind=engine)

    from . import __all_models

    SqlAlchemyBase.metadata.create_all(engine)


def create_session() -> Session:
    global __factory
    return __factory()
