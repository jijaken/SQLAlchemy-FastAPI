from database import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey, select
from sqlalchemy.orm import relationship
from database import SessionLocal
from table_user import User
from table_post import Post

class Feed(Base):
    '''
    Описание таблицы feed_action (активность) через SQLAlchemy
    '''
    __tablename__ = 'feed_action'
    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    user = relationship('User')
    post_id = Column(Integer, ForeignKey('post.id'), primary_key=True)
    post = relationship('Post')
    action = Column(String)
    time = Column(TIMESTAMP)

if __name__ == '__main__':
    session = SessionLocal()

    stmt = select(Post.text, Post.topic, Feed.user_id, Feed.post_id, Feed.action, Feed.time, User.gender ).limit(1)
    result = session.execute(stmt)
    list_res = []
    for feed in result:
        list_res.append(feed)
    print(list_res)