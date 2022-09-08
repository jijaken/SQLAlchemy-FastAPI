from database import Base, SessionLocal
from sqlalchemy import Column, Integer, String
from sqlalchemy.sql.functions import count
from sqlalchemy import select

class User(Base):
    '''
    Описание таблицы user (информация о пользователях) через SQLAlchemy
    '''
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    gender = Column(Integer)
    age = Column(Integer)
    country = Column(String)
    city = Column(String)
    exp_group = Column(Integer)
    os = Column(String)
    source = Column(String)

if __name__ == '__main__':
    session = SessionLocal()

    stmt = select(User.country,User.os,count("*")).where(User.exp_group==3).group_by(User.country, User.os).having(count("*") > 100).order_by(count("*").desc())
    result = session.execute(stmt)
    list_res = []
    for user in result:
        list_res.append(user)
    print(list_res)
