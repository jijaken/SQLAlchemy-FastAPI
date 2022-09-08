from pydantic import BaseModel
from datetime import datetime

class UserGet(BaseModel):
    '''
    Валидация входной информации по классу User (пользователи)
    '''
    id : int
    gender : int
    age : int
    country : str
    city : str
    exp_group : int
    os : str
    source : str
    class Config:
        orm_mode = True

class PostGet(BaseModel):
    '''
    Валидация входной информации по классу Post (посты)
    '''
    id : int
    text : str
    topic : str
    class Config:
        orm_mode = True


class FeedGet(BaseModel):
    '''
    Валидация входной информации по классу Feed (активность)
    '''
    user_id : int
    user: UserGet
    post_id : int
    post: PostGet
    action : str
    time : datetime
    class Config:
        orm_mode = True
