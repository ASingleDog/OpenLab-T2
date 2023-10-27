from __future__ import unicode_literals, absolute_import
from sqlalchemy import Integer, Column, String, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from fastapi.encoders import jsonable_encoder


class DbServer:
    __engine = create_engine("sqlite:///data.db")
    __Base = declarative_base()
    Session = sessionmaker(__engine)

    class User(__Base):
        __tablename__ = "User"
        id = Column(Integer, primary_key=True)
        name = Column(String)
        code = Column(String)
        score1 = Column(Integer, default=0)
        score2 = Column(Integer, default=0)
        score3 = Column(Integer, default=0)
        score4 = Column(Integer, default=0)

    def __init__(self):
        try:
            self.__Base.metadata.create_all(self.__engine)
        except:
            pass

    def add(
        self, id: int, name: str, code: str, score1=0, score2=0, score3=0, score4=0
    ):
        session = self.Session()
        try:
            user = self.User(
                id=id,
                name=name,
                code=code,
                score1=score1,
                score2=score2,
                score3=score3,
                score4=score4,
            )

            session.add(user)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def delete(self, id: int):
        session = self.Session()
        try:
            session.query(self.User).filter(self.User.id == id).delete(synchronize_session='fetch')
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def update(
        self,
        id: int,
        name: str | None = None,
        score1: int | None = None,
        score2: int | None = None,
        score3: int | None = None,
        score4: int | None = None,
    ):
        session = self.Session()
        try:
            user = session.query(self.User).filter(self.User.id == id).first()
            
            if name:
                user.name = name
            if score1:
                user.score1 = score1
            if score2:
                user.score2 = score2
            if score3:
                user.score3 = score3
            if score4:
                user.score4 = score4
            
            session.add(user)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def query_all(self):
        session = self.Session()
        try:
            return jsonable_encoder(session.query(self.User).all())
        except Exception as e:
            raise e
        finally:
            session.close()

    def query_one(self, id: int):        
        session = self.Session()
        try:
            return jsonable_encoder(
                session.query(self.User).filter(self.User.id == id).first()
            )
        except Exception as e:
            raise e
        finally:
            session.close()
