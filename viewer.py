from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()


class Viewer(Base):
    __tablename__ = "viewers"
    id = Column(Integer, primary_key=True)
    twitch_id = Column(Integer)
    twitch_name = Column(String)
    channel_points = Column(Integer)
