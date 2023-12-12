from sqlalchemy import create_engine

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import sessionmaker

from urllib.parse import quote

mysqlUser = "sam9mo"
mysqlPassword = "sam9mo!!"
mysqlHost = "59.3.28.12"
mysqlPort = 3306
SQLALCHEMY_DATABASE_URL = f'mysql+pymysql://{mysqlUser}:{quote(mysqlPassword)}@{mysqlHost}:{mysqlPort}?charset=utf8'

engine = create_engine(
    url=SQLALCHEMY_DATABASE_URL,
    encoding='utf-8'
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()