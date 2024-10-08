from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import Session
from traceback import format_exc
from utils_common.repetition_decorator import repetition_decorator


class Crud:
    def __init__(self, **kwargs):
        self.connection_string = kwargs['CONNECTION_STRING']
        self.encoding = kwargs.get("ENCODING", 'utf-8')
        self.pool_size = kwargs.get("POOL_SIZE", 10)
        self.max_overflow = kwargs.get("MAX_OVERFLOW", 20)
        self.pool_recycle = kwargs.get("POOL_RECYCLE", 3600)
        self.base = kwargs.get("BASE", None)
        self.logger = kwargs.get("logger", None)

        self._engine = None
        self._session = None

    @property
    def engine(self):
        if self._engine is None:
            self.create_engine()
        return self._engine

    def create_engine(self):
        self._engine = create_engine(
            url=self.connection_string,
            encoding=self.encoding
        )

    @property
    def session(self):
        if self._session is None:
            self.create_session()
        return self._session

    def create_session(self):
        self._session = Session(bind=self.engine)

    def initiate(self):
        self.create_engine()
        self.create_session()
        self.create_tables()

    def create_tables(self):
        try:
            for key in self.base.metadata.tables.keys():
                if not inspect(self.engine).has_table(key):
                    self.base.metadata.create_all(self.engine)
        except Exception:
            if self.logger:
                self.logger.critical(format_exc())

    def insert(self,
               instances,
               refresh=False):
        try:
            self.session.add(instances)
            self.session.commit()
            if refresh:
                self.session.refresh(instances)
            return instances
        except Exception:
            if self.logger:
                self.logger.warning(format_exc())
            self.session.rollback()
            raise

    @repetition_decorator(repetition=10,
                          caught_exceptions=(Exception,),
                          raised_exceptions=(),
                          sleep_between_each=0.5)
    def commit(self):
        try:
            return self.session.commit()
        except Exception:
            if self.logger:
                self.logger.warning(format_exc())
            self.session.rollback()
            raise

    def find(
            self,
            query='',
            filter_str='',
            fetch='one'
    ):
        """
        :param query:should be name of the class in models.py
        :param filter_str: should be based on name of classes in models.py
        :param fetch: 'one' or 'all'
        self.session.query(Files).filter(Files.id==1).all()
        :return:
        """
        if not self.session:
            self.create_session()

        query = self.session.query(eval(query))
        if filter_str:
            query = query.filter(eval(filter_str))

        if fetch in ('one', 1,):
            return [query.one()]
        elif fetch in ('all',):
            return query.all()
        else:
            raise

    # @manage_exceptions_decorator(report_traceback=False)
    # def __del__(self):
    #     self.close_session()
    #     self.close_all_connections()
    #
    def close_session(self):
        try:
            self._session.close()
        except Exception:
            if self.logger:
                self.logger(format_exc())

    def close_all_connections(self):
        try:
            self.engine.dispose()
        except Exception:
            if self.logger:
                self.logger(format_exc())


def crud_creator(**kwargs):
    crud = Crud(**kwargs)
    crud.initiate()
    return {"crud": crud}
