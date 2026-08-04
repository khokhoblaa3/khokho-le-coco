from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from .database import base
from sqlalchemy.orm import relationship

class user(base):
    __tablename__ = "user"

    name = Column(String, nullable = False)
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, server_default=text('now()'))
    
class Posts(base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key = True, nullable = False)
    title = Column(String, nullable = False)
    content = Column(String, nullable=False)
    rating = Column(Integer, nullable=True)
    published = Column(Boolean, server_default='TRUE', nullable = False)
    created_at = Column(TIMESTAMP, nullable=False, server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    owner = relationship("user")


class Votes(base): 
    __tablename__ = "votes"

    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable = False,  primary_key=True )
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), nullable = False,  primary_key=True )