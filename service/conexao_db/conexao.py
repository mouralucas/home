from __future__ import annotations

from typing import Optional

import sqlalchemy as db
from sqlalchemy.orm import sessionmaker

from base.settings import DATABASES


class SqlAlchemyMeta(type):
    _instance: Optional[SqlAlchemy] = None

    def __call__(cls) -> SqlAlchemy:
        if cls._instance is None:
            cls._instance = super().__call__()
        return cls._instance


class SqlAlchemy:
    def __init__(self, user=DATABASES['default']['USER'], senha=DATABASES['default']['PASSWORD'], host=DATABASES['default']['HOST'],
                 porta=DATABASES['default']['PORT'], database=DATABASES['default']['NAME']):
        self.user = user
        self.senha = senha
        self.host = host
        self.porta = porta
        self.database = database
        self.engine = None
        self.conexao = None
        self.metadata = None
        self.session = None
        self.resultset = None

        self.conectar()
        # self.cria_sessao()

    def conectar(self):
        database_url = 'postgresql+psycopg2://{user}:{password}@{host}/{database_name}'.format(
            user=self.user,
            password=self.senha,
            host=self.host,
            database_name=self.database,
        )

        self.engine = db.create_engine(database_url)
        self.conexao = self.engine.connect()
        self.metadata = db.MetaData()

    def cria_sessao(self):
        self.session = sessionmaker(bind=self.engine)()

    def get_conexao(self):
        return self.conexao

    def criar_tabela_meta(self, nm_tabela):
        table = db.Table(nm_tabela, self.metadata, autoload=True, autoload_with=self.engine)

        return table

    def buscar(self, query=None, retorno_dict=True):
        with self.conexao.begin():
            self.resultset = self.conexao.execute(query)

        return self.resultset
        
    def get_dict(self):
        if not self.resultset:
            return False

        d, resultlist = {}, []
        for i in self.resultset:
            for column, value in i.items():
                d = {**d, **{column: value}}
                # d = {k: 0 if not v else v for k, v in d.items()}
            resultlist.append(d)

        return resultlist
