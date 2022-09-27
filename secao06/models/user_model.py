from email.policy import default
from sqlalchemy import Integer, String, Column, Boolean
from sqlalchemy.orm import relationship
from core.configs import settings

class UserModel(settings.DBBaseModel):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(256), nullable=True)
    lastname = Column(String(256), nullable=True)
    email = Column(String(256), index=True, nullable=True, unique=True)
    pwd = Column(String(256), nullable=False)
    is_admin = Column(Boolean, default=False)
    articles = relationship(
        'ArticleModel',
        cascade='all,delete-orphan',
        back_populates='creator',
        uselist=True,
        lazy='joined'
    )