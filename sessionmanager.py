import os
from sqlalchemy import Column, Integer, MetaData, String, Table, create_engine
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from viewer import Viewer
from types import SimpleNamespace


class SessionManager:
    def __init__(self):
        if not os.path.isfile('database.sqlite3'):
            with open('database.sqlite3', 'w'): pass

        db_file = "sqlite:///database.sqlite3"
        engine = create_engine(db_file, echo=False)

        if not sqlalchemy.inspect(engine).has_table("viewers"):
            meta_data = MetaData()
            viewers = Table('viewers', meta_data, 
                  Column('id', Integer, primary_key=True, nullable=False),
                  Column('twitch_id', Integer),
                  Column('twitch_name', String),
                  Column('channel_points', Integer),
                  )
            viewers.create(engine)
        
        session_maker = sessionmaker(bind=engine)
        self.Session = session_maker()
        self.Session.expire_on_commit = False

    def __del__(self):
        self.Session.close()

    def increment_points(self, users):
        print(f"Users found: {users}")
        for user in users:
            new_viewer = self.insert_user_if_not_exists(user.id, user.name)

            print(f"Incrementing Point for {user.name}")
            new_viewer.channel_points += 1
            self.Session.query(Viewer).filter(Viewer.twitch_id == user.id).update(
                {"channel_points": new_viewer.channel_points}
            )
            self.Session.commit()

    def user_exists_in_db(self, twitch_id):
        viewerExists = (
            self.Session.query(Viewer).filter(Viewer.twitch_id == twitch_id).scalar()
        )
        return viewerExists or False

    def insert_user_if_not_exists(self, twitch_id, twitch_name):
        viewer = self.user_exists_in_db(twitch_id)
        if viewer:
            return viewer
        else:
            viewer = Viewer(
                twitch_id=twitch_id,
                twitch_name=twitch_name,
                channel_points=0,
            )
        self.Session.add(viewer)
        self.Session.commit()

        return viewer

    def get_points(self, twitch_id):
        user = self.user_exists_in_db(twitch_id)
        if user:
            return user.channel_points
        else:
            return False

    def set_points(self, twitch_id, target_points):
        print("Session Created")
        self.Session.query(Viewer).filter(Viewer.twitch_id == twitch_id).update(
            {"channel_points": target_points}
        )
        self.Session.commit()

    def deduct_points(self, twitch_id, amount):
        user = self.user_exists_in_db(twitch_id)
        if user and user.channel_points >= amount:
            user.channel_points -= amount
            # sanity check that user can't have negative points
            user.channel_points = max(user.channel_points, 0)
            self.Session.commit()
            return user.channel_points
        else:
            return False

    def get_top_users_by_points(self):
        rows = (
            self.Session.query(Viewer)
            .order_by(Viewer.channel_points.desc())
            .limit(3)
            .all()
        )
        self.Session.commit()
        top_users = []
        for row in rows:
            top_users.append(
                SimpleNamespace(
                    **{
                        "twitch_name": row.twitch_name,
                        "channel_points": row.channel_points,
                    }
                )
            )
        return top_users
