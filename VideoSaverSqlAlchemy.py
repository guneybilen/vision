import sqlalchemy
import os
from sqlalchemy.orm import registry
#from sqlalchemy.orm import select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func
import sqlalchemy as db

mapper_registry = registry()
Base = mapper_registry.generate_base()

class VideoBase(Base):
    __abstract__ = True

    created_on = db.Column(db.DateTime, default=db.func.now())
    updated_on = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
  
class Video(Base):
  
    #__table_args__ = {'schema': 'sakila'}
    __tablename__ = 'video'
  
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    extension = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(50), nullable=False)
    created_time = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_time = db.Column(db.DateTime(timezone=True), onupdate=func.now())

  
  
# DEFINE THE ENGINE (CONNECTION OBJECT)
engine = db.create_engine("mysql://user:user??@localhost/vision")
  
# CREATE A SESSION OBJECT TO INITIATE QUERY IN DATABASE
Session = sessionmaker(bind=engine)
session = Session()
  
# SELECT COUNT(*) FROM Actor
# result = session.query("Video").count()


class VideoToDatabase():

	@staticmethod
	def record(name, extension, description):
		vid = Video(name = name, extension=extension, description = description)

		session.add(vid)   
		session.commit()
		print(name + extension + " has been saved to the database!")


class DatabaseInformation():

	@staticmethod
	def getInfo(name, extension):
		out, ext = os.path.splitext(name)
		if ext == "":
			vid = session.query(Video).filter_by(name = name).one()
		#else:
			#vid = session.query(Video).filter(out == out).one()
		print(name + ext + " description has been read from the database!")
		print(vid.description)


