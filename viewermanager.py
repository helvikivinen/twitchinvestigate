from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from viewer import Viewer

class ViewerManager:
    def __init__(self):
        db_file = "sqlite:///database.sqlite3"
        engine = create_engine(db_file, echo=True)
        self.Session = sessionmaker(bind=engine)

    def increment_points(self, users):
        print(f"Users found: {users}")
        for user in users:
            new_viewer = self.insert_user_if_not_exists(user.id, user.name)
            with self.Session() as session:
                print(f"Incrementing Point for {user.name}")
                new_viewer.channel_points += 1
                session.query(Viewer).filter(Viewer.twitch_id == user.id).update(
                    {"channel_points": new_viewer.channel_points}
                )
                session.commit()

    def user_exists_in_db(self, twitch_id):
        with self.Session() as session:
            viewerExists = (
                session.query(Viewer).filter(Viewer.twitch_id == twitch_id).scalar()
            )

        return viewerExists or False

    def insert_user_if_not_exists(self, twitch_id, twitch_name):
        with self.Session() as session:
            viewer = self.user_exists_in_db(twitch_id)
            if viewer:
                return viewer
            else:
                viewer = Viewer(
                    twitch_id=twitch_id,
                    twitch_name=twitch_name,
                    channel_points=0,
                )
            session.expire_on_commit = False
            session.add(viewer)
            session.commit()

        return viewer


    def get_points(self, twitch_id):
        user = self.user_exists_in_db(twitch_id)
        if user:
            return user.channel_points
        else:
            return False
        
    def set_ponts(self, twitch_id, target_points):
        with self.Session() as session:
            print("Session Created")
            session.query(Viewer).filter(Viewer.twitch_id == twitch_id).update(
                {"channel_points": target_points}
            )
            result = session.commit()


    def deduct_points(self, twitch_id, amount):
        user = self.user_exists_in_db(twitch_id)
        if user:
            if self.get_points(twitch_id) >= amount:
                with self.Session() as session:
                    user.channel_points -= amount
                    # sanity check that user can't have negative points
                    user.channel_points = max(user.channel_points, 0)
                    session.commit()
            return user.channel_points
        else:
            return False
