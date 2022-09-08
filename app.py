from sqlalchemy.orm import Session
from typing import List
from sqlalchemy import func

from fastapi import FastAPI, Depends, HTTPException
from database import SessionLocal


from schema import UserGet, PostGet, FeedGet
from table_user import User
from table_post import Post
from table_feed import Feed

from loguru import logger
from sqlalchemy import desc


app = FastAPI()

def get_db():
    '''
    Сессия с базой данных
    '''
    with SessionLocal() as db:
        return db

def check_errors(result):
    '''
    Проверка ошибок
    '''
    if result is None:
        raise HTTPException(404 ,detail='User not found')


@app.get('/user/{id}',response_model = UserGet)
def get_user(id: int , db: Session = Depends(get_db)):
    '''
    Вывод информации пользователя по id
    '''
    result = db.query(User)\
        .filter(User.id==id)\
        .first()
    logger.info(result)
    check_errors(result)
    return result

@app.get('/user/{id}/feed', response_model = List[FeedGet])
def get_user_feed(id: int, db: Session = Depends(get_db), limit:int = 10):
    '''
    Вывод активность пользователя по id за последнее время
    '''
    result = db.query(Feed)\
        .filter(Feed.user_id==id)\
        .order_by(Feed.time.desc())\
        .limit(limit)\
        .all()
    logger.info(result)
    return result

@app.get('/post/{id}',response_model = PostGet)
def get_post(id: int, db: Session = Depends(get_db)):
    '''
    Вывод информации о постах по id
    '''
    result = db.query(Post)\
        .filter(Post.id==id)\
        .first()
    logger.info(result)
    check_errors(result)
    return result

@app.get('/post/{id}/feed', response_model = List[FeedGet])
def get_post_feed(id: int, db: Session = Depends(get_db), limit:int = 10):
    '''
    Вывод активность на посте по id за последнее время
    '''
    result = db.query(Feed)\
        .filter(Feed.post_id==id)\
        .order_by(Feed.time.desc())\
        .limit(limit)\
        .all()
    logger.info(result)
    return result

@app.get('/post/recommendations/')
def get_recommended_feed(id:int,db: Session = Depends(get_db),limit:int = 10):
    '''
    Вывести топ постов по лайкам
    '''
    #Ещё решение
    #stmt = db.query(Feed.post_id, func.count(Feed.action).label('count')).filter(Feed.action=='like').group_by(Feed.post_id).subquery()

    #result = db.query(Post.id,Post.text,Post.topic) \
    #    .select_from(stmt)\
    #    .join(Post, stmt.c.post_id==Post.id)\
    #    .order_by(stmt.c.count.desc())\
    #    .limit(limit).all()
    ##
    result = db.query(Post)\
        .select_from(Feed)\
        .filter(Feed.action=='like') \
        .join(Post) \
        .group_by(Post.id)\
        .order_by(desc(func.count(Post.id))) \
        .limit(limit).all()

    logger.info(result)
    return result
